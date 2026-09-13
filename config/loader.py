"""
Loads config/pairs.yaml and resolves it into simple, typed objects.

This is the ONLY place that should read pairs.yaml directly. Every other module
(data layer, structure detectors, strategy, risk) should import PairConfig objects
from here, never touch YAML or hardcode timeframes.
"""

from dataclasses import dataclass
from pathlib import Path
import yaml

ROLES = ("bias", "trend_poi", "structure_entry", "entry")

CONFIG_PATH = Path(__file__).parent / "pairs.yaml"


@dataclass(frozen=True)
class PairConfig:
    symbol: str
    volatility_class: str
    timeframes: dict  # role -> timeframe string, e.g. {"bias": "D1", ...}

    def timeframe_for(self, role: str) -> str:
        if role not in ROLES:
            raise ValueError(f"Unknown role '{role}'. Must be one of {ROLES}")
        return self.timeframes[role]

    @property
    def all_timeframes(self) -> list:
        """Unique timeframes this pair needs fetched, in role order."""
        seen = []
        for role in ROLES:
            tf = self.timeframes[role]
            if tf not in seen:
                seen.append(tf)
        return seen


@dataclass(frozen=True)
class FibConfig:
    premium_discount_split: float
    poi_band: tuple  # (low, high)


@dataclass(frozen=True)
class RiskConfig:
    stop_loss_pips_min: float
    stop_loss_pips_max: float
    take_profit_pip_targets: list


class Config:
    """Top-level resolved config. Use Config.load() to get an instance."""

    def __init__(self, pairs: dict, fib: FibConfig, risk: RiskConfig):
        self.pairs = pairs  # symbol -> PairConfig
        self.fib = fib
        self.risk = risk

    @classmethod
    def load(cls, path: Path = CONFIG_PATH) -> "Config":
        with open(path, "r") as f:
            raw = yaml.safe_load(f)

        vol_classes = raw["volatility_classes"]

        pairs = {}
        for symbol, pair_raw in raw["pairs"].items():
            vclass = pair_raw["volatility_class"]
            if vclass not in vol_classes:
                raise ValueError(
                    f"Pair {symbol} references unknown volatility_class '{vclass}'"
                )
            pairs[symbol] = PairConfig(
                symbol=symbol,
                volatility_class=vclass,
                timeframes=dict(vol_classes[vclass]),
            )

        fib_raw = raw["fib"]
        fib = FibConfig(
            premium_discount_split=fib_raw["premium_discount_split"],
            poi_band=tuple(fib_raw["poi_band"]),
        )

        risk_raw = raw["risk"]
        risk = RiskConfig(
            stop_loss_pips_min=risk_raw["stop_loss_pips_min"],
            stop_loss_pips_max=risk_raw["stop_loss_pips_max"],
            take_profit_pip_targets=list(risk_raw["take_profit_pip_targets"]),
        )

        return cls(pairs=pairs, fib=fib, risk=risk)

    def get_pair(self, symbol: str) -> PairConfig:
        if symbol not in self.pairs:
            raise KeyError(f"Pair '{symbol}' not found in config")
        return self.pairs[symbol]