# Internal Transfer Flow Diagram

## Visual Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER CREATES PAYMENT                          │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ Payment Form                                            │    │
│  │ ─────────────                                           │    │
│  │ [ ] Internal Transfer  ← Toggle ON                      │    │
│  │                                                          │    │
│  │ Payment Type: [Send Money ▼]                            │    │
│  │ Journal:      [Bank A ▼]                                │    │
│  │ Destination:  [Bank B ▼]  ← Shows when toggle is ON    │    │
│  │ Amount:       $1,000                                     │    │
│  │                                                          │    │
│  │ Partner: (hidden for internal transfer)                 │    │
│  │                                                          │    │
│  │              [Confirm Button]                            │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ User clicks Confirm
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    action_post() TRIGGERED                       │
│                                                                  │
│  1. Super().action_post() - Posts the original payment          │
│  2. Checks: is_internal_transfer == True?                       │
│  3. Checks: paired_payment already exists?                      │
│  4. If NO → Call _create_paired_internal_transfer()             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│           _create_paired_internal_transfer()                     │
│                                                                  │
│  Step 1: Determine opposite payment type                        │
│  ┌──────────────────────────────────────────────────┐          │
│  │ IF original = 'outbound' → new = 'inbound'       │          │
│  │ IF original = 'inbound'  → new = 'outbound'      │          │
│  └──────────────────────────────────────────────────┘          │
│                                                                  │
│  Step 2: Swap journals                                          │
│  ┌──────────────────────────────────────────────────┐          │
│  │ Original journal_id → Paired destination_journal │          │
│  │ Original destination → Paired journal_id         │          │
│  └──────────────────────────────────────────────────┘          │
│                                                                  │
│  Step 3: Create payment with swapped values                     │
│  Step 4: Link both payments together                            │
│  Step 5: Auto-post the paired payment                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RESULT: TWO PAYMENTS                        │
│                                                                  │
│  ┌─────────────────────────────┐  ┌─────────────────────────┐  │
│  │ PAYMENT 1 (Original)        │  │ PAYMENT 2 (Auto-created)│  │
│  │ ─────────────────────        │  │ ────────────────────────│  │
│  │ Type: Send Money (outbound) │  │ Type: Receive Money     │  │
│  │ Journal: Bank A             │  │ Journal: Bank B         │  │
│  │ Destination: Bank B         │  │ Destination: Bank A     │  │
│  │ Amount: $1,000              │  │ Amount: $1,000          │  │
│  │ State: Posted               │  │ State: Posted           │  │
│  │ Paired Payment: → Payment 2 │  │ Paired Payment: → Pay 1 │  │
│  └─────────────────────────────┘  └─────────────────────────┘  │
│              │                              │                    │
│              └──────────────┬───────────────┘                    │
│                             │                                    │
│                    Both Linked Together                          │
└─────────────────────────────────────────────────────────────────┘
```

## Example Scenarios

### Scenario 1: Transfer from Bank to Cash

**User Input:**
```
Internal Transfer: YES
Payment Type: Send Money
Journal: Main Bank
Destination: Cash Register
Amount: $500
```

**System Creates:**

Payment 1 (Original):
- Type: Outbound (Send Money)
- From: Main Bank
- To: Cash Register
- Amount: $500
- Effect: Decreases Main Bank balance

Payment 2 (Auto-created):
- Type: Inbound (Receive Money)
- From: Cash Register (swapped)
- To: Main Bank (swapped)
- Amount: $500
- Effect: Increases Cash Register balance

**Net Result:** $500 moved from Main Bank to Cash Register

---

### Scenario 2: Transfer from Cash to Bank

**User Input:**
```
Internal Transfer: YES
Payment Type: Receive Money
Journal: Main Bank
Destination: Cash Register
Amount: $300
```

**System Creates:**

Payment 1 (Original):
- Type: Inbound (Receive Money)
- From: Main Bank
- To: Cash Register
- Amount: $300
- Effect: Increases Main Bank balance

Payment 2 (Auto-created):
- Type: Outbound (Send Money)
- From: Cash Register (swapped)
- To: Main Bank (swapped)
- Amount: $300
- Effect: Decreases Cash Register balance

**Net Result:** $300 moved from Cash Register to Main Bank

---

## State Management Flow

```
┌──────────────┐
│   DRAFT      │
│              │
└──────┬───────┘
       │ Confirm
       ▼
┌──────────────┐      ┌─────────────────────────────────┐
│   POSTED     │◄─────┤ Paired Payment Also Created     │
│              │      │ and Posted Automatically        │
└──────┬───────┘      └─────────────────────────────────┘
       │
       │ Cancel
       ▼
┌──────────────┐      ┌─────────────────────────────────┐
│  CANCELLED   │◄─────┤ Paired Payment Also Cancelled   │
│              │      │ Automatically                   │
└──────────────┘      └─────────────────────────────────┘
```

## Journal Entry Impact

When both payments are posted, journal entries are created:

**Payment 1 (Send from Bank A to Bank B):**
```
Debit  | Credit | Account
-------|--------|------------------
       | 1,000  | Bank A (Asset)
1,000  |        | Outstanding Payment
```

**Payment 2 (Receive at Bank B from Bank A):**
```
Debit  | Credit | Account
-------|--------|------------------
1,000  |        | Bank B (Asset)
       | 1,000  | Outstanding Receipt
```

**Net Effect:**
- Bank A balance: -$1,000
- Bank B balance: +$1,000
- Total company assets: No change (internal transfer)

