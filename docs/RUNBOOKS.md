# Operational runbooks — AWS EC2 / Nginx / Terraform

Each runbook starts by identifying affected resources and confirming authorization. This is an educational guide; do not run destructive operations against production without a change procedure.

## 1. Website is unreachable over HTTP

1. Confirm the `http_url` value using `terraform output -raw http_url` from `terraform/`.
2. Confirm EC2 state and both EC2 status checks in the AWS console.
3. Confirm instance public IPv4 address is assigned; addresses can change following recreation.
4. Verify route table: `0.0.0.0/0 -> internet gateway`; subnet is associated with the correct route table.
5. Verify security group allows inbound TCP 80 from your current public IP. No inbound SSH rule should exist.
6. Check host service via Session Manager: `sudo systemctl status nginx`.
7. Check cloud-init bootstrap: `sudo tail -n 100 /var/log/cloud-init-output.log`.
8. Run `curl -I http://localhost` inside the instance. If local works but remote does not, focus on network configuration.
9. Record timestamps and results; avoid assigning an unconfirmed root cause.

## 2. Nginx bootstrap fails

1. View `/var/log/cloud-init-output.log` and `/var/log/cloud-init.log`.
2. Inspect package installation and startup: `sudo dnf info nginx` and `sudo journalctl -u nginx -n 100 --no-pager`.
3. Confirm configuration: `sudo nginx -t`.
4. Confirm port: `sudo ss -ltnp | grep ':80'`.
5. Check outbound connectivity to package repositories if `dnf` failed.
6. If remediation requires EC2 replacement, review the Terraform plan and data preservation before applying.

## 3. Can't connect with Session Manager

1. Check instance profile and attachment to `AmazonSSMManagedInstanceCore`.
2. Confirm SSM Agent service and outbound HTTPS to regional `ssm` and `ssmmessages` endpoints.
3. Confirm your IAM identity can call `ssm:StartSession` on the target; access is separate from EC2 role permissions.
4. Confirm the instance has bootstrapped, a working route to the internet and valid DNS.
5. Review managed-instance registration and AWS Systems Manager troubleshooting documentation.
6. Do **not** add public SSH access as a quick workaround.

## 4. CloudWatch alarm triggers

1. Review the alarm name, status, recent values and evaluation window.
2. For `StatusCheckFailed`, inspect EC2 status checks and AWS Health notices.
3. For `CPUUtilization`, inspect traffic, Nginx logs, background processes and recent changes.
4. Note: the two alarms deliberately have `actions_enabled = false`. They do not send email or automate recovery.
5. Escalate with evidence and the precise timeframe.

## 5. Unexpected AWS charges

1. Review AWS Billing and Cost Explorer by resource and region.
2. Compare with the Terraform state and deployed resource list.
3. If lab no longer needed, run `terraform destroy` from the correct directory/workspace.
4. Verify termination, EBS volume deletion, IP release and alarm deletion in the console.
5. Audit leftover resources, state handling and billing alerts before launching new labs.

## Sample incident ticket fields

- Incident ID (training):
- Start time (UTC):
- Observed symptom:
- Affected endpoint / instance ID:
- Customer impact: unconfirmed until verified
- Evidence gathered:
- Timeline:
- Current owner / escalation:
- Next update time:
- Root cause: unconfirmed until analysis completes
