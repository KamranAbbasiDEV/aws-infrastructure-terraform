#!/usr/bin/env python3
"""Offline structural sanity checks for portfolio source files.

Does not replace Terraform's own fmt/validate, a security review or a deploy test.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def inspect_source() -> dict[str, bool]:
    main = (ROOT / "terraform" / "main.tf").read_text(encoding="utf-8")
    versions = (ROOT / "terraform" / "versions.tf").read_text(encoding="utf-8")
    init = (ROOT / "terraform" / "user_data.sh").read_text(encoding="utf-8")
    return {
        "dedicated_vpc": 'resource "aws_vpc" "lab"' in main,
        "internet_gateway": 'resource "aws_internet_gateway" "lab"' in main,
        "ssm_managed_instance": "AmazonSSMManagedInstanceCore" in main,
        "encrypted_ebs": "encrypted             = true" in main,
        "imdsv2_required": 'http_tokens   = "required"' in main,
        "no_ssh_ingress": "from_port   = 22" not in main and "to_port     = 22" not in main,
        "cloudwatch_alarms": main.count('resource "aws_cloudwatch_metric_alarm"') == 2,
        "no_automated_alarm_actions": main.count("actions_enabled     = false") == 2,
        "nginx_bootstrap": "dnf install -y nginx" in init and "systemctl enable --now nginx" in init,
        "terraform_provider": 'source  = "hashicorp/aws"' in versions,
    }


def main() -> int:
    results = inspect_source()
    for check, passed in results.items():
        print(f"{'PASS' if passed else 'FAIL'}  {check}")
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
