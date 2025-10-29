CI: Build and Push Docker Image to Docker Hub

This repository is preconfigured to build a production image with `Dockerfile.prod` and push it to Docker Hub via GitHub Actions.

1) Prerequisites
- Docker Hub account (e.g., `passang`).
- Docker Hub repository named `todo-flask` (create it in Docker Hub if needed).
- A GitHub repository containing this code.

2) Configure GitHub Secrets
Add repository secrets in GitHub → Settings → Secrets and variables → Actions → New repository secret:
- `DOCKERHUB_USERNAME`: your Docker Hub username (e.g., `passang`).
- `DOCKERHUB_TOKEN`: Docker Hub Access Token (Docker Hub → Account Settings → Security → New Access Token)..

3) Workflow File
The workflow lives at `.github/workflows/docker.yml`. It:
- Triggers on push to `main`.
- Logs in to Docker Hub using the secrets.
- Builds a multi-arch image from `Dockerfile.prod`.
- Tags and pushes to `docker.io/passang/todo-flask`.

If you fork/rename, update the `images:` field in the metadata step to match your Docker Hub repo.

4) Default Build Settings
- `context: .`
- `file: Dockerfile.prod`
- `platforms: linux/amd64,linux/arm64`
- Tags generated automatically by `docker/metadata-action` (latest + sha/semver when applicable).

5) How to Run the Workflow
- Push any commit to the `main` branch.
- Check progress at GitHub → Actions → “Build and Push Docker Image”.

6) Local Test (Optional)
Build and run the production image locally:
```
# Build
docker build -f Dockerfile.prod -t yeshey09/todo-flask:latest .

# Run
docker run --rm -p 8000:8000 --env-file .env.prod yeshey09/todo-flask:latest
```

7) Customize Tags (Optional)
To push a custom tag, edit `.github/workflows/docker.yml` and set in the metadata step:
```
with:
  images: yourhubuser/yourrepo
  tags: |
    type=raw,value=latest
    type=raw,value=prod
```

8) Troubleshooting
- denied: requested access to the resource is denied → Verify `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, and repo permissions.
- Workflow can’t find Dockerfile → Ensure `Dockerfile.prod` exists or update `file:` path.
- Build fails on dependencies → Rebuild locally and adjust `Dockerfile.prod` or `requirements.txt`.

9) Security Notes
- Keep the access token scoped minimally; rotate if leaked.
- Do not echo secrets in workflow logs.

After a successful run, the image is available at `docker.io/<DOCKERHUB_USERNAME>/todo-flask:latest`.




