# Internal Transfer Account Configuration Guide

## Overview

The module now uses a **company-level transfer account** as the counterpart for all internal transfer journal entries. This provides a centralized account for tracking internal fund movements.

---

## Configuration

### Step 1: Set Up Transfer Account

The `transfer_account_id` field already exists in your system (from the `check_management` module). To configure it:

1. Go to **Settings** → **Accounting**
2. Look for the **Transfer Account** or **Internal Transfer Account** field
3. Select an account to use for internal transfers
4. Click **Save**

**Note:** This field is shared with the check management module, so any configuration here will affect both modules.

**Recommended Account Types:**
- Current Assets (for temporary transfers)
- Bank and Cash (for transit accounts)
- Avoid: Receivable or Payable accounts

---

## How It Works

### Journal Entry Structure

When you create an internal transfer, the system creates journal entries using the **company transfer account** as the counterpart.

#### Example: Transfer $1,000 from Bank A to Cash Register

**Configuration:**
- Company Transfer Account: `1050 - Internal Transfer Account`
- Bank A Account: `1010 - Bank A`
- Cash Register Account: `1020 - Cash Register`

**Payment 1 (Original - Send Money):**
```
Journal: Bank A
Date: 2025-11-02

Debit  | Credit | Account                      | Amount
-------|--------|------------------------------|--------
       | 1,000  | 1010 - Bank A                | 1,000
1,000  |        | 1050 - Internal Transfer     | 1,000
```

**Payment 2 (Paired - Receive Money):**
```
Journal: Cash Register
Date: 2025-11-02

Debit  | Credit | Account                      | Amount
-------|--------|------------------------------|--------
1,000  |        | 1020 - Cash Register         | 1,000
       | 1,000  | 1050 - Internal Transfer     | 1,000
```

**Net Effect:**
- Bank A: **-$1,000** (decreased)
- Cash Register: **+$1,000** (increased)
- Transfer Account: **$0** (balanced - debit and credit cancel out)

---

## Technical Implementation

### Modified Files

1. **`models/account_payment.py`**
   - Added `_prepare_move_line_default_vals()` override
   - Uses company transfer account for counterpart line
   - Uses existing `transfer_account_id` from `check_management` module

2. **`__manifest__.py`**
   - Added dependency on `check_management` module to access `transfer_account_id`

### Code Logic

```python
def _prepare_move_line_default_vals(self, write_off_line_vals=None):
    """Override to use company transfer account for internal transfers"""
    line_vals_list = super()._prepare_move_line_default_vals(write_off_line_vals)
    
    if self.is_internal_transfer and self.company_id.transfer_account_id:
        transfer_account = self.company_id.transfer_account_id
        
        # Update the counterpart line (not the liquidity line)
        for line_vals in line_vals_list:
            if line_vals.get('account_id') != self.journal_id.default_account_id.id:
                line_vals['account_id'] = transfer_account.id
                break
    
    return line_vals_list
```

---

## Complete Flow Example

### Scenario: Transfer $5,000 from Main Bank to Petty Cash

#### Step 1: Configuration
```
Settings → Accounting:
- Transfer Account: 1050 - Internal Transfer Account
```

#### Step 2: Create Payment
```
Accounting → Payments → New:
- Internal Transfer: ✓ ON
- Payment Type: Send Money
- Journal: Main Bank
- Destination Journal: Petty Cash
- Amount: $5,000
- Date: 2025-11-02
```

#### Step 3: Confirm Payment

**System Creates Payment 1:**
```
Journal: Main Bank
Reference: BANK/2025/0001

Move Lines:
Line 1:
  - Account: 1010 - Main Bank
  - Credit: $5,000
  
Line 2:
  - Account: 1050 - Internal Transfer Account
  - Debit: $5,000
```

**System Auto-Creates Payment 2:**
```
Journal: Petty Cash
Reference: CASH/2025/0001

Move Lines:
Line 1:
  - Account: 1020 - Petty Cash
  - Debit: $5,000
  
Line 2:
  - Account: 1050 - Internal Transfer Account
  - Credit: $5,000
```

