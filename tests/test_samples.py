import subprocess, sys, os

def run(pw):
    out = subprocess.check_output([sys.executable, "password_strength_checker.py", pw]).decode()
    return out

def test_weak():
    o = run("password")
    assert "Weak" in o or "Moderate" in o

def test_strong():
    o = run("This-Is-A-Pretty-Good-Passphrase-2025!")
    assert "Strong" in o or "Very Strong" in o
