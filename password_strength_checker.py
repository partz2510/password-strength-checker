#!/usr/bin/env python3
"""
Password Strength Checker
- Rates a password: Weak / Moderate / Strong / Very Strong
- Explains WHY and gives concrete fixes
- Beginner-friendly: single file, no external deps
"""

import re
import math
import sys

# Minimal common word list + obvious patterns (expandable)
COMMON_WORDS = {
    "password","welcome","qwerty","admin","letmein","dragon","monkey","login",
    "abc123","iloveyou","sunshine","football","baseball","princess","123456",
    "1234567","12345678","123456789","1234567890","111111","000000","1q2w3e",
    "passw0rd","p@ssw0rd","p4ssw0rd"
}

# Simple keyboard / numeric sequences to catch
SEQUENCES = [
    "12345", "23456", "34567", "45678", "56789", "67890",
    "qwerty", "asdf", "zxcv", "qwert", "abcde"
]

def estimate_entropy(password: str) -> float:
    """Very rough entropy estimate based on character set size and length."""
    if not password:
        return 0.0
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"\d", password):     charset += 10
    if re.search(r"[^\w]", password):  charset += 33  # symbols (approx)
    # H ~ L * log2(charset)
    return len(password) * math.log2(max(charset, 1))

def has_repeated_runs(password: str, max_run: int = 3) -> bool:
    """Detect long repeated characters like 'aaaa' or '1111'."""
    return re.search(r"(.)\1{" + str(max_run) + r",}", password) is not None

def contains_dictionary_word(password: str) -> bool:
    p = password.lower()
    for w in COMMON_WORDS:
        if w in p:
            return True
    return False

def contains_sequence(password: str) -> bool:
    p = password.lower()
    return any(seq in p for seq in SEQUENCES)

def score_password(password: str) -> dict:
    """
    Return a structured assessment:
    {
      'rating': 'Weak/Moderate/Strong/Very Strong',
      'score': 0-100,
      'entropy_bits': float,
      'checks': {...},
      'advice': [ ... ]
    }
    """
    advice = []
    checks = {
        "length_ge_12": len(password) >= 12,
        "has_lower": bool(re.search(r"[a-z]", password)),
        "has_upper": bool(re.search(r"[A-Z]", password)),
        "has_digit": bool(re.search(r"\d", password)),
        "has_symbol": bool(re.search(r"[^\w]", password)),
        "no_dict_word": not contains_dictionary_word(password),
        "no_sequence": not contains_sequence(password),
        "no_repeats": not has_repeated_runs(password, 3)
    }

    # Base scoring: start from 0, add for each good property
    score = 0
    weighting = {
        "length_ge_12": 25,
        "has_lower": 10,
        "has_upper": 10,
        "has_digit": 10,
        "has_symbol": 10,
        "no_dict_word": 15,
        "no_sequence": 10,
        "no_repeats": 10
    }
    for k, ok in checks.items():
        if ok:
            score += weighting[k]

    # Entropy bonus (cap at +10)
    entropy = estimate_entropy(password)
    if entropy >= 60:
        score += 10
    elif entropy >= 50:
        score += 7
    elif entropy >= 40:
        score += 5
    elif entropy >= 30:
        score += 3

    score = max(0, min(score, 100))

    # Rating
    if score < 40:
        rating = "Weak"
    elif score < 65:
        rating = "Moderate"
    elif score < 85:
        rating = "Strong"
    else:
        rating = "Very Strong"

    # Advice generation
    if not checks["length_ge_12"]: advice.append("Use at least 12 characters (16+ is better).")
    if not checks["has_lower"]:     advice.append("Add lowercase letters.")
    if not checks["has_upper"]:     advice.append("Add uppercase letters.")
    if not checks["has_digit"]:     advice.append("Add numbers.")
    if not checks["has_symbol"]:    advice.append("Add symbols (e.g., !@#?$%).")
    if not checks["no_dict_word"]:  advice.append("Avoid common words/phrases (e.g., 'password', 'qwerty').")
    if not checks["no_sequence"]:   advice.append("Avoid sequences like '12345' or 'qwerty'.")
    if not checks["no_repeats"]:    advice.append("Avoid repeated characters (e.g., 'aaaa' or '1111').")
    advice.append("Consider a passphrase of 4–5 random words (easy to remember, high entropy).")

    return {
        "rating": rating,
        "score": score,
        "entropy_bits": round(entropy, 1),
        "checks": checks,
        "advice": advice
    }

def pretty_print(result: dict, password: str):
    print("="*48)
    print("Password Strength Report")
    print("="*48)
    print(f"Password: {('*' * len(password)) if len(password) <= 24 else '(hidden)'}")
    print(f"Rating:   {result['rating']}  |  Score: {result['score']}/100  |  Entropy: {result['entropy_bits']} bits")
    print("-"*48)
    print("Checks:")
    for k, v in result["checks"].items():
        label = {
            "length_ge_12":"Length ≥ 12",
            "has_lower":"Has lowercase",
            "has_upper":"Has uppercase",
            "has_digit":"Has digit",
            "has_symbol":"Has symbol",
            "no_dict_word":"No common words",
            "no_sequence":"No sequences",
            "no_repeats":"No repeats"
        }[k]
        print(f"  [{'OK' if v else '!!'}] {label}")
    print("-"*48)
    print("Recommendations:")
    for tip in result["advice"]:
        print(f"  - {tip}")
    print("="*48)

def main():
    # Usage: python password_strength_checker.py [password]
    if len(sys.argv) > 1:
        pw = sys.argv[1]
    else:
        # Visible input (intentionally) so beginners can see what they typed
        pw = input("Enter a password to evaluate: ").strip()

    res = score_password(pw)
    pretty_print(res, pw)

if __name__ == "__main__":
    main()
