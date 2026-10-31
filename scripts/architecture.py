#!/usr/bin/env python3
"""Print the expected architecture of the Terraform project, without deploying."""

COMPONENTS = (
    ("Network", "VPC, one public subnet, internet gateway, route table"),
    ("Firewall", "Security group: inbound TCP 80; no inbound SSH"),
    ("Compute", "EC2 Amazon Linux 2023; cloud-init installs Nginx"),
    ("Security", "SSM-managed instance profile, IMDSv2, encrypted EBS"),
    ("Monitoring", "Two CloudWatch metric alarms, no notifications"),
)


def main() -> int:
    print("EXPECTED AWS LAB RESOURCES — not a live deployment")
    for category, description in COMPONENTS:
        print(f"{category:12} | {description}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
