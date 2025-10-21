# Password Strength Checker (Beginner-Friendly Cybersecurity Project)

**Goal:** Help absolute beginners build their **first Python security script** in under an hour — and learn how to evaluate password quality with simple, practical rules.

## What this tool does
- Rates a password as **Weak / Moderate / Strong / Very Strong**
- Explains **WHY** (length, variety, dictionary words, sequences, repeats)
- Suggests **concrete fixes** (e.g., “add symbols”, “use 12+ chars”, “avoid ‘12345’”)
- No external libraries, single file, easy to read

## Why this matters (real-world relevance)
- Strong passwords reduce account takeover risk and brute-force success.
- Shows basic **regex**, **logic**, and **security hygiene** — great first step in cyber.

---

## Quick start

```bash
# 1) Clone
git clone https://github.com/<your-username>/password-strength-checker.git
cd password-strength-checker

# 2) Run (Python 3.8+)
python password_strength_checker.py "Sup3r$ecret!"
# or:
python password_strength_checker.py
# (then type your password when prompted)
