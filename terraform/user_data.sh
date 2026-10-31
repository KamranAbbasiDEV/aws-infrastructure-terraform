#!/bin/bash
set -euo pipefail

# Runs once at first boot. Bootstrap logs: /var/log/cloud-init-output.log
# Sample static content only; no application credentials or secrets.
dnf install -y nginx
cat > /usr/share/nginx/html/index.html <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CloudOps AWS Lab</title>
  <style>
    body{font:16px/1.6 system-ui,sans-serif;background:#0b1725;color:#eef4fa;min-height:100vh;display:grid;place-items:center;margin:0}
    main{max-width:620px;padding:42px;border:1px solid #294761;border-radius:14px;background:#14283b}
    h1{margin:0 0 12px;font-size:2rem}p{color:#b4cadc}.tag{color:#65dcbb;font-size:.85rem;letter-spacing:.1em;text-transform:uppercase}
  </style>
</head>
<body><main><p class="tag">Terraform / Amazon EC2 / Nginx</p><h1>CloudOps Infrastructure Lab</h1>
<p>This server was provisioned through Infrastructure as Code and configured by EC2 user data.</p>
<p>For demonstration only: HTTP is intentionally used. Do not host private data or credentials here.</p>
</main></body>
</html>
HTML
systemctl enable --now nginx
curl --fail --silent http://127.0.0.1/ >/dev/null
