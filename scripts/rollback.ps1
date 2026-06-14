$current = (Get-Content "nginx/active-environment").Trim()
$target = if ($current -eq "blue") { "green" } else { "blue" }
Write-Host "Rollback desde $current hacia $target"
& "$PSScriptRoot/promote.ps1" -Target $target
