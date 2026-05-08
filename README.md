# 🚀 Dockerized Multi‑Container Application with CI/CD Deployment
 
This repository demonstrates a **real‑world DevOps pipeline** that takes code from a GitHub push all the way to **automatic deployment on an AWS EC2 server** — with a live UI that makes the entire pipeline visible to any user.
 
The focus is **system correctness, reproducibility, and automation** — not toy examples.
 
---
 
## 🌐 Live Demo
 
**[http://44.220.146.167](http://44.220.146.167)**
 
Open it and you will see:
- Your real IP address — fetched live from the Python backend
- Backend status including the exact **Git commit SHA** that was deployed
- An animated breakdown of the **7 CI/CD steps** that delivered this page
- The system architecture diagram showing how traffic flows
---
 
## 🧠 What This Project Proves
 
* You understand **how CI and CD are different — and how they work together**
* You can build **immutable artifacts** (Docker images)
* You can deploy **the exact same artifact** that passed CI
* You can automate deployments **securely using SSH**
* You can inject build metadata (Git SHA) into running containers
* You can debug real‑world DevOps issues (networking, SSH, permissions, CI runners)
This is **job‑ready DevOps work**, not tutorial code.
 
---
 
## 🏗️ Architecture Overview
 
```
Browser
   ↓
Frontend (Nginx container) — Port 80
   ↓   /api/* → reverse proxy (Docker internal network)
Backend (Python HTTP server container) — Port 8000 (internal only)
```
 
* Browser talks **only to the frontend**
* Nginx acts as a **reverse proxy** — strips `/api/` prefix and forwards to backend
* Backend is **not exposed publicly**
* Containers communicate via **Docker internal networking**
---
 
## 🧩 Application Components
 
### 1️⃣ Backend (Python)
 
Lightweight HTTP server with four endpoints:
 
| Endpoint | Response |
|---|---|
| `/` | Hello from Python server |
| `/whoami` | Client IP address |
| `/status` | JSON — server info + deployed Git SHA |
| `/pipeline` | JSON — 7-step CI/CD pipeline story |
 
* Binds to `0.0.0.0` for container networking
* Git SHA injected at build time via `--build-arg` and read from environment
---
 
### 2️⃣ Frontend (Nginx)
 
* Serves a styled HTML page with live data fetched from the backend
* Reverse proxies `/api/*` requests to the backend container
* Prevents browser from directly accessing the backend service
* Displays IP, backend status, pipeline steps, and architecture diagram
---
 
### 3️⃣ Docker Compose
 
* Orchestrates frontend + backend containers
* Creates isolated internal Docker network
* Enables service discovery by container name (`backend`)
* One‑command startup for the full system
---
 
## 🔁 CI/CD Pipeline (Core of This Project)
 
### Continuous Integration (CI)
 
Triggered automatically on every push to the `main` branch.
 
**Steps:**
 
1. Checkout repository
2. Build backend Docker image with `GIT_SHA` build arg
3. Build frontend Docker image
4. Start containers using Docker Compose
5. Wait for app with smart retry loop (no fragile `sleep`)
6. Test frontend — `curl --fail http://localhost`
7. Test `/api/status` endpoint
8. Test `/api/whoami` endpoint
9. Push verified images to Docker Hub tagged with **Git SHA + stable**
If **any step fails**, the pipeline stops.
 
---
 
### Artifacts
 
* Docker images are treated as **immutable artifacts**
* Images are tagged with both the **Git commit SHA** (immutable) and `stable` (floating)
* The registry is the **single source of truth**
* The Git SHA is baked into the image at build time and visible in the live UI
This prevents:
* "Works on my machine" problems
* Rebuilding different code during deployment
---
 
### Continuous Deployment (CD)
 
After CI succeeds:
 
* `docker-compose.yml` is copied to EC2 via `scp` on every deploy
* The same verified images are pulled on the **AWS EC2 instance**
* Deployment happens via **SSH automation** using `ssh-agent`
* Containers are restarted with zero manual intervention
Deployment is:
* Automated
* Reproducible
* Deterministic
---
 
## 🔐 Security Practices
 
* SSH key‑based authentication (no passwords)
* EC2 host IP stored as a GitHub Secret (not hardcoded)
* No secrets committed to the repository
* All secrets stored securely in GitHub Actions
---
 
## 🧪 Why This Matters
 
This project demonstrates **real production patterns**:
 
* CI ≠ CD
* Artifacts ≠ source code
* Deployment should use **already‑verified outputs**
* Build metadata (Git SHA) should be traceable all the way to production
* Automation must handle networking, permissions, and trust
Most beginner projects stop at "Docker runs locally".
 
This one goes all the way to:
 
> **push → build → test → package → deploy → live UI showing it all**
 
---
 
## ▶️ Run Locally
 
### Prerequisites
 
* Docker
* Docker Compose
### Start the application
 
```bash
docker compose up --build
```
 
### Access
 
* Frontend UI: [http://localhost](http://localhost)
* Backend: internal only (via Nginx reverse proxy at `/api/`)
### Test endpoints
 
```bash
curl http://localhost/api/whoami
curl http://localhost/api/status
curl http://localhost/api/pipeline
```
 
---
 
## 📂 Repository Structure
 
```
docker_project/
├── server.py               ← Python backend (4 endpoints)
├── Dockerfile              ← Backend image with GIT_SHA build arg
├── docker-compose.yml      ← Orchestration (uses image tags for EC2)
├── frontend/
│   ├── index.html          ← Live UI with IP, status, pipeline, architecture
│   ├── Dockerfile          ← Nginx image
│   └── default.conf        ← Nginx reverse proxy config
└── .github/
    └── workflows/
        └── ci.yml          ← Full CI/CD pipeline
```
 
---
 
## 🧠 Key Learnings
 
* Docker containers do **not** use `localhost` to talk to each other
* Reverse proxies are essential in real architectures
* CI runners are stateless — every job needs its own checkout
* Git SHA can be injected as a build arg and traced to production
* `docker-compose.yml` on the server must use `image:` not `build:`
* SSH automation has strict security requirements
* Real DevOps work involves debugging invisible edge cases
---
 
## 📌 Summary
 
This project showcases a **complete DevOps workflow**:
 
* Multi‑container Docker architecture with Nginx reverse proxy
* Automated CI with real HTTP integration tests
* Git SHA injected into every build and visible in production
* Immutable artifact creation and dual tagging strategy
* Secure CD to AWS EC2 via SSH with no manual steps
* Live UI that makes the entire pipeline visible to any user
It reflects **real engineering discipline**, not shortcut demos.
 
---
 
### 👤 Author
 
**Abhay Gehlot**
DevOps / Cloud Engineering
[github.com/abhaygehlot2005](https://github.com/abhaygehlot2005)
