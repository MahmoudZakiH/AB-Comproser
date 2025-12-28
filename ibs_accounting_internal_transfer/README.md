# IBS Accounting Internal Transfer

## Overview
This module adds internal transfer functionality between bank and cash journals in Odoo, allowing seamless fund transfers within the same company.

## Features

### Internal Transfer Functionality

This feature allows you to transfer funds between different bank and cash journals within the same company. When you create an internal transfer payment, the system automatically creates a corresponding opposite payment.

#### How It Works:

1. **Create Internal Transfer**:
   - Go to Accounting/Invoicing → Customers/Vendors → Payments
   - Click "New"
   - Enable the "Internal Transfer" toggle
   - Select payment type (Send Money/Receive Money)
   - Choose the source journal
   - Select the destination journal from the dropdown (only bank/cash journals are shown)
   - Enter the amount and date
   - Click "Confirm"

2. **Automatic Paired Payment Creation**:
   - When you confirm an internal transfer, the system automatically creates a paired payment:
     - If original is "Send Money" (outbound), paired will be "Receive Money" (inbound)
     - If original is "Receive Money" (inbound), paired will be "Send Money" (outbound)
   - The journals are swapped:
     - Original destination journal becomes the paired payment's source journal
     - Original source journal becomes the paired payment's destination journal
   - Both payments are linked together via the "Paired Transfer Payment" field

3. **Key Features**:
   - Partner field is hidden for internal transfers (not needed)
   - Destination journal is required when internal transfer is enabled
   - Source and destination journals must be different
   - Both payments are automatically posted
   - Canceling one payment will cancel the paired payment
   - Filter available to show only internal transfers

#### Example:

**Scenario**: Transfer $1,000 from Bank A to Bank B

1. Create Payment:
   - Payment Type: Send Money
   - Internal Transfer: Yes
   - Journal: Bank A
   - Destination Journal: Bank B
   - Amount: $1,000

2. System automatically creates:
   - Payment Type: Receive Money
   - Internal Transfer: Yes
   - Journal: Bank B
   - Destination Journal: Bank A
   - Amount: $1,000

## Installation

1. Copy this module to your Odoo addons directory
2. Update the apps list
3. Install "IBS Accounting Internal Transfer"

## Dependencies

- account (Odoo Accounting/Invoicing module)

## Technical Details

### New Fields:
- `is_internal_transfer` (Boolean): Marks a payment as an internal transfer
- `destination_journal_id` (Many2one): The destination journal for the transfer
- `paired_internal_transfer_payment_id` (Many2one): Links to the automatically created paired payment

### Modified Methods:
- `action_post()`: Creates the paired payment when confirming an internal transfer
- `action_draft()`: Validates that paired payment is also in draft before allowing
- `action_cancel()`: Automatically cancels the paired payment

## Version History

- **v1.0**: Initial release with internal transfer functionality

## Author
IBS

## License
LGPL-3

## Support

For support or questions, please contact your system administrator.

## Credits

Based on the functionality from wm_accounting_internal_transfer module.

