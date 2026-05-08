# Install IIS + the CGI feature
Install-WindowsFeature -name Web-Server, Web-CGI -IncludeManagementTools

# To Download the NTS
$phpZip = "C:\php.zip"
$phpDir = "C:\php"
Invoke-WebRequest -Uri "https://php.net" -OutFile $phpZip

# Extract PHP
if (!(Test-Path $phpDir)) { New-Item -ItemType Directory -Path $phpDir }
Expand-Archive -Path $phpZip -DestinationPath $phpDir -Force

# PHP file handler in IIS server
Import-Module WebAdministration
New-WebHandler -Name "PHP_via_FastCGI" `
    -Path "*.php" `
    -Verb "*" `
    -Modules "FastCgiModule" `
    -ScriptProcessor "$phpDir\php-cgi.exe" `
    -ResourceType "Either"

# Set index.php as homepage
Add-WebConfigurationProperty -pspath 'MACHINE/WEBROOT/APPHOST' `
    -filter "system.webServer/defaultDocument/files" `
    -name "." -value @{value = 'index.php' }

# PHP test file
$content = "<?php echo '<h1>Hello from Windows VM via Azure Automation</h1>'; phpinfo(); ?>"
Set-Content -Path "C:\inetpub\wwwroot\index.php" -Value $content


Remove-Item "C:\inetpub\wwwroot\iisstart.htm" -Force

# Restart IIS to apply all changes
Restart-Service W3SVC
