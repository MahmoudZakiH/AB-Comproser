# Changelog - IBS Accounting Internal Transfer

## Version 1.1 - Enhanced Journal and Account Handling

### New Features Added

#### 1. **Override `_compute_journal_id` Method**
When internal transfer is enabled, the system now automatically uses the destination journal as the payment journal.

**How it works:**
- When `is_internal_transfer = True` and `destination_journal_id` is set
- The payment's `journal_id` is automatically set to `destination_journal_id`
- This ensures the journal entry is created in the correct journal

**Example:**
```
User selects:
- Internal Transfer: ✓ ON
- Destination Journal: Cash Register

System automatically sets:
- Journal: Cash Register (from destination)
```

#### 2. **Override `_prepare_move_line_default_vals` Method**
The move lines now use the destination journal's default account instead of the source journal's account.

**How it works:**
- When creating journal entries for internal transfers
- The liquidity line account is changed from source journal's account to destination journal's account
- This ensures proper accounting in the correct accounts

**Example:**
```
Original behavior:
- Debit: Outstanding Payment Account
- Credit: Bank A Account

New behavior (internal transfer):
- Debit: Outstanding Payment Account  
- Credit: Cash Register Account (from destination journal)
```

### Technical Details

#### Method: `_compute_journal_id`
```python
@api.depends('company_id', 'partner_id', 'is_internal_transfer', 'destination_journal_id')
def _compute_journal_id(self):
    """Override to use destination journal for internal transfers"""
    for payment in self:
        # For internal transfers, use the destination journal
        if payment.is_internal_transfer and payment.destination_journal_id:
            payment.journal_id = payment.destination_journal_id
            continue
        
        # Default logic from parent for non-internal transfers
        ...
```

**Dependencies:**
- `company_id`
- `partner_id`
- `is_internal_transfer`
- `destination_journal_id`

**Logic:**
1. Check if payment is internal transfer
2. If yes and destination journal is set → use destination journal
3. If no → use default Odoo logic (partner payment method or company default)

#### Method: `_prepare_move_line_default_vals`
```python
def _prepare_move_line_default_vals(self, write_off_line_vals=None):
    """Override to use destination journal's account for internal transfers"""
    line_vals_list = super()._prepare_move_line_default_vals(write_off_line_vals)
    
    if self.is_internal_transfer and self.destination_journal_id:
        destination_account = self.destination_journal_id.default_account_id
        
        if destination_account:
            # Update the liquidity line to use destination journal's account
            for line_vals in line_vals_list:
                if line_vals.get('account_id') == self.journal_id.default_account_id.id:
                    line_vals['account_id'] = destination_account.id
                    break
    
    return line_vals_list
```

**Logic:**
1. Call parent method to get default move lines
2. If internal transfer and destination journal exists
3. Get destination journal's default account
4. Find the liquidity line (line with source journal's account)
5. Replace it with destination journal's account

### Complete Flow Example

**Scenario: Transfer $1,000 from Bank A to Cash Register**

#### Step 1: User Creates Payment
```
Internal Transfer: ✓ ON
Payment Type: Send Money
Source Journal: Bank A
Destination Journal: Cash Register
Amount: $1,000
```

#### Step 2: System Processes (_compute_journal_id)
```
journal_id = Cash Register (from destination_journal_id)
```

#### Step 3: System Creates Move Lines (_prepare_move_line_default_vals)
```
Original Payment (Send Money):
- Debit: Outstanding Payment Account - $1,000
- Credit: Cash Register Account - $1,000 (from destination journal)
```

#### Step 4: System Creates Paired Payment
```
Paired Payment (Receive Money):
- journal_id = Bank A (swapped from original source)
- destination_journal_id = Cash Register (swapped from original destination)

Move Lines:
- Debit: Bank A Account - $1,000 (from destination journal)
- Credit: Outstanding Receipt Account - $1,000
```

#### Step 5: Final Result
```
Bank A Account: -$1,000 (decreased)
Cash Register Account: +$1,000 (increased)
Outstanding accounts reconcile each other
```

### Benefits

1. **Correct Journal Entries**: Entries are created in the appropriate journals
2. **Proper Accounts**: Uses the correct accounts from each journal
3. **Automatic Reconciliation**: Outstanding accounts can be reconciled
4. **Clean Accounting**: Maintains proper double-entry bookkeeping
5. **Audit Trail**: Clear trail of fund movement between journals

### Upgrade Notes

If you already have the module installed:
1. Update the module to get these new features
2. Test with a small internal transfer first
3. Verify the journal entries are correct
4. Check that accounts match your expectations

### Version History

- **v1.1**: Added journal and account handling overrides
  - Override `_compute_journal_id`
  - Override `_prepare_move_line_default_vals`
  
- **v1.0**: Initial release
  - Internal transfer toggle
  - Destination journal field
  - Automatic paired payment creation
  - Journal swapping
  - Payment type reversal

### Testing Checklist

After upgrading, test:
- [ ] Internal transfer creates payment in destination journal
- [ ] Move lines use destination journal's account
- [ ] Paired payment uses correct swapped journals
- [ ] Paired payment uses correct swapped accounts
- [ ] Outstanding accounts can be reconciled
- [ ] Journal entries balance correctly
- [ ] Reports show correct balances

### Known Limitations

- Only works with bank and cash journals
- Requires destination journal to have a default account configured
- Both journals must be in the same company
- Currency must be the same for both journals

### Support

For questions or issues:
- Review the README.md for usage instructions
- Check FLOW_DIAGRAM.md for visual explanation
- Review Odoo logs for error messages
- Contact your system administrator

