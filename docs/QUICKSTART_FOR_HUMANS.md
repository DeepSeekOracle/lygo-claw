# LYGO-Claw — quick start (humans)

## Do I need an .exe?

**Not yet.** You need **Python 3.11+** once. Use the included `.bat` launchers (same idea as double-clicking an app).

Pre-built `.exe` may come later; the supported path today is Python + `INSTALL_AND_CHECK.bat`.

## 5-minute setup (Windows)

1. **Python** — https://www.python.org/downloads/ — enable **Add to PATH**.
2. Open this folder in File Explorer.
3. Double-click **`launchers\INSTALL_AND_CHECK.bat`**.
4. Double-click **`launchers\TRY_GATEWAY.bat`** — you should see JSON with `"ok": true`.

## With the LYGO USB (recommended)

| Step | Where | Action |
|------|--------|--------|
| 1 | USB | `LYGO_One_Boot_AI.bat` — offline chat |
| 2 | USB | `LYGO_Supervisor_Daemon.bat` — leave open |
| 3 | PC | `lygo-claw usb-health` — stick guardian online |

## What each piece does

- **gateway** — checks incoming text (P0), logs to Hermes, asks USB to approve if plugged in.
- **run** — runs safe stack commands (`help`, `status`, `lattice` if stack installed).
- **Champions** — persona text in `champions/` (Lightfather, LYRA, …).

## Stuck?

See **`docs\COMMANDS.md`** and **`docs\TROUBLESHOOTING.md`**.