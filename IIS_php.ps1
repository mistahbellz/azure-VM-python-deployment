Install-WindowsFeature -name Web-Server -IncludeManagementTools

# Create simple PHP page
Set-Content -Path "C:\inetpub\wwwroot\index.php" -Value "<?php echo 'Hello from Windows VM via Azure Automation'; ?>"
