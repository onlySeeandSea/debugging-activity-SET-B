# SET B: The Ghost Withdrawal  (Section B)

The campus credit cooperative's official report says one account has
**less money than it should**. Someone made a "ghost withdrawal". The audit
program that should expose it is broken.

Your job: **fix the program**, solve the puzzle, and submit the **FINAL ANSWER**.

## The 4 tasks

The program has 4 tasks. Each task's result is used by the next one, so
you only get the correct FINAL ANSWER if **every** bug is fixed.

1. **Task 1: Clean the Spreadsheet Export.** Fix messy IDs, types and amounts.
2. **Task 2: Replay the Ledger.** Apply every deposit and withdrawal.
3. **Task 3: Account Summary.** Show each account's balance.
4. **Task 4: Expose the Ghost Withdrawal.** Compare with the official report and save the FINAL ANSWER as a QR code.

**You will need:** dictionaries and lists, `for` loops, `if`/`elif`/`else`, string methods, type casting (`int` vs `float`), multiple assignment, logical operators (`and`/`or`), f-strings, comments, `input()`, the `qrcode` module.

## How to work

1. **RUN the program first.** Don't read the whole thing looking for bugs.
   Open a terminal **in this folder** and run:
   ```
   python main.py
   ```
2. **Read the error message.** It tells you the error **type**
   (`SyntaxError`, `TypeError`, `NameError`, ...), the **line number**,
   and a short reason.
3. **FIX only that bug**, then **RUN again.** One bug at a time.
4. **Watch out for silent bugs.** Some bugs do **not** crash the program;
   they just give **wrong results**. Each task in `main.py` has
   **RULES** (what the code should do) and a **CHECKPOINT** (what a correct
   result looks like). If the output breaks a rule or fails a checkpoint,
   there is still a bug.
5. **Some bugs hide behind other bugs.** Fixing one can reveal another.
   That's normal; keep going.
6. **Log every bug** in your Bug Report as you fix it
   ([BUG_REPORT_TEMPLATE.md](../BUG_REPORT_TEMPLATE.md)).

## Tips

- The program asks for your **name**. Type it each time you run it.

## Rules

- Do **not** delete tasks, comment out code, or hard-code an answer.
  Fix the code so it **computes** the right answer.
- Do **not** change the data unless it is stored with the **wrong data type**.
- Fixes are small. Most bugs need only **one line** changed.
- Do **not** edit `qrcode.py`. It has no bugs. All the bugs are in `main.py`.
- Everything works **offline**. Nothing needs to be installed.

## What to submit

1. Your fixed `main.py`
2. Your completed **Bug Report**
3. The **FINAL ANSWER** printed by your program
4. The QR code image your program saves: `SET-B-final-answer.png`
   (scan it with your phone camera; it works offline and must show your FINAL ANSWER)

Grading: [RUBRIC.md](../RUBRIC.md) (40 points)
