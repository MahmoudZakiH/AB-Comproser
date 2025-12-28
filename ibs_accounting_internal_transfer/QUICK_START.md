# Quick Start Guide - IBS Accounting Internal Transfer

## Installation (2 minutes)

1. **Update Apps List**: Apps → Update Apps List
2. **Install Module**: Search "IBS Accounting Internal Transfer" → Install
3. **Done!** ✅

## How to Use (30 seconds)

### Create Internal Transfer

1. Go to: **Accounting → Customers → Payments**
2. Click: **New**
3. Enable: **Internal Transfer** toggle
4. Select:
   - **Payment Type**: Send Money or Receive Money
   - **Journal**: Source journal (e.g., Bank A)
   - **Destination Journal**: Target journal (e.g., Bank B)
   - **Amount**: Transfer amount
5. Click: **Confirm**

**That's it!** The system automatically creates the paired payment.

## Example

### Transfer $1,000 from Bank to Cash

**You create:**
```
Internal Transfer: ✓ ON
Payment Type: Send Money
Journal: Main Bank
Destination: Cash Register
Amount: $1,000
```

**System creates automatically:**
```
Payment Type: Receive Money
Journal: Cash Register
Destination: Main Bank
Amount: $1,000
```

**Result**: $1,000 moved from Main Bank to Cash Register

## Key Points

✅ **Partner field is hidden** - Not needed for internal transfers  
✅ **Both payments are linked** - Via "Paired Transfer Payment" field  
✅ **Both are auto-posted** - No need to confirm twice  
✅ **Cancel one = cancel both** - Keeps data consistent  
✅ **Filter available** - Search → "Internal Transfers"  

## Validation Rules

❌ **Source = Destination** → Error: Must be different journals  
❌ **No destination selected** → Error: Destination required  
❌ **Non-bank/cash journal** → Not shown in dropdown  

## View Your Transfers

**List View**: Accounting → Customers → Payments → Filter: "Internal Transfers"

**Paired Payment**: Open any internal transfer → See "Paired Transfer Payment" field

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Toggle not showing | Update module / Clear cache |
| Can't select journal | Only bank/cash journals allowed |
| Paired payment not created | Check Odoo logs for errors |
| Partner field still showing | Disable Internal Transfer toggle |

## Technical Details

**Module Name**: `ibs_accounting_internal_transfer`  
**Version**: 1.0  
**Dependencies**: `account`  
**License**: LGPL-3  

## Need More Info?

- **Usage Guide**: See `README.md`
- **Technical Flow**: See `FLOW_DIAGRAM.md`
- **Installation Details**: See `INSTALLATION.md`
- **Complete Summary**: See `SUMMARY.md`

## Support

Contact your system administrator or review the Odoo logs at:
```
/var/log/odoo/odoo-server.log
```

---

**Happy Transferring! 💸**

