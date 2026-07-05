# USB supervisor bridge

When the LYGO Champion USB is plugged in and `LYGO_BUILDR_Daemon.bat` (or `LYGO_Supervisor_Daemon.bat`) is running:

- URL: `http://127.0.0.1:9630` (override with `LYGO_USB_SUPERVISOR_URL`)
- `lygo-claw usb-health` — GET `/health`
- Gateway calls POST `/Supervise` with `agent_id` + `tool_call`

If offline, gateway **soft-approves** with `skipped: usb_supervisor_offline` (configurable hard-fail in future).

**Task the stick:** `lygo-claw buildr-task verify_standalone --wait` (POST `/Task` on the daemon).

BUILDR entry: `phase2/buildr_usb_daemon.py` on the USB root.