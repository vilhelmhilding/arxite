# Arxite – Hardened Web Application Architecture

**Arxite** is a fully self-hosted, production-ready demo of a **Zero Trust web application architecture**.

## Table of Contents
- [Key Features](#key-features)
- [Requirements](#requirements)
- [Security Note](#security-note)
- [Quickstart Overview](#quickstart-overview)
  1. [Clone & Setup](#clone--setup)
  2. [Configure Cloudflare & DNS](#configure-cloudflare--dns)
  3. [Harden Host Firewall](#harden-host-firewall)
  4. [Start Dockerized App](#start-dockerized-app)
  5. [Access the App](#access-the-app)
- [Security Architecture](#security-architecture)
- [Project Structure](#project-structure)
- [License](#license)

## Key Features
- **Fully self-hosted & air-gapped-ready** — no external dependencies
- **Cloudflare Tunnel** (via `cloudflared`) for edge protection
- **Dockerized Services** (with `Docker` & `Docker Compose`)
- **OAuth2 Authentication** via `GitHub`
- **Rate Limiting** per IP with `Redis`
- **Session Hardening**: HttpOnly, Secure, SameSite cookies
- **User-Agent & Path Filtering** against common attacks
- **Production-ready WSGI server** using `Waitress`
- **Complete project structure**, configurations & templates

## Requirements
- Docker
- Docker Compose
- Python 3.10+
- A GitHub OAuth App
- A registered domain (e.g., `arxite.com`)
- A Cloudflare account with DNS control

## Security Note

This repository includes **dummy configuration files and placeholder credentials** to illustrate a complete Zero Trust deployment setup:

- `.env.example`: Template with fake secrets for local setup  
- `cloudflared/cert.pem`: **NOT a real certificate** – included for structural clarity  
- `cloudflared/<tunnel-id>.json`: Example format only  

> **Do not reuse these files in production, always:**
> - Replace with your own secrets and credentials  
> - Never commit actual secrets or tokens to version control  
> - Ensure `.env` is ignored in `.gitignore`, as this project does

## Quickstart Overview

### Clone & Setup
```bash
git clone https://github.com/vilhelmhilding/arxite.git
cd arxite
cp .env.example .env  # Edit with your own secrets
```
Edit `.env` and set:
```env
SECRET_KEY=your-flask-secret-key
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
REDIRECT_URI=https://yourdomain.com/auth/callback
REDIS_PASSWORD=your-redis-password
```

### Configure Cloudflare & DNS
1. **Create a Cloudflare Tunnel**  
   ```bash
   cloudflared tunnel create arxite_com
   ```
2. **Move credentials into place**  
   ```bash
   mv ~/.cloudflared/*.json ./cloudflared/REPLACE_WITH_TUNNEL_ID.json
   ```
3. **Edit `cloudflared/config.yml`** for your hostname and credential path.
4. **Update your domain’s nameservers** to Cloudflare (if not already).
5. **Add DNS records** in the Cloudflare dashboard:  
   - `A` record: `arxite.com` → placeholder IP  
   - `CNAME`: `www.arxite.com` → `arxite.com`  
   Set both to **Proxied**.

### Harden Host Firewall
Block all inbound traffic except through the Cloudflare Tunnel:
- Port `51821` (Flask app)
- Port `6379` (Redis)

### Start Dockerized App
```bash
docker-compose up --build
```

### Access the App
Visit:
```
https://yourdomain.com
```
Log in with GitHub — your session is rate-limited, secured, and protected behind a Cloudflare Tunnel.

## Security Architecture

### External Protection (Edge)
- Cloudflare Tunnel eliminates open ports and public IPs.
- HTTPS & DDoS mitigation via Cloudflare.
- DNS masking with proxied records.

### Internal Safeguards
- Rate limiting per IP using Redis.
- Strong session settings: HttpOnly, Secure, SameSite.
- User-Agent & path filtering against bots and scanners.
- Renamed sensitive Redis commands to prevent abuse.
- Containers run as non-root users.
- Host firewall rules deny direct access to internal services.

## Project Structure
```
arxite/
├── .dockerignore
├── .env.example
├── .gitignore
├── README.md
│
├── app/
│   ├── Dockerfile
│   ├── __init__.py
│   ├── auth.py
│   ├── errors.py
│   ├── requirements.txt
│   ├── routes.py
│   ├── security.py
│   ├── static/
│   └── templates/
│
├── cloudflared/
│   ├── <tunnel-id>.json
│   ├── cert.pem
│   └── config.yml
│
├── docker-compose.yml
├── redis/
│   └── redis.conf
└── run.py
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
