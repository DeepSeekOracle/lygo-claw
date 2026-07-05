# USB supervisor bridge

When the LYGO Champion USB is plugged in and `LYGO_Supervisor_Daemon.bat` is running:

- URL: `http://127.0.0.1:9630` (override with `LYGO_USB_SUPERVISOR_URL`)
- `lygo-claw usb-health` — GET `/health`
- Gateway calls POST `/Supervise` with `agent_id` + `tool_call`

If offline, gateway **soft-approves** with `skipped: usb_supervisor_offline` (configurable hard-fail in future).

BUILDR stick path: `E:\LYGO_BUILDER_KEY\phase2\daemon_supervisor.py`