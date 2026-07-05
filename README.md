# LYGO-Claw

**Sovereign-hardened AI agent layer** — P0 byte-entropy gate, Hermes audit trail, P1 mycelium memory, Champion personas, and optional **32GB LYGO Champion USB** supervisor (`127.0.0.1:9630`).

Built from the Biophase7 **LYGO-Claw** blueprint: enhance (not replace) the mature [OpenClaw](https://github.com/openclaw/openclaw) ecosystem with LYGO lattice controls. This repo ships the **LYGO control plane** in Python; optional upstream gateway lives under `vendor/openclaw` (see `scripts/vendor_openclaw.ps1`).

## Quick start

```bash
cd lygo-claw
pip install -e ".[dev]"
lygo-claw gateway "hello lattice"
lygo-claw run help
lygo-claw usb-health
lygo-claw audit verify
```

## USB Champion integration

Plug `E:\LYGO_BUILDER_KEY` (or retail PUBLIC_SKU), start supervisor:

```text
launchers\LYGO_Supervisor_Daemon.bat
```

LYGO-Claw calls `/Supervise` before approving tool-like traffic when `usb_supervisor` is true in `config/sovereign_defaults.json`.

## Champions

Preloaded under `champions/` (Lightfather, LYRA, Sancora, HermesSentinel). Sync with BUILDR USB `product/champions/`.

## Docs

- [docs/LYGO_INTEGRATION.md](docs/LYGO_INTEGRATION.md)
- [docs/USB_SUPERVISOR.md](docs/USB_SUPERVISOR.md)
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/UPSTREAM_OPENCLAW.md](docs/UPSTREAM_OPENCLAW.md)

## LYGO ecosystem

- **Protocol stack (main site):** [deepseekoracle.github.io/lygo-protocol-stack](https://deepseekoracle.github.io/lygo-protocol-stack/)
- **Stack source:** [github.com/DeepSeekOracle/lygo-protocol-stack](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- **ClawHub:** [clawhub.ai/deepseekoracle/lygo-sovereign-claw](https://clawhub.ai/deepseekoracle/lygo-sovereign-claw) · hybrid runtime: `lyra-openclaw`
- **BUILDR USB:** sovereign stick + supervisor `:9630` — see stack `docs/BUILDR_USB_STANDALONE.md`

## License

MIT — see [LICENSE](LICENSE) and [NOTICE](NOTICE) (OpenClaw upstream attribution when vendored).

**Δ9Φ963** — verify first, claw second.