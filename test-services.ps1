Write-Host "Testing TaskFlow services through NGINX..." -ForegroundColor Green

# Wait for services to start
Write-Host "Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Test NGINX health
Write-Host "Testing NGINX health..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost/nginx-health" -Method GET
    Write-Host "✅ NGINX: $response" -ForegroundColor Green
} catch {
    Write-Host "❌ NGINX: $_" -ForegroundColor Red
}

# Test Auth Service through NGINX
Write-Host "Testing Auth Service through NGINX..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost/auth/health" -Method GET
    Write-Host "✅ Auth Service: $($response | ConvertTo-Json)" -ForegroundColor Green
} catch {
    Write-Host "❌ Auth Service: $_" -ForegroundColor Red
}

# Test Projects Service through NGINX
Write-Host "Testing Projects Service through NGINX..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost/projects/health" -Method GET
    Write-Host "✅ Projects Service: $($response | ConvertTo-Json)" -ForegroundColor Green
} catch {
    Write-Host "❌ Projects Service: $_" -ForegroundColor Red
}

Write-Host "Testing completed!" -ForegroundColor Green