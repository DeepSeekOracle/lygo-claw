# LYGO CLAW USB — public release guide

**Canonical repo:** [DeepSeekOracle/lygo-claw](https://github.com/DeepSeekOracle/lygo-claw)  
**Full offline kit:** [GitHub Releases](https://github.com/DeepSeekOracle/lygo-claw/releases) (`LYGO-CLAW-USB-PUBLIC-*.zip`)

## What you get

A **self-contained local AI terminal** on Windows:

1. Plug USB (or extract zip to any folder)
2. Run `LYGO_CLAW_Launch.bat`
3. Chat in the dashboard — no cloud API required

Stack: portable **Ollama** (`qwen2.5:3b`) + **LYGO CLAW Gateway** + browser UI.

## Download paths

| Artifact | Contents | Size |
|----------|----------|------|
| **Release zip** | Full working USB (Ollama + models + gateway) | ~8 GB |
| **`usb/` in repo** | Launchers, configs, dashboards (no models/runtime/gateway dist) | Small source tree |
| **`releases/staging-full`** | Maintainer-local verified full kit (~8.5 GB) | Build with `package_usb_claw_public.ps1` |

Clone the repo for docs and host pairing. End users need the **release zip** (built via `create_usb_release_zip.ps1`) for the complete offline stick.

## Install (end user)

1. Download latest `LYGO-CLAW-USB-PUBLIC-*.zip` from Releases.
2. Extract to USB drive or `D:\LYGO_CLAW` (any path without special permissions issues).
3. Double-click `LYGO_CLAW_Launch.bat`.
4. In the dashboard: **Connect** (token prefilled) → send a test message.
5. Optional: install [LYGO-Claw](https://github.com/DeepSeekOracle/lygo-claw) on PC and run `lygo-claw usb-health`.

## Verify it works

From the extracted USB root:

```powershell
python path\to\lygo-claw\scripts\verify_usb_claw_public.py . --require-weights
```

After boot:

```powershell
python path\to\lygo-claw\scripts\verify_usb_claw_public.py . --require-weights --check-ports
```

Expect `ok: true` and models `qwen2.5:3b` (and optionally `llama3.2:1b`).

## Build / repackage (maintainers)

From a verified private builder stick (`LYGO_BUILDER_KEY`):

```powershell
cd lygo-claw
powershell -ExecutionPolicy Bypass -File scripts\package_usb_claw_public.ps1 `
  -SourceRoot "I:\E Drive\LYGO_BUILDER_KEY" `
  -OutRoot "releases\staging-full" `
  -IncludeWeights -IncludeOllamaRuntime

python scripts\verify_usb_claw_public.py releases\staging-full --require-weights
```

Create release zip:

```powershell
Compress-Archive -Path releases\staging-full\* -DestinationPath releases\LYGO-CLAW-USB-PUBLIC-v1.0.0.zip
gh release create v1.0.0 releases\LYGO-CLAW-USB-PUBLIC-v1.0.0.zip --title "LYGO CLAW USB Public v1.0.0"
```

## Security (public SKU)

Public packages **must not** include:

- `boot/` API keys or wallet material
- `_builder_vault/`
- Runtime logs with tokens
- Private restore anchors listing key paths

`verify_usb_claw_public.py` scans for these before publish.

## Pair with LYGO-Claw (host)

The USB runs standalone. **LYGO-Claw** on the PC adds P0 gate, Hermes audit, champion personas, and optional BUILDR supervisor `:9630`.

See [QUICKSTART_FOR_HUMANS.md](QUICKSTART_FOR_HUMANS.md) and [USB_SUPERVISOR.md](USB_SUPERVISOR.md).

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Port 11434 in use | Close other Ollama; re-run launcher |
| Gateway disconnected | Wait 15s; click Reconnect |
| No models listed | Run `usb\scripts\hydrate_usb_models.ps1` (online once) |
| Path with spaces | Use provided `.ps1` launchers (space-safe) |

**Δ9Φ963** — verify first.