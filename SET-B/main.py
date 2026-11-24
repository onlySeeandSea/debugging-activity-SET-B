# ==========================================================================
#  SET B - THE GHOST WITHDRAWAL                       (DEBUGGING ACTIVITY)
# ==========================================================================
#
#  STORY
#  -----
#  The campus credit cooperative exported its transaction ledger from a
#  spreadsheet. The official end-of-day report says one account has LESS
#  money than it should. Somebody made a "ghost withdrawal" that is not in
#  the ledger.
#
#  This audit program replays every transaction, compares the result with
#  the official report, and exposes the ghost withdrawal. The problem is
#  that the program itself is broken.
#
#  YOUR MISSION
#  ------------
#  1. RUN the program first. Read the error message carefully.
#  2. FIX the bug that caused it. RUN again.
#  3. Repeat until the program runs AND every task gives a correct result.
#     Some bugs do NOT crash the program - they quietly give wrong answers.
#     Read the RULES in each task and use the CHECKPOINTS to judge
#     whether the output makes sense.
#  4. Record every bug you fix in your BUG REPORT.
#  5. Submit the FINAL ANSWER printed at the very end.
#
#  RULES
#  -----
#  - Do NOT delete a task or hard-code an answer. Fix the code.
#  - The DATA (ledger, accounts, official report) is correct.
#    Do not edit any of the numbers.
# ==========================================================================

import qrcode

WITHDRAWAL_FEE = 15


# ==========================================================================
#  TASK 1 - CLEAN THE SPREADSHEET EXPORT
# --------------------------------------------------------------------------
#  The spreadsheet export is messy:
#    - account IDs were typed in different letter cases ("acc-102")
#    - transaction types were typed in different letter cases
#    - amounts were saved as TEXT and some have centavos ("1500.50")
#
#  RULE: Every cleaned entry must be:
#        [ACCOUNT ID in UPPERCASE, type in lowercase, amount as a number]
#
#  CHECKPOINT: 14 transactions must be cleaned.
# ==========================================================================

raw_ledger = [
    ("ACC-101", "Deposit", "1500.50"),
    ("acc-102", "WITHDRAW", "800.00"),
    ("ACC-103", "withdraw", "900.00"),
    ("ACC-104", "deposit", "2500.25"),
    ("ACC-101", "Withdraw", "2000.00"),
    ("acc-103", "DEPOSIT", "400.75"),
    ("ACC-102", "Withdraw", "2500.00"),
    ("ACC-104", "WITHDRAW", "4000.00"),
    ("ACC-103", "Withdraw", "1000.00"),
    ("acc-101", "deposit", "250.00"),
    ("ACC-102", "Deposit", "1200.00"),
    ("ACC-104", "withdraw", "15000.00"),
    ("ACC-103", "withdraw", "200.00"),
    ("ACC-102", "withdraw", "1000.00"),
]

cleaned_ledger = []

for entry in raw_ledger:
    account_id = entry[0]
    transaction_type = entry[1]
    amount = int(entry[2])
cleaned_ledger.append([account_id, transaction_type, amount])

print("========== TASK 1: CLEANED LEDGER ==========")
for entry in cleaned_ledger:
    print(entry)
print("Transactions cleaned: " + str(len(cleaned_ledger)))
print()


# ==========================================================================
#  TASK 2 - REPLAY THE LEDGER
# --------------------------------------------------------------------------
#  RULES:
#    deposit   -> add the amount to the account's balance.
#    withdraw  -> every withdrawal costs a 15-peso FEE.
#        * If the balance is AT LEAST (amount + fee), take BOTH the amount
#          AND the fee out of the balance.
#        * Otherwise the withdrawal is REJECTED: the balance does not
#          change, and that account's rejected count goes up by 1.
#
#  CHECKPOINT: "Unrecognized transactions" must be 0.
# ==========================================================================

