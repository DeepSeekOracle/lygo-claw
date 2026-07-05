# Troubleshooting

## Python not found

Install Python 3.11+ with **Add to PATH**. Close and reopen Command Prompt.

## pip install fails

```powershell
cd "path\to\lygo-claw"
python -m pip install -e ".[dev]"
```

## usb-health ok: false

- Plug LYGO USB, run `LYGO_Supervisor_Daemon.bat` on the stick.
- Windows Firewall: allow local 127.0.0.1 only.

## gateway ok: false

Read `p0.verdict` in output. QUARANTINE means input blocked by design.

## run lattice fails

Set `LYGO_STACK_ROOT` to folder containing `tools/verify_lattice_alignment.py` (on USB: `...\stack\lygo-protocol-stack`).

## Self-test

```powershell
python scripts/self_check.py
```

Expect `pytest_exit: 0` and `gateway_ok: true`.