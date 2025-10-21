Write-Host "Deploying TaskFlow to Docker Swarm..." -ForegroundColor Green

# Build images
Write-Host "Building Docker images..." -ForegroundColor Yellow
docker-compose build

# Initialize swarm if not already initialized
Write-Host "Initializing Docker Swarm..." -ForegroundColor Yellow
docker swarm init --advertise-addr 127.0.0.1

# Deploy stack
Write-Host "Deploying stack..." -ForegroundColor Yellow
docker stack deploy -c docker-stack.yml taskflow

Write-Host "Deployment completed!" -ForegroundColor Green
Write-Host "Check services with: docker service ls" -ForegroundColor Cyan
Write-Host "Check stack with: docker stack ps taskflow" -ForegroundColor Cyan