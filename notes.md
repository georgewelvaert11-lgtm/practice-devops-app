08/09/26 - Git Hub set up. Dockerfile written, image built and ran to make a container.
Then will commit to Dockerize branch before merging with main branch and pushing to GitHub repo.

## Kubernetes Deployment
- Wrote deployment.yaml (used kubectl create --dry-run to generate a starting template, corrected image name, added imagePullPolicy: Never, ports, liveness/readiness probes)
- Wrote service.yaml (used kubectl create --dry-run, had to fix selector - auto-generated version incorrectly matched the service's own name instead of the pod label)
- Both applied successfully, then i confirmed that the app was reachable via minikube service --url

## ConfigMap
- Created ConfigMap object
- Moved hardcoded TIPS list out of app.py into a ConfigMap (practice-devops-config)
- Used | as delimiter to store multiple tips as one string, split back into a list in app.py
- Referenced via envFrom.configMapRef in deployment.yaml
- Required rebuilding the Docker image (due to the fact that app.py changed) and reloading into Minikube before the change took effect

## Testing
- Self-healing: deleted a pod, confirmed Kubernetes automatically created a replacement
- Scaling: scaled replicas 3 → 5 → 2, confirmed pod count adjusted correctly both directions