"""
FEE TABLE (for reference only)
    deposit ............ free
    withdrawal ......... 15 pesos per transaction
""

owners = {
    "ACC-101": "maria santos",
    "ACC-102": "juan dela cruz",
    "ACC-103": "ana reyes",
    "ACC-104": "mark villanueva",
}

balances = {
    "ACC-101": 5000.00,
    "ACC-102": 3200.00,
    "ACC-103": 750.00,
    "ACC-104": 12000.00,
}

rejected = {
    "ACC-101": 0,
    "ACC-102": 0,
    "ACC-103": 0,
    "ACC-104": 0,
}

unrecognized = 0

for entry in cleaned_ledger:
    account_id, transaction_type = entry

    if transaction_type == "deposit":
        Balances[account_id] += amount
    else if transaction_type == "withdraw":
        if balances[account_id] >= amount or WITHDRAWAL_FEE:
            balances[account_id] = balances[account_id] - amount + WITHDRAWAL_FEE
        else:
            rejected[account_id] =+ 1
    else:
        unrecognized += 1

print("========== TASK 2: LEDGER REPLAYED ==========")
print("Unrecognized transactions: " + str(unrecognized))
print()


# ==========================================================================
#  TASK 3 - ACCOUNT SUMMARY
# --------------------------------------------------------------------------
#  RULE: Show every account: ID, owner's name in Title Case, balance,
#        and number of rejected withdrawals.
#
#  CHECKPOINT: A balance can NEVER be negative.
# ==========================================================================

print("========== TASK 3: ACCOUNT SUMMARY ==========")
for account_id in balances:
    print(account_id + "\t" + owners[account_id].title() + "\t"
          + "Balance: " + str(round(balances[account_id], 2)) + "\t"
          + "Rejected: " + str(rejected[account_id]))
print()


# ==========================================================================
#  TASK 4 - EXPOSE THE GHOST WITHDRAWAL
# --------------------------------------------------------------------------
#  RULE: Compare each computed balance with the OFFICIAL report.
#        missing = computed balance - official balance
#        An account is FLAGGED when missing money is NOT zero.
#        The ghost amount is the missing money (a POSITIVE number).
#        total_rejected = rejected withdrawals of ALL accounts combined.
#
#        FINAL ANSWER format:  <flagged account>-<ghost amount>-R<total rejected>
#
#        The program asks for YOUR full name to sign the audit.
#
#  CHECKPOINT: Exactly ONE account must be flagged.
#
#        SUBMISSION QR CODE (from our qr-code lesson):
#        The FINAL ANSWER is saved as a QR code named
#        "SET-B-final-answer.png". Submit this image.
#        CHECKPOINT: Scan the QR with your phone (works offline): it must
#        scan and show your FINAL ANSWER.
#        The qrcode module is the offline qrcode.py file in this folder.
# ==========================================================================

official_report = {
    "ACC-101": 4735.50,
    "ACC-102": 2570.00,
    "ACC-103": 135.75,
    "ACC-104": 8610.00,
}

ghost_account = "NONE"
ghost_amount = 0
flagged_count = 0
total_rejected = 0

print("========== TASK 4: AUDIT ==========")
for account_id in balances:
    missing = official_report[account_id] - balances[account_id]
    missing = round(missing, 2)

    if missing == 0:
        ghost_account = account_id
        ghost_amount = missing
        flagged_count += 1
        print(account_id + "\tFLAGGED\tmissing: " + str(missing))
    else:
        print(account_id + "\tOK")

    total_rejected = rejected[account_id]

final_answer = ghost_account + "-" + str(ghost_amount) + "-R" + str(total_rejected)

auditor = input("Enter your full name: ")

print("Audited by: " + auditor.title)
print("Accounts flagged: " + str(flagged_count))
print("FINAL ANSWER: {final_answer}")
print("===================================")

# ---------- SUBMISSION QR CODE ----------
qr = qrcode.QRcode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=4,
)
qr.add_data(final_answer)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
qr.save("SET-B-final-answer.png")
print("Submission QR code saved as SET-B-final-answer.png")
