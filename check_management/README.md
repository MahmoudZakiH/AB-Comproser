# IBS Check Management

## Overview
This module provides comprehensive check (cheque) management functionality for Odoo, allowing businesses to track, manage, and process checks from receipt to final disposition.

## Features

### 1. Check Management
- **Location**: Accounting → Checks
- **Capabilities**:
  - Create and manage payment checks
  - Track check lines with detailed information
  - Support for inbound (received) and outbound (sent) checks
  - Internal transfer checks

### 2. Check States
Checks can be in multiple states throughout their lifecycle:
- **Holding**: Check is received but not yet deposited
- **Deposited**: Check has been deposited to the bank
- **To Vendor**: Check is prepared to be paid to a vendor
- **Paid Vendor**: Check has been paid to a vendor
- **Accepted**: Check has been accepted by the bank
- **Rejected**: Check has been rejected by the bank
- **Closed**: Check processing is complete
- **Returned**: Check has been returned
- **Cancelled**: Check has been cancelled
- **Complete Transfer**: Internal transfer is complete

### 3. Check Operations

#### Bank Operations (Wizards):
1. **Deposit Check** (`check.depoiset`)
   - Deposit checks to the bank
   - Select journal and account for deposit

2. **Accept Check** (`check.accept`)
   - Mark checks as accepted by the bank
   - Generate accounting entries

3. **Reject Check** (`check.reject`)
   - Handle rejected checks
   - Add rejection notes
   - Create reversal entries

4. **Deduct Check** (`check.deduct`)
   - Process check deductions
   - Handle bank charges

5. **Cash Check** (`check.cash`)
   - Convert checks to cash
   - Generate cash journal entries

6. **Transfer Deduct** (`transfer.deduct`)
   - Handle deductions on transfer checks

### 4. Partial Collections
- **Model**: `partial.collection`
- **Wizard**: `partial.collection.wizard`
- **Features**:
  - Collect partial amounts from checks
  - Track remaining balance
  - Automatic history logging
  - Validation to prevent over-collection

### 5. Check History
- **Model**: `check.history`
- **Features**:
  - Automatic tracking of all check state changes
  - Records creation, modifications, and state transitions
  - Timestamped audit trail
  - Linked to original check records

### 6. Check Line Details
Each check line includes:
- Check Number (required)
- Check Date (required)
- Check Amount (required)
- Bank Name and Branch
- Partner Information
- Account Owner
- With Drawer Name
- Currency support with automatic conversion
- Mozahar (مظهر) and Mosatar (مسطر) flags
- Invoice linkage

### 7. Integration with Accounting
- Automatic journal entry creation
- Integration with account.payment
- Support for multiple journals
- Reconciliation support
- Multi-currency support

## Models

### Main Models (Persistent):
1. **payment.check** - Main check container
2. **payment.check.line** - Individual check records
3. **check.history** - Audit trail for checks
4. **partial.collection** - Partial collection records

### Wizard Models (Transient):
1. **partial.collection.wizard** - Partial collection wizard
2. **check.depoiset** - Deposit wizard
3. **check.accept** - Accept wizard
4. **check.reject** - Reject wizard
5. **check.deduct** - Deduct wizard
6. **check.cash** - Cash wizard
7. **transfer.deduct** - Transfer deduct wizard

## Installation
1. Copy the module to your Odoo addons directory
2. Update the apps list
3. Install the module from Apps menu

## Configuration
1. Navigate to Accounting → Configuration → Journals
2. Configure check journals with appropriate accounts
3. Set up default accounts for check operations

## Usage

### Receiving a Check:
1. Create a payment with payment method "Check"
2. Add check details (number, date, amount, bank)
3. Check will be in "Holding" state
4. Use "Deposit" button to deposit to bank
5. Use "Accept" or "Reject" buttons based on bank response

### Paying with a Check:
1. Create a vendor payment with payment method "Check"
2. Add check details
3. Check will be marked as "To Vendor"
4. Mark as "Paid Vendor" when delivered

### Partial Collections:
1. Open a check in holding state
2. Click "Partial Collection" button
3. Enter partial amount and journals
4. System tracks remaining balance automatically

### Check History:
1. Open any check record
2. Click "Check History" smart button
3. View complete audit trail

## Security
Access rights configured for:
- **Account User**: Full access to all check operations
- **Account Manager**: Full access to all check operations

## Dependencies
- base
- account

## Technical Details
- **Version**: 18.0
- **Category**: Accounting
- **Author**: IBS
- **Website**: https://www.ibs-egy.com

## Support
For support and inquiries, please contact IBS at https://www.ibs-egy.com

## License
Proprietary

## Changelog

### Version 18.0
- Initial release for Odoo 18
- Complete check lifecycle management
- Multi-currency support
- Partial collection functionality
- Comprehensive audit trail
- Arabic language support for specific fields