#### Step 4: Result

**Account Balances:**
- Main Bank (1010): -$5,000
- Petty Cash (1020): +$5,000
- Transfer Account (1050): $0 (balanced)

**Both payments are:**
- ✅ Posted automatically
- ✅ Linked together
- ✅ Using centralized transfer account

---

## Benefits

### 1. **Centralized Tracking**
All internal transfers go through one account, making it easy to track all fund movements.

### 2. **Simplified Reconciliation**
The transfer account debits and credits should always balance to zero.

### 3. **Clear Audit Trail**
Easy to see all internal transfers by checking the transfer account's journal items.

### 4. **Flexible Configuration**
Different companies can use different transfer accounts.

### 5. **Automatic Balancing**
Paired payments automatically balance the transfer account.

---

## Reports and Analysis

### View Transfer Account Activity

**Method 1: Account Report**
1. Go to **Accounting** → **Reporting** → **General Ledger**
2. Filter by account: Internal Transfer Account
3. View all internal transfer movements

**Method 2: Journal Items**
1. Go to **Accounting** → **Accounting** → **Journal Items**
2. Filter: Account = Internal Transfer Account
3. Group by: Partner or Journal

**Expected Balance:**
The transfer account should always have a **zero balance** (or close to zero) because:
- Each outbound transfer creates a debit
- Each inbound transfer creates a credit
- Paired payments balance each other

---

## Troubleshooting

### Issue: Transfer Account Not Configured

**Error:** Internal transfers create entries but don't use transfer account

**Solution:**
1. Go to Settings → Accounting
2. Set the Internal Transfer Account field
3. Save settings
4. Try creating a new internal transfer

### Issue: Transfer Account Has Non-Zero Balance

**Cause:** Unpaired or incomplete transfers

**Solution:**
1. Check for draft or cancelled payments
2. Verify all internal transfers have paired payments
3. Review journal items for the transfer account
4. Reconcile any outstanding items

### Issue: Cannot Find Transfer Account Setting

**Solution:**
1. Ensure module is installed and updated
2. Refresh browser cache
3. Check user has accounting manager rights
4. Go to Settings → Accounting → scroll down

---

## Best Practices

### 1. **Choose Appropriate Account**
- Use a dedicated account for internal transfers
- Don't use operational accounts
- Account should be of type "Current Assets" or similar

### 2. **Regular Reconciliation**
- Check transfer account balance monthly
- Should always be zero or near zero
- Investigate any persistent balances

### 3. **Naming Convention**
- Name account clearly: "Internal Transfer Account" or "Inter-Journal Transfer"
- Makes it easy to identify in reports

### 4. **Documentation**
- Document which account is used for transfers
- Include in accounting procedures manual
- Train staff on internal transfer process

### 5. **Monitoring**
- Set up alerts if transfer account balance exceeds threshold
- Review transfer account regularly
- Ensure all transfers are completed

---

## Migration Notes

### Upgrading from Previous Version

If you're upgrading from a version without the transfer account feature:

1. **Install/Update Module**
   ```bash
   ./odoo-bin -u ibs_accounting_internal_transfer -d your_database
   ```

2. **Configure Transfer Account**
   - Go to Settings → Accounting
   - Set Internal Transfer Account
   - Save

3. **Test**
   - Create a test internal transfer
   - Verify journal entries use transfer account
   - Check paired payment is created correctly

4. **Historical Data**
   - Old transfers won't be affected
   - Only new transfers use the transfer account
   - No data migration needed

---

## Version History

- **v1.2**: Added company transfer account usage
  - Uses existing `transfer_account_id` from `check_management` module
  - Override `_prepare_move_line_default_vals`
  - Added dependency on `check_management`
  
- **v1.1**: Enhanced journal and account handling
  
- **v1.0**: Initial release

---

## Support

For questions or issues:
- Review this guide
- Check README.md for basic usage
- Review FLOW_DIAGRAM.md for visual explanation
- Contact your system administrator

