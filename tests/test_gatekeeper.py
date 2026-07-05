from lygo_claw.gatekeeper import P0Gatekeeper


def test_validate_amplify():
    g = P0Gatekeeper()
    r = g.validate("hello lygo claw")
    assert r["verdict"] in ("AMPLIFY", "SOFTEN")