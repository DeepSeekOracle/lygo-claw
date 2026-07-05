# LYGO-Claw — command reference

Install once: `pip install -e .` from repo root (or use `INSTALL_AND_CHECK.bat`).

| Command | What it does |
|---------|----------------|
| `lygo-claw gateway "your text"` | Full safety pipeline (P0 + Hermes + USB if present) |
| `lygo-claw validate "text"` | P0 only — AMPLIFY / SOFTEN / QUARANTINE |
| `lygo-claw usb-health` | Ping USB supervisor (port 9630) |
| `lygo-claw audit verify` | Check Hermes hash chain |
| `lygo-claw run help` | List built-in limbs |
| `lygo-claw run status` | Paths and hybrid skill hints |

**Windows without PATH:** `bin\lygo-claw.bat gateway "hello"`

**Environment (optional):**

- `LYGO_USB_SUPERVISOR_URL` — default `http://127.0.0.1:9630`
- `LYGO_STACK_ROOT` — portable stack for `run lattice`