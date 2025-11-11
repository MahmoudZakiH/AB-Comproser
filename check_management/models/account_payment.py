# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    payment_check_lines = fields.One2many('payment.check.line', 'payment_id')
    is_check_journal = fields.Boolean(string="is check journal", related="journal_id.is_check")
    is_debit_journal = fields.Boolean(string="is Debit journal", related="journal_id.is_debit")
    total_check_amount = fields.Float(string="Total Check Amount", compute="compute_total_check_amount", store=True,
                                      default=0.0)
    existing_check_lines = fields.Many2many('payment.check.line')
    exist_check = fields.Boolean(string='From Existing Checks', default=False)
    effective_date = fields.Date('Effective Date',
                                 help='Effective date of PDC', copy=False,
                                 default=False)
    payment_type = fields.Selection([
        ('outbound', 'Send'),
        ('inbound', 'Receive'),
        ('transfer', 'Transfer'),
    ], string='Payment Type', default='inbound', required=True, tracking=True)
    bank_account = fields.Integer('Bank Account')

    # @api.depends('payment_check_lines.check_amount', 'payment_check_lines')
    # def compute_total_check_amount(self):
    #     # print("Compute Total")
    #     for rec in self:
    #         if rec.payment_check_lines:
    #             if rec.is_check_journal:
    #                 total = 0
    #                 for line in rec.payment_check_lines:
    #                     if line.state != 'cancel':
    #                         total += line.check_amount
    #                 rec.write({'total_check_amount': total, 'amount': total})
    #         else:
    #             rec.write({'total_check_amount': 0.0})
    #             return

    @api.depends('payment_check_lines.check_amount', 'payment_check_lines')
    def compute_total_check_amount(self):
        for rec in self:
            total = 0
            if rec.payment_check_lines:
                if rec.is_check_journal:
                    for line in rec.payment_check_lines:
                        if line.state != 'cancel':
                            total += line.check_amount
                    rec.write({'total_check_amount': total})
                else:
                    rec.write({'total_check_amount': total})
            else:
                rec.write({'total_check_amount': total})

    def action_post(self):
        for rec in self:
            if rec.is_check_journal:
                rec.amount = rec.total_check_amount
        return super(AccountPayment, self).action_post()

    def button_check_lines(self):
        return {
            'name': _('Check Lines'),
            'view_type': 'form',
            'view_mode': 'list,form',
            'res_model': 'payment.check.line',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.payment_check_lines.ids)],
        }

    def compute_existing_check_lines(self):
        if not self.existing_check_lines:
            raise UserError("Warning , Please choose checks")

        for check in self.existing_check_lines:
            self.env['payment.check.line'].create({
                'payment_id': self.id,
                'check_number': check.check_number,
                'check_date': check.check_date,
                'check_amount': check.check_amount,
                'check_bank_id': check.check_bank_id.id,
                'with_drawer_name': check.with_drawer_name,
                'currency_id': check.currency_id.id,
                'customer_check_id': check.id,
                'bank_branch': check.bank_branch,
                'account_owner': check.account_owner,
                'mozahar': check.mozahar,
                'mosatar': check.mosatar,
                'desc': check.desc,
            })
            check.state = 'to_vendor'
        return {
            'name': _('Payments'),
            'view_type': 'form',
            'view_mode': 'list,form',
            'res_model': 'account.payment',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', '=', self.id)],
        }

    def compute_delete_existing_check_lines(self):
        for rec in self:
            for line in rec.payment_check_lines:
                line.customer_check_id.state = 'holding'
                line.state = 'cancel'
            rec.payment_check_lines = [(5, 0, 0)]

    def cancel2(self):
        for rec in self:
            if rec.move_id:
                rec.move_id.line_ids.remove_move_reconcile()

    @api.onchange('journal_id')
    def onchange_payment_type_check(self):
        if self.journal_id.is_debit and self.payment_type == 'outbound':
            self.exist_check = True
        else:
            self.exist_check = False
