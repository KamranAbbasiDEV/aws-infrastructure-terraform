#!/usr/bin/env python3
"""Manual, read-only smoke test against an authorized HTTP(S) endpoint."""
from __future__ import annotations
import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


def smoke_test(url: str, timeout: float = 5.0) -> dict:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Provide a full HTTP(S) URL")
    if parsed.username or parsed.password:
        raise ValueError("Credentials must not appear in URLs")
    if not 0 < timeout <= 30:
        raise ValueError("Timeout must be greater than 0 and at most 30 seconds")

    # Strip query string and fragments from the printable URL.
    sanitized = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))
    request = urllib.request.Request(url, headers={"User-Agent": "CloudOps-AWS-Lab/1.0"})
    started = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            code = response.status
            body = response.read(32768)
    except urllib.error.HTTPError as exc:
        code = exc.code
        body = b""
        exc.close()
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {"url": sanitized, "status": "failed", "detail": str(exc),
                "elapsed_ms": round((time.monotonic() - started) * 1000, 2)}
    return {"url": sanitized, "status": "passed" if 200 <= code < 400 else "failed",
            "http_status": code, "contains_lab_marker": b"CloudOps Infrastructure Lab" in body,
            "elapsed_ms": round((time.monotonic() - started) * 1000, 2)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Endpoint you own or have permission to check")
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args(argv)
    try:
        result = smoke_test(args.url, args.timeout)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
