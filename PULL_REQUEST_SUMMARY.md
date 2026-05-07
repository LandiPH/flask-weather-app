# Pull Request: Add Dockerfile and GitHub Actions CI/CD Pipeline

## Summary
This PR introduces containerization and automated CI/CD deployment for the Flask weather application. It includes a production-ready Dockerfile with multi-stage builds, comprehensive Docker configuration files, and a GitHub Actions workflow for automated testing and Docker Hub deployment.

## Changes

### Files Added

#### 1. **Dockerfile**
- Multi-stage build approach (builder + runtime stages)
- Optimized image size using `python:3.11-slim` base image
- Non-root user execution for enhanced security
- Health check endpoint configured
- Layer caching optimization

#### 2. **.github/workflows/docker-ci-cd.yml**
- Automated CI/CD pipeline triggered on push to `main` and pull requests
- **Test stage**: Runs pytest on all commits
- **Build stage**: Builds Docker image using Docker Buildx
- **Push stage**: Pushes to Docker Hub only on `main` branch pushes
- Image tagging: `latest` and commit SHA for version control
- GitHub Actions cache integration for faster builds

#### 3. **.dockerignore**
- Excludes unnecessary files from build context
- Reduces image size and build time
- Ignores: `.git`, `__pycache__`, `.env`, tests, documentation, etc.

#### 4. **docker-compose.yml**
- Local development orchestration
- Service configuration for Flask app
- Port mapping and environment variables
- Health check configuration
- Restart policy

#### 5. **test_app.py**
- Unit tests for all API endpoints
- Tests: home, health check, status, weather, invalid city handling
- Pytest-compatible test suite

#### 6. **requirements.txt** (Updated)
- Flask 3.0.0
- requests 2.31.0
- Werkzeug 3.0.1

#### 7. **.gitignore**
- Standard Python exclusions
- Virtual environment paths
- IDE configuration directories
- Compiled Python files

## Key Features

### Security
- Non-root user (`appuser`) runs the container
- Minimal base image reduces attack surface
- No sensitive data in image layers

### Performance
- Multi-stage build reduces final image size
- Layer caching optimization
- GitHub Actions cache for faster CI/CD builds

### Developer Experience
- Local development with `docker-compose up`
- Automated testing on every commit
- Automatic Docker Hub deployment
- Clear error messages and health checks

## Testing
All tests pass successfully:
- ✓ Home endpoint returns correct JSON
- ✓ Health check endpoint returns 200
- ✓ Status endpoint returns running status
- ✓ Invalid city queries handled correctly
- ✓ Valid city weather requests functional

## Deployment
The workflow automates:
1. **Code checkout** from GitHub
2. **Dependency installation** and testing
3. **Docker image build** with Buildx
4. **Docker Hub authentication** using secrets
5. **Image push** with `latest` and commit SHA tags
6. **Artifact caching** for faster subsequent builds

## Prerequisites for Deployment
To enable Docker Hub deployment, configure these GitHub secrets:
- `DOCKERHUB_USERNAME`: Your Docker Hub username
- `DOCKERHUB_TOKEN`: Docker Hub personal access token (from hub.docker.com/settings/security)

## Build Information
- **Base Image**: `python:3.11-slim`
- **Working Directory**: `/app`
- **Port**: 5000
- **Health Check**: `GET /health` endpoint

## How to Use

### Local Development
```bash
docker-compose up
curl http://localhost:5000/health
```

### Manual Build
```bash
docker build -t flask-weather-app:latest .
docker run -p 5000:5000 flask-weather-app:latest
```

### Automatic Deployment
Push to `main` branch → GitHub Actions automatically tests, builds, and pushes to Docker Hub

## Related Issues
Closes: N/A

## Checklist
- [x] Code follows project style guidelines
- [x] Tests pass locally and in CI
- [x] Dockerfile uses security best practices
- [x] Documentation is clear and complete
- [x] No hardcoded secrets in configuration files
- [x] Image builds and runs successfully
- [x] GitHub Actions workflow executes without errors

## Notes
- First-time setup requires Docker Hub credentials in GitHub Secrets
- Workflow runs on every push to `main` and pull requests
- Images are tagged with both `latest` and commit SHA for version tracking
- Multi-stage build significantly reduces final image size compared to single-stage approach
