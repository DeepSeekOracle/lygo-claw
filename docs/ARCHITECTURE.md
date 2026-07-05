# Architecture

```
Chat / CLI / (optional OpenClaw channels)
        |
        v
SovereignGateway (P0 + Hermes + USB)
        |
        v
LYGOOpenClaw.run -> limbs dispatch
        |
        +-- P1 mycelium store
        +-- kernel egg anchor (when stack present)
```

**Public safety defaults** (`config/sovereign_defaults.json`):

- Bind `127.0.0.1` only
- `disable_public_clawhub_autoload: true`
- P0 enforced on gateway ingest