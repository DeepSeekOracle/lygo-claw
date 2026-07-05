from lygo_claw.gateway import SovereignGateway


def test_gateway_ingest():
    gw = SovereignGateway()
    r = gw.ingest("test message", tool_name="test")
    assert "ok" in r
    assert "p0" in r