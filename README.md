# Practice DevOps App

## Goal -
A deliberately minimal Flask App, built as a vehicle to practice and demonstrate use of Docker, Kubernetes, Git Branching, and CI/CD - the app was made using ClaudeCode and it's functionality is intentionally trivial.

## Status - 
## Status - App has been Dockerized and deployed to a local Kubernetes cluster (Deployment, Service, ConfigMap, health probes). Self-healing and scaling tested. CI/CD not yet added.

## Tech stack
| Layer | Choice |
|-------|--------|
| Backend | Python (Flask) |
| Frontend | HTML/CSS/JS (inline) |

## Dockerizing
Wrote a Dockerfile from scratch (base image: python:3.14-slim, matching the local Python version). Built and ran the image locally, confirmed working via the homepage, live tip button, and health endpoint.

Key decisions:
- Copied requirements.txt separately, before the rest of the code, to take advantage of Docker's build caching — dependency installation only reruns when requirements.txt itself changes, not on every code edit.
- Used `imagePullPolicy: Never` later in Kubernetes since the image is loaded directly into Minikube rather than pushed to a registry.

## Kubernetes Deployment
Deployed the Dockerized app to a local Minikube cluster.

- Deployment: 3 replicas, with liveness and readiness probes (HTTP GET on `/`) built in from the start.
- Service: NodePort type, exposing the app for local browser access outside the cluster.
- ConfigMap: moved the hardcoded list of tips out of the application code into a ConfigMap, read via an environment variable at runtime — avoids needing to rebuild the image just to change display content.
- Secrets: not used in this project, since the app has no sensitive configuration (API keys, credentials) to manage.

Problems hit:
- The auto-generated service.yaml's selector incorrectly matched the Service's own name rather than the pods' actual label — had to manually correct it to `app: practice-devops-app`.
- After adding the ConfigMap and updating app.py to read from it, the running pods still used the old hardcoded version until the Docker image was rebuilt and reloaded into Minikube.

Tested and confirmed:
- Self-healing: deleted a pod manually, confirmed Kubernetes automatically created a replacement.
- Scaling: scaled replicas up (3→5) and down (5→2), confirmed pod count adjusted correctly both directions.
