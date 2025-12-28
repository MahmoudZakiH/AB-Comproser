# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    is_internal_transfer = fields.Boolean(
        string='Internal Transfer',
        default=False,
        help='Check this box if this is an internal transfer between journals'
    )
    
    destination_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Destination Journal',
        domain="[('type', 'in', ('bank','cash')), ('company_id', '=', company_id), ('id', '!=', journal_id)]",
        check_company=True,
        help='The destination journal for internal transfer'
    )
    
    paired_internal_transfer_payment_id = fields.Many2one(
        comodel_name='account.payment',
        string='Paired Transfer Payment',
        readonly=True,
        help='The corresponding payment created for the internal transfer'
    )

    @api.onchange('is_internal_transfer')
    def _onchange_is_internal_transfer(self):
        """Clear partner when internal transfer is selected"""
        if self.is_internal_transfer:
            self.partner_id = False
            self.destination_journal_id = False

    @api.constrains('is_internal_transfer', 'destination_journal_id')
    def _check_internal_transfer_destination(self):
        """Validate that destination journal is set for internal transfers"""
        for payment in self:
            if payment.is_internal_transfer and not payment.destination_journal_id:
                raise ValidationError(_('Please select a destination journal for internal transfer.'))
            if payment.is_internal_transfer and payment.journal_id == payment.destination_journal_id:
                raise ValidationError(_('Source and destination journals must be different.'))

    def action_post(self):
        """Override to create paired payment for internal transfers"""
        res = super(AccountPayment, self).action_post()
        
        for payment in self:
            if payment.is_internal_transfer and not payment.paired_internal_transfer_payment_id:
                payment._create_paired_internal_transfer()
        
        return res

    def _create_paired_internal_transfer(self):
        """Create the opposite payment for internal transfer"""
        self.ensure_one()
        
        if not self.is_internal_transfer or not self.destination_journal_id:
            return
        
        # Determine the opposite payment type
        if self.payment_type == 'outbound':
            new_payment_type = 'inbound'
        else:
            new_payment_type = 'outbound'
        
        # Prepare values for the new payment
        payment_vals = {
            'payment_type': new_payment_type,
            'partner_type': self.partner_type,
            'journal_id': self.destination_journal_id.id,  # Swap: destination becomes source
            'destination_journal_id': self.journal_id.id,  # Swap: source becomes destination
            'amount': self.amount,
            'currency_id': self.currency_id.id,
            'date': self.date,
            'memo': _('Internal Transfer from %s') % self.name,
            'is_internal_transfer': True,
            'paired_internal_transfer_payment_id': self.id,
        }
        
        # Create the paired payment
        paired_payment = self.create(payment_vals)
        
        # Link back to original payment
        self.write({'paired_internal_transfer_payment_id': paired_payment.id})
        
        # Post the paired payment
        paired_payment.action_post()
        
        # Auto-reconcile the transfer account lines
        self._reconcile_internal_transfer_lines(paired_payment)
        
        return paired_payment

    def _reconcile_internal_transfer_lines(self, paired_payment):
        """Reconcile the transfer account lines between original and paired payments"""
        self.ensure_one()
        
        if not self.company_id.transfer_account_id:
            return
        
        transfer_account = self.company_id.transfer_account_id
        
        # Get move lines from both payments that use the transfer account
        original_lines = self.move_id.line_ids.filtered(
            lambda l: l.account_id == transfer_account and not l.reconciled
        )
        paired_lines = paired_payment.move_id.line_ids.filtered(
            lambda l: l.account_id == transfer_account and not l.reconciled
        )
        
        # Reconcile the lines
        lines_to_reconcile = original_lines + paired_lines
        if lines_to_reconcile and len(lines_to_reconcile) >= 2:
            lines_to_reconcile.reconcile()

    def action_draft(self):
        """Override to handle paired payments when setting to draft"""
        for payment in self:
            if payment.is_internal_transfer and payment.paired_internal_transfer_payment_id:
                if payment.paired_internal_transfer_payment_id.state == 'posted':
                    raise UserError(_(
                        'Cannot set this payment to draft because it has a paired internal transfer payment that is posted. '
                        'Please set the paired payment to draft first.'
                    ))
        return super(AccountPayment, self).action_draft()

    def action_cancel(self):
        """Override to handle paired payments when canceling"""
        for payment in self:
            if payment.is_internal_transfer and payment.paired_internal_transfer_payment_id:
                paired = payment.paired_internal_transfer_payment_id
                if paired.state not in ['cancel', 'draft']:
                    paired.action_cancel()
        return super(AccountPayment, self).action_cancel()

    def _prepare_move_line_default_vals(self, write_off_line_vals=None, force_balance=None):
        """Override to use company transfer account for internal transfers"""
        line_vals_list = super(AccountPayment, self)._prepare_move_line_default_vals(write_off_line_vals, force_balance)
        
        if self.is_internal_transfer and self.company_id.transfer_account_id:
            # Get the transfer account from company
            transfer_account = self.company_id.transfer_account_id
            
            # Replace the counterpart account (customer/vendor account) with transfer account
            # The counterpart line is the one with destination_account_id
            for line_vals in line_vals_list:
                if line_vals.get('account_id') == self.destination_account_id.id:
                    line_vals['account_id'] = transfer_account.id
                    break
        
        return line_vals_list

