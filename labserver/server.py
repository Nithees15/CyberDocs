#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Cybersecurity-Mastery - an interactive, offline cybersecurity learning app.
# Copyright (C) 2026 Nithees Narendra S
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This file is part of Cybersecurity-Mastery. It is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version. There is NO WARRANTY. See the
# LICENSE file for the full text. For use outside the GPL-3.0 terms (e.g.
# proprietary/commercial), contact the copyright holder for a separate licence.

"""Cybersecurity-Mastery — local Lab Runner.

A tiny, dependency-free (Python stdlib only) HTTP server that lets the offline
learning site actually RUN the walkthrough commands — by executing them **inside
a designated Kali container** on your isolated lab network and returning the
output to the browser's "▸ Run" buttons and Live Terminal.

SECURITY — read this. This server executes commands. Its safety rests on:
  * It binds to 127.0.0.1 only (never your LAN/the internet).
  * /run and /lab require a session TOKEN printed on startup (blocks drive-by
    web pages from silently using it).
  * It executes ONLY via `docker exec <attacker-container> ...` — never on your
    host. The blast radius is the disposable Kali container on the isolated lab
    network, exactly matching the repo's fail-closed model.
  * It refuses if Docker or the container is unavailable, with a clear message.

Use it only for your own local, authorised lab. See README.md.

Run:  python server.py            (or ./run.sh / .\run.ps1)
"""

from __future__ import annotations

import json
import os
import secrets
import shlex
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

DEFAULT_CONFIG = {
    "host": "127.0.0.1",
    "port": 8777,
    "container": "kali",                       # the attacker container to exec into
    "shell": "bash",                           # shell inside the container
    "timeout_seconds": 180,
    "environments_dir": os.path.join(REPO, "labs", "environments"),
    "compose_project_prefix": "cm",
}


def load_config():
    cfg = dict(DEFAULT_CONFIG)
    path = os.path.join(HERE, "config.json")
    if os.path.exists(path):
        try:
            cfg.update(json.load(open(path, encoding="utf-8")))
        except Exception as e:
            print(f"[warn] could not read config.json: {e}")
    return cfg


CFG = load_config()
TOKEN = os.environ.get("LAB_TOKEN") or secrets.token_hex(16)


def docker_available():
    try:
        r = subprocess.run(["docker", "version"], capture_output=True, timeout=8)
        return r.returncode == 0
    except Exception:
        return False


def container_running(name):
    try:
        r = subprocess.run(["docker", "ps", "--filter", f"name=^{name}$", "--format", "{{.Names}}"],
                           capture_output=True, text=True, timeout=8)
        return name in r.stdout.split()
    except Exception:
        return False


def run_in_container(cmd):
    """Execute a command INSIDE the attacker container only. Never on the host."""
    if not docker_available():
        return "[lab runner] Docker is not available. Start Docker Desktop / the daemon.\n"
    name = CFG["container"]
    if not container_running(name):
        return (f"[lab runner] Container '{name}' is not running.\n"
                f"Start your Kali attacker container on the lab network, e.g.:\n"
                f"  docker run -dit --name {name} --network labnet kalilinux/kali-rolling\n"
                f"(or set a different name in labserver/config.json)\n")
    argv = ["docker", "exec", name, CFG.get("shell", "bash"), "-lc", cmd]
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=CFG["timeout_seconds"])
        out = (r.stdout or "") + (r.stderr or "")
        return out if out.strip() else "[done] (no output)\n"
    except subprocess.TimeoutExpired:
        return f"[lab runner] command timed out after {CFG['timeout_seconds']}s\n"
    except Exception as e:
        return f"[lab runner] error: {e}\n"


def compose_up(section, up=True):
    envdir = CFG["environments_dir"]
    path = os.path.join(envdir, f"{section}.yml")
    if not os.path.exists(path):
        return f"[lab runner] no environment file for '{section}' at {path}\n"
    if not docker_available():
        return "[lab runner] Docker is not available.\n"
    proj = f"{CFG['compose_project_prefix']}-{section}"
    argv = (["docker", "compose", "-p", proj, "-f", path] +
            (["up", "-d"] if up else ["down"]))
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=CFG["timeout_seconds"])
        return (r.stdout or "") + (r.stderr or "") or "[done]\n"
    except Exception as e:
        return f"[lab runner] compose error: {e}\n"


class Handler(BaseHTTPRequestHandler):
    server_version = "CMLabRunner/1.0"

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "X-Lab-Token, Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")

    def _send(self, code, body, ctype="text/plain; charset=utf-8"):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self._cors()
        self.end_headers()
        self.wfile.write(data)

    def _json(self, code, obj):
        self._send(code, json.dumps(obj), "application/json; charset=utf-8")

    def _authed(self):
        return self.headers.get("X-Lab-Token", "") == TOKEN

    def log_message(self, fmt, *args):
        pass  # quiet

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path.split("?")[0] == "/health":
            self._json(200, {
                "ok": True,
                "container": CFG["container"],
                "container_running": container_running(CFG["container"]),
                "docker": docker_available(),
                "needs_token": True,
            })
        else:
            self._send(404, "not found\n")

    def _read_json(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            return json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            return {}

    def do_POST(self):
        path = self.path.split("?")[0]
        if not self._authed():
            self._send(401, "[lab runner] missing/invalid token. Click 'Connect lab runner' in the site "
                            "and paste the token printed when you started the server.\n")
            return
        body = self._read_json()
        if path == "/run":
            cmd = (body.get("cmd") or "").strip()
            if not cmd:
                self._send(400, "[lab runner] empty command\n")
                return
            self._send(200, run_in_container(cmd))
        elif path == "/lab/up":
            self._send(200, compose_up(body.get("section", ""), up=True))
        elif path == "/lab/down":
            self._send(200, compose_up(body.get("section", ""), up=False))
        else:
            self._send(404, "not found\n")


def main():
    host, port = CFG["host"], int(CFG["port"])
    # ASCII-only output so it never crashes on a Windows cp1252 console.
    line = "=" * 66
    print(line)
    print("  Cybersecurity-Mastery - Lab Runner")
    print(line)
    print(f"  Listening on   http://{host}:{port}   (localhost only)")
    print(f"  Attacker box   container '{CFG['container']}' (docker exec)")
    print(f"  Docker present {docker_available()} | container running "
          f"{container_running(CFG['container'])}")
    print("")
    print("  SESSION TOKEN (paste into the site's 'Connect lab runner' box):")
    print(f"      {TOKEN}")
    print("")
    print("  In the site: open any lesson -> click 'Connect lab runner' in the Live")
    print("  Terminal card -> paste the token. Then 'Run' executes in the container.")
    print("  Ctrl-C to stop.  Safety: runs ONLY inside the container, never your host.")
    print(line)
    sys.stdout.flush()
    ThreadingHTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[lab runner] stopped.")
        sys.exit(0)
