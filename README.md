# LYGO-Claw

**Humans:** open **[START_HERE.txt](START_HERE.txt)** then **[docs/QUICKSTART_FOR_HUMANS.md](docs/QUICKSTART_FOR_HUMANS.md)** — use **`launchers\INSTALL_AND_CHECK.bat`** on Windows.

**Full build log (no drift):** [docs/LYGO_USB_AND_CLAW_MASTER_WHITEPAPER.md](docs/LYGO_USB_AND_CLAW_MASTER_WHITEPAPER.md)

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

## LYGO CLAW USB (public standalone terminal)

**Full guide:** [docs/USB_PUBLIC_RELEASE.md](docs/USB_PUBLIC_RELEASE.md)

| Artifact | What |
|----------|------|
| `usb/` in this repo | Launchers, configs, dashboards, verify scripts |
| **Full offline zip** (~8 GB) | [Excavationpro downloads](https://deepseekoracle.github.io/Excavationpro/downloads/) → `LYGO-CLAW-USB-PUBLIC-v1.0.0.zip` |

**Quick boot:** extract zip → `LYGO_CLAW_Launch.bat` → dashboard connects at `ws://127.0.0.1:18789`.

**Verify before publish:**
```bash
python scripts/verify_usb_claw_public.py releases/staging-full --require-weights
```

## USB Champion integration (host pairing)

Plug the USB stick, then on PC:

```bash
lygo-claw usb-health
```

Optional BUILDR supervisor on `:9630` — see [docs/USB_SUPERVISOR.md](docs/USB_SUPERVISOR.md).

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