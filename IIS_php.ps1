Install-WindowsFeature -name Web-Server -IncludeManagementTools

# Install PHP
Invoke-WebRequest -Uri https://windows.php.net/downloads/releases/php-8.2.0-Win32-vs16-x64.zip -OutFile C:\php.zip
Expand-Archive -Path C:\php.zip -DestinationPath C:\php

# Create PHP test page
Set-Content -Path "C:\inetpub\wwwroot\index.php" -Value "<?php echo 'Hello from Windows VM via Azure Automation'; ?>"