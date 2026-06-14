param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("blue", "green")]
    [string]$Target
)

$ErrorActionPreference = "Stop"
$service = "app_$Target"
$port = if ($Target -eq "blue") { 8001 } else { 8002 }
$current = (Get-Content "nginx/active-environment" -ErrorAction SilentlyContinue).Trim()

Write-Host "Ambiente actual: $current"
Write-Host "Candidato: $Target"

docker compose up -d --build $service

$healthy = $false
for ($attempt = 1; $attempt -le 30; $attempt++) {
    try {
        $health = Invoke-RestMethod "http://127.0.0.1:$port/health"
        $health | ConvertTo-Json -Compress | Write-Host
        $healthy = $true
        break
    }
    catch {
        Start-Sleep -Seconds 2
    }
}

if (-not $healthy) {
    throw "La version $Target no esta saludable. El trafico permanece en $current."
}

Copy-Item "nginx/$Target-upstream.inc" "nginx/active-upstream.inc" -Force
docker compose exec -T nginx nginx -t
docker compose exec -T nginx nginx -s reload
Set-Content "nginx/active-environment" $Target

Write-Host "Promocion completada: el trafico ahora apunta a $Target."
Invoke-RestMethod "http://127.0.0.1:8080/deployment" | ConvertTo-Json
