# LYGO integration (LYGO-Claw)

Per Biophase7 `LYGO-Claw.txt`: fork/enhance OpenClaw with a **LYGO control plane**, do not rewrite mature execution cores blindly.

## Layers

| Layer | Module | Role |
|-------|--------|------|
| P0 | `gatekeeper.py` + `vendor/p0/byte_entropy_filter.py` | Prompt/command quarantine |
| Hermes | `hermes_audit.py` | Hash-chained audit |
| P1 | `memory.py` | Mycelium fragments (12/10) |
| P3 | `consensus.py` | Multi-agent consensus hook |
| P5 | `harmony.py` | Run identity / ethical mass |
| Gateway | `gateway.py` | Ingest pipeline |
| USB | `usb_supervisor.py` | mTLS-ready HTTP to stick :9630 |
| Champions | `champion_loader.py` + `champions/` | Persona prompts |

## CLI

```bash
lygo-claw gateway "<user message>"
lygo-claw run lattice    # requires LYGO_STACK_ROOT
lygo-claw validate "text"
```

Set `LYGO_STACK_ROOT` to portable stack on USB for lattice/army limbs.