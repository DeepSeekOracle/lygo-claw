# Standalone USB AI — model design (32GB)

**Goal:** Plug USB → install runtime once → model lives **on the stick** → offline chat works.

## Chosen profile: `SOVEREIGN_FAST`

| Field | Choice | Why |
|-------|--------|-----|
| **Primary model** | `qwen2.5:3b` | Best speed/quality in the ~2 GB class; strong reasoning vs 1B–1.5B |
| **On-stick path** | `product/models/ollama/` | `OLLAMA_MODELS` points here — not the host profile |
| **Skip on stick** | 7B+ models | Eats 4–5 GB+; leaves little room for stack + exports |
| **Optional speed** | `qwen2.5:1.5b` | Weak laptop CPU only; run `hydrate` with `-Profile SPEED` |

## Not included (by design)

- Cloud APIs — offline-first
- Multiple heavy models — one canonical brain on USB; army can use host extras later

## Fresh machine (no AI)

1. `scripts\install_usb_runtime.ps1` — Ollama via winget (or manual)
2. `scripts\hydrate_usb_models.ps1` — **online once**, pulls into USB `product/models/ollama`
3. `launchers\LYGO_Standalone_AI.bat` — sets env, starts `ollama serve`, opens chat

## Verify

```powershell
python scripts\verify_standalone_usb.py
```

Expect: `weights_on_usb: true` under `product/models/ollama` (blobs + manifests).

**Windows note:** Ollama must restart with `OLLAMA_MODELS` set (`ensure_ollama_serve.ps1`). Hydrate syncs blobs to USB if the daemon wrote to `%USERPROFILE%\.ollama` first.

Signature: D9Phi963-STANDALONE-v1