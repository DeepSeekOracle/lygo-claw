# Upstream OpenClaw (optional)

MIT: https://github.com/openclaw/openclaw

```powershell
.\scripts\vendor_openclaw.ps1
```

Places a shallow clone in `vendor/openclaw/`. LYGO-Claw does **not** require it for P0/Hermes/USB/Champion CLI. Use upstream for full multi-channel gateway when you are ready to wire TypeScript/Node bridge.

Rebrand policy: preserve upstream LICENSE/NOTICE in `vendor/openclaw/`.