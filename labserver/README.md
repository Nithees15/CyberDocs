# Lab Runner — make the site's commands actually run

The Cybersecurity-Mastery site is a fully-offline learning app. The **Lab Runner**
is the small optional backend that makes the **▸ Run** buttons and the **Live
Terminal** on each lesson *actually execute* — by running each command **inside a
Kali container** on your isolated lab network and streaming the output back to the
browser.

Without it, the site still works completely: every command has a **📋 Copy**
button and you run it in your own terminal. The Lab Runner just closes the loop.

## Requirements

- **Python 3.8+** (standard library only — nothing to `pip install`).
- **Docker** running.
- A **Kali attacker container** on your lab network. For example:

  ```bash
  docker network create labnet 2>/dev/null || true
  docker run -dit --name kali --network labnet kalilinux/kali-rolling
  # install tooling inside it as needed, e.g.:
  docker exec kali bash -lc "apt update && apt install -y kali-linux-headless"
  ```

  (Any container works; set its name in `config.json` → `container`.)

## Start it

```bash
# Linux / macOS
./run.sh
# Windows (PowerShell)
.\run.ps1
# or directly
python server.py
```

It prints a **session token**. In the site, open any lesson, find the **Live
Terminal** card, click **Connect lab runner**, and paste the token. From then on:

- **▸ Run** on any walkthrough step runs that command in the container.
- The **Live Terminal** input runs commands you type.
- **▸ Start lab** on a lesson's Lab-setup card brings up that part's targets
  (`docker compose up -d` of `labs/environments/<section>.yml`).

## Configuration — `config.json`

| Key | Meaning | Default |
| --- | --- | --- |
| `host` | Bind address — **keep it 127.0.0.1** | `127.0.0.1` |
| `port` | Port | `8777` |
| `container` | The attacker container to `docker exec` into | `kali` |
| `shell` | Shell inside the container | `bash` |
| `timeout_seconds` | Max seconds per command | `180` |

## Security — please read

This backend executes commands. It is safe **only because of these constraints**,
which you should not weaken:

- **Localhost only.** It binds `127.0.0.1`. Never expose it to your LAN or the
  internet.
- **Token required.** `/run` and `/lab/*` require the session token printed on
  startup, so a random web page open in your browser cannot silently drive it.
- **Container-scoped.** It executes **only** via `docker exec <container> …` —
  never on your host. The blast radius is the disposable Kali container on the
  isolated `labnet`, matching the repo's fail-closed model.
- **Your own lab only.** Use it exclusively for authorised testing of the local,
  intentionally-vulnerable targets in this repo — never against anything you do
  not own.

This is, by design, authenticated command execution into a container you control.
That is exactly what a hands-on lab needs; it is not a general-purpose service.

## Alternative: CyberForge

CyberForge already exposes container exec (`CYBERFORGE_DOCKER_EXEC_ENABLED=true`)
and an API. You can point the site at it instead of this runner if you prefer;
this runner is the decoupled default. CyberForge itself is used read-only.
