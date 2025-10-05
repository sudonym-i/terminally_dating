Remove-Item -Path "challenge.py" -ErrorAction SilentlyContinue
New-Item -Path "challenge.py" -ItemType File -Force | Out-Null

Add-Content -Path "challenge.py" -Value $prompt

& code "challenge.py"