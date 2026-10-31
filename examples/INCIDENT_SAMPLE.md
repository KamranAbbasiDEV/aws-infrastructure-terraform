# Simulated incident: HTTP endpoint unavailable

> Entirely fictional training example; no live AWS resources were tested.

**Status:** Investigating  
**Severity:** Internal demo only  
**Impact:** Not assessed — synthetic exercise

## Symptoms

- Demo HTTP endpoint returns a connection error.
- EC2 state was reported as `running` in the fictional scenario.
- The Nginx process was intentionally not started as part of this training exercise.

## Triage sequence

1. Check public-IP, security group, route table and internet gateway.
2. Start a Systems Manager session without opening SSH.
3. Check `systemctl status nginx` and `/var/log/cloud-init-output.log`.
4. Review synthetic Nginx startup failure evidence and identify missing service startup.
5. Document the hypothetical fix: `sudo systemctl enable --now nginx`.
6. Re-run a local and external smoke check after authorization.

**Root cause:** Simulated startup failure; not supported by real telemetry.

## Prevention

Verify cloud-init output and add a deployment smoke test to the rollout checklist.
