from config.loader import Config

def test_config_loads():
    cfg = Config.load()
    assert "EURUSD" in cfg.pairs
    assert "GBPJPY" in cfg.pairs

def test_low_volatility_hierarchy():
    cfg = Config.load()
    eurusd = cfg.get_pair("EURUSD")
    assert eurusd.timeframe_for("bias") == "D1"
    assert eurusd.timeframe_for("entry") == "M15"

def test_high_volatility_hierarchy():
    cfg = Config.load()
    gbpjpy = cfg.get_pair("GBPJPY")
    assert gbpjpy.timeframe_for("bias") == "H4"
    assert gbpjpy.timeframe_for("entry") == "M5"

def test_fib_and_risk_config():
    cfg = Config.load()
    assert cfg.fib.poi_band == (0.62, 0.79)
    assert cfg.risk.stop_loss_pips_max == 15