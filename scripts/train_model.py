#!/usr/bin/env python3
"""Thin CLI wrapper over ``certmalconv.training.train``."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import yaml

from certmalconv.training.train import TrainConfig, train
from certmalconv.utils.logging import configure_logging

log = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path,
                        default=Path("configs/training/training_config.yaml"))
    parser.add_argument("--dataset", default="bodmas")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--seeds", type=int, nargs="*", default=None)
    args = parser.parse_args()
    configure_logging()

    with open(args.config) as f:
        yaml_cfg = yaml.safe_load(f) or {}
    cfg_dict = yaml_cfg.get("training", {}) | {"dataset": args.dataset}

    seeds = args.seeds or [args.seed]
    for seed in seeds:
        cfg = TrainConfig(**{**cfg_dict, "seed": seed})
        log.info("Training seed=%d config=%s", seed, args.config.name)
        metrics = train(cfg)
        print(json.dumps({"seed": seed, "metrics": metrics}))


if __name__ == "__main__":
    main()
