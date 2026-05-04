# 🚀 Dockerized Multi‑Container Application with CI/CD Deployment

This repository demonstrates a **real‑world DevOps pipeline** that takes code from a GitHub push all the way to **automatic deployment on an AWS EC2 server**.

The focus is **system correctness, reproducibility, and automation** — not toy examples.

---

## 🧠 What This Project Proves

* You understand **how CI and CD are different — and how they work together**
* You can build **immutable artifacts** (Docker images)
* You can deploy **the exact same artifact** that passed CI
* You can automate deployments **securely using SSH**
* You can debug real‑world DevOps issues (networking, SSH, permissions, CI runners)

This is **job‑ready DevOps work**, not tutorial code.

---

## 🏗️ Architecture Overview

```
Browser
   ↓
Frontend (Nginx container)
   ↓   (Docker internal network)
Backend (Python HTTP server container)
```

* Browser talks **only to the frontend**
* Nginx acts as a **reverse proxy**
* Backend is **not exposed publicly**
* Containers communicate via **Docker internal networking**

---

## 🧩 Application Components

### 1️⃣ Backend (Python)

* Lightweight HTTP server using Python
* Runs inside a Docker container
* Exposes:

  * `/` → basic response
  * `/whoami` → returns client IP
* Binds to `0.0.0.0` for container networking

---

### 2️⃣ Frontend (Nginx)

* Serves static HTML
* Uses **reverse proxy** to forward API calls to backend
* Prevents browser from directly accessing backend service

---

### 3️⃣ Docker Compose

* Orchestrates frontend + backend containers
* Creates isolated internal Docker network
* Enables service discovery by container name
* One‑command startup for the full system

---

## 🔁 CI/CD Pipeline (Core of This Project)

### Continuous Integration (CI)

Triggered automatically on every push to the `main` branch.

CI performs **verification only** — no deployment.

**Steps:**

1. Checkout repository
2. Build backend Docker image
3. Build frontend Docker image
4. Start containers using Docker Compose
5. Run real HTTP checks against the running system
6. Push verified Docker images to Docker Hub

If **any step fails**, the pipeline stops.

---

### Artifacts

* Docker images are treated as **immutable artifacts**
* Images are tagged using the **Git commit SHA**
* The registry becomes the **single source of truth**

This prevents:

* "Works on my machine" problems
* Rebuilding different code during deployment

---

### Continuous Deployment (CD)

After CI succeeds:

* The same verified images are deployed to an **AWS EC2 instance**
* Deployment happens via **SSH automation** (no passwords)
* Uses `ssh-agent` to securely load private keys in CI
* Containers are restarted using Docker Compose

Deployment is:

* Automated
* Reproducible
* Deterministic

---

## 🔐 Security Practices

* SSH key‑based authentication (no passwords)
* Separate **public/private key roles**
* No secrets committed to the repository
* Secrets stored securely in GitHub Actions

---

## 🧪 Why This Matters

This project demonstrates **real production patterns**:

* CI ≠ CD
* Artifacts ≠ source code
* Deployment should use **already‑verified outputs**
* Automation must handle networking, permissions, and trust

Most beginner projects stop at "Docker runs locally".

This one goes all the way to:

> **push → verify → package → deploy**

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

* Frontend: [http://localhost:8080](http://localhost:8080)
* Backend: internal only (via frontend proxy)

---

## 📂 Repository Structure

```
docker_project/
├── server.py
├── Dockerfile
├── docker-compose.yml
├── frontend/
│   ├── index.html
│   ├── Dockerfile
│   └── default.conf
└── .github/
    └── workflows/
        └── ci.yml
```

---

## 🧠 Key Learnings

* Docker containers do **not** use `localhost` to talk to each other
* Reverse proxies are essential in real architectures
* CI runners behave differently from local machines
* SSH automation has strict security requirements
* Real DevOps work involves debugging invisible edge cases

---

## 📌 Summary

This project showcases a **complete DevOps workflow**:

* Multi‑container Docker architecture
* Automated CI verification
* Immutable artifact creation
* Secure CD to cloud infrastructure

It reflects **real engineering discipline**, not shortcut demos.

---

### 👤 Author

**Abhay Gehlot**
DevOps / Cloud Engineering
