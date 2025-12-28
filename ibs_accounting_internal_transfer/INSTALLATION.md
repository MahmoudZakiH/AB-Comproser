# Installation Guide - IBS Accounting Internal Transfer

## Module Information

- **Technical Name**: `ibs_accounting_internal_transfer`
- **Module Name**: IBS Accounting Internal Transfer
- **Version**: 1.0
- **Author**: IBS
- **Category**: Accounting
- **License**: LGPL-3
- **Dependencies**: `account` (Odoo Accounting/Invoicing)

## Installation Steps

### Step 1: Module Location

The module is already in your addons directory:
```
/home/ayman/odoo-dev/sh/egy_marble16/ibs_accounting_internal_transfer/
```

### Step 2: Update Apps List

1. Login to Odoo as Administrator
2. Go to **Apps** menu
3. Click **Update Apps List** (you may need to enable Developer Mode first)
4. Confirm the update

### Step 3: Install the Module

1. In the **Apps** menu, remove the "Apps" filter to see all modules
2. Search for "IBS Accounting Internal Transfer"
3. Click on the module
4. Click **Install** button

### Step 4: Verify Installation

After installation, verify the module is working:

1. Go to **Accounting** → **Customers** → **Payments**
2. Click **New**
3. You should see a new **Internal Transfer** toggle field after Payment Type
4. Enable the toggle and verify:
   - Partner field is hidden
   - Destination Journal field appears
   - Only bank/cash journals are shown in Destination Journal

## What This Module Does

### Features Added:

1. **Internal Transfer Toggle**: Boolean field to mark payments as internal transfers
2. **Destination Journal**: Select the destination journal for the transfer
3. **Automatic Paired Payment**: Creates opposite payment automatically when confirmed
4. **Journal Swapping**: Source and destination journals are swapped in the paired payment
5. **Payment Type Reversal**: Send becomes Receive and vice versa
6. **Search Filter**: Filter to show only internal transfers

### How It Works:

When you create a payment with "Internal Transfer" enabled and confirm it:

**Example: Transfer $1,000 from Bank A to Bank B**

**You create:**
- Payment Type: Send Money
- Journal: Bank A
- Destination: Bank B
- Amount: $1,000

**System automatically creates:**
- Payment Type: Receive Money
- Journal: Bank B (swapped)
- Destination: Bank A (swapped)
- Amount: $1,000

Both payments are linked and posted automatically.

## Troubleshooting

### Issue: Module not found in Apps list

**Solution:**
- Make sure you updated the apps list
- Check that Developer Mode is enabled
- Verify the module folder exists in the addons path

### Issue: Installation fails

**Solution:**
- Check the Odoo logs for detailed error messages
- Ensure the `account` module is installed
- Verify all Python files have correct syntax

### Issue: Views not showing correctly

**Solution:**
- Clear browser cache
- Restart Odoo server
- Update the module again

## Uninstallation

If you need to uninstall the module:

1. Go to **Apps**
2. Search for "IBS Accounting Internal Transfer"
3. Click **Uninstall**

**Note**: Uninstalling will remove the custom fields and any internal transfer payments created with this module may lose their special functionality.

## Module Structure

```
ibs_accounting_internal_transfer/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── account_payment.py
├── views/
│   └── account_payment_views.xml
├── README.md
├── FLOW_DIAGRAM.md
└── INSTALLATION.md (this file)
```

## Support

For technical support or questions:
- Review the README.md for usage instructions
- Check FLOW_DIAGRAM.md for visual flow explanation
- Contact your system administrator
- Review Odoo logs at `/var/log/odoo/odoo-server.log`

## Related Modules

This module is separate from `short_code_customization` which only handles journal short code field size customization.

## Credits

Based on the functionality from the wm_accounting_internal_transfer module available on Odoo Apps Store.

