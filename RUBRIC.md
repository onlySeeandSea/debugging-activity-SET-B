# Debugging Activity: Rubric (40 points)

This rubric applies to **SET A, SET B and SET C**.

## Summary

| # | Criterion | Points |
|---|-----------|:------:|
| 1 | Error-free execution | 8 |
| 2 | Logic correctness (per task) | 12 |
| 3 | Final answer | 6 |
| 4 | Bug report | 10 |
| 5 | Code integrity | 4 |
|   | **TOTAL** | **40** |

---

## 1. Error-free execution (8 pts)

The program runs from start to finish with **no crash**: no
`SyntaxError`, `NameError`, `TypeError`, `ValueError`, `KeyError`,
`IndexError`, `AttributeError`, or `ModuleNotFoundError`.

| Points | Description |
|:------:|-------------|
| 8 | Program runs to the end with no errors. |
| 6 | Program crashes on **1** remaining error. |
| 4 | Program crashes; **2–3** crashing bugs remain. |
| 2 | At least one crashing bug fixed, but **4 or more** remain. |
| 0 | No crashing bug fixed. |

## 2. Logic correctness (12 pts, 3 per task)

Each task's output follows its **RULES** and meets its **CHECKPOINT**.
Silent (non-crashing) bugs count here.

| Points per task | Description |
|:------:|-------------|
| 3 | Output fully follows the task's rules and checkpoint. |
| 2 | Mostly correct; one rule still violated (e.g. a value is negative when it should be positive). |
| 1 | Task runs but its output is clearly wrong. |
| 0 | Task does not run or was removed/bypassed. |

| Task 1 | Task 2 | Task 3 | Task 4 |
|:------:|:------:|:------:|:------:|
| /3 | /3 | /3 | /3 |

## 3. Final answer (6 pts)

| Points | Description |
|:------:|-------------|
| 6 | Final answer is **exactly** correct, is produced by the student's own code when the teacher runs it, and the submitted QR code scans to that same answer. |
| 3 | Correct format, but **one** part of the answer is wrong, **or** the answer is right but the QR code is missing or won't scan. |
| 1 | An answer is printed, but **two or more** parts are wrong. |
| 0 | No final answer, or the answer is hard-coded. |

## 4. Bug report (10 pts)

Each fixed bug is documented with: **line number, error type, error
message/symptom, cause (why it happened), and the fix**.

| Points | Description |
|:------:|-------------|
| 9–10 | **All** fixed bugs documented. Causes are explained in the student's own words and connect to the lesson concept (e.g. "`or` doesn't repeat the comparison", "a tuple is immutable"). Silent bugs include **how they were detected** (which rule/checkpoint failed). |
| 6–8 | Most bugs documented with correct types and fixes; some causes are vague or missing. |
| 3–5 | Few bugs documented, or entries list only the fix without the cause. |
| 1–2 | Report is incomplete or mostly copied error messages. |
| 0 | No bug report. |

## 5. Code integrity (4 pts)

| Points | Description |
|:------:|-------------|
| 4 | Fixes are minimal and targeted. No tasks deleted, no data changed (except fixing a wrong data type), no hard-coded results. |
| 2–3 | Works, but with unnecessary rewrites or minor changes to the data. |
| 0–1 | Tasks deleted or commented out, data altered to force results, or values hard-coded. |

---

### Automatic deductions

- **Hard-coded final answer or checkpoint values:** 0 for criteria 2 and 3.
- **Identical bug reports between students:** both reports get 0 for criterion 4.

### Score sheet

| Student | Set | C1 /8 | C2 /12 | C3 /6 | C4 /10 | C5 /4 | **Total /40** |
|---------|:---:|:-----:|:------:|:-----:|:------:|:-----:|:-------------:|
|         |     |       |        |       |        |       |               |
