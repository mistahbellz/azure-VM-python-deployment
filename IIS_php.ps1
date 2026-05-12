l
# Install IIS + CGI
Install-WindowsFeature -Name Web-Server, Web-CGI -IncludeManagementTools

# Variables
$phpZip = "C:\php.zip"
$phpDir = "C:\php"

# Download PHP for Windows (CORRECT ZIP FILE)
Invoke-WebRequest `
    -Uri "https://windows.php.net/downloads/releases/php-8.2.28-nts-Win32-vs16-x64.zip" `
    -OutFile $phpZip

# Create PHP directory
if (!(Test-Path $phpDir)) {
    New-Item -ItemType Directory -Path $phpDir
}

# Extract PHP
Expand-Archive -Path $phpZip -DestinationPath $phpDir -Force

# Add PHP to PATH
[Environment]::SetEnvironmentVariable(
    "Path",
    $env:Path + ";C:\php",
    [EnvironmentVariableTarget]::Machine
)

# Register PHP with IIS
Import-Module WebAdministration

New-WebHandler `
    -Name "PHP_via_FastCGI" `
    -Path "*.php" `
    -Verb "*" `
    -Modules "FastCgiModule" `
    -ScriptProcessor "C:\php\php-cgi.exe" `
    -ResourceType Either

# Configure FastCGI
Add-WebConfiguration `
    "/system.webServer/fastCgi" `
    -Value @{
    fullPath = "C:\php\php-cgi.exe"
}

# Set index.php as default page
Add-WebConfigurationProperty `
    -pspath 'MACHINE/WEBROOT/APPHOST' `
    -filter "system.webServer/defaultDocument/files" `
    -name "." `
    -value @{value = 'index.php' }

# Remove IIS default page
Remove-Item "C:\inetpub\wwwroot\iisstart.htm" -Force -ErrorAction SilentlyContinue

# Create PHP test page
$content = "<?php echo '<h1>Hello from Windows VM via Azure Automation</h1>'; phpinfo(); ?>"
Set-Content `
    -Path "C:\inetpub\wwwroot\index.php" `
    -Value $content

# Restart IIS
iisreset

Write-Host "✅ IIS + PHP configured successfully"

