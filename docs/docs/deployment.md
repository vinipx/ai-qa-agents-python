# Deployment & CI/CD

QORE is designed to be easily deployed to modern cloud environments and integrated into enterprise CI/CD pipelines.

## Containerization

QORE provides a multi-stage `docker-compose.yml` for production-grade deployments.

```bash
docker-compose up --build -d
```

### API Service
- **Base Image:** `python:3.10-slim`
- **Port:** `8000`
- **Volume:** Mounts `checkpoints.sqlite` for persistent storage.

### UI Service
- **Base Image:** `node:20-alpine`
- **Port:** `3000`
- **Environment:** Needs `NEXT_PUBLIC_API_URL` if the API is hosted on a different domain.

---

## GitHub Pages Deployment (Docs)

The QORE Documentation site is optimized for GitHub Pages. 

### Manual Deploy
```bash
cd docs
npm run build
npm run deploy
```

### Automated CI (GitHub Actions)
We recommend the following workflow structure:
1.  **Trigger:** On push to `main`.
2.  **Build:** Run `npm install` and `npm run build` in the `docs` directory.
3.  **Action:** Use `peaceiris/actions-gh-pages` to push the `build/` directory to the `gh-pages` branch.

---

## Pipeline Integration

You can trigger QORE orchestrations as part of your CI pipeline via the `/execute` REST endpoint.

### Example: Jenkins/GitHub Actions Step
```bash
curl -X POST http://qore-api:8000/execute \
     -H "Content-Type: application/json" \
     -d '{"requirement": "Review recent commits for performance regressions", "thread_id": "CI-BUILD-42"}'
```

:::warning Persistence Note
In production, we recommend using a persistent volume for the SQLite database or migrating to a managed Postgres instance to ensure state is shared across multiple API instances.
:::
