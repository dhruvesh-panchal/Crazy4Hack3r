@echo off
:: Requires Administrator privileges.
:: Configures Windows so Nessus credentialed (authenticated) scans can succeed
:: and creates the local admin account used as the scan credential.
:: Based on Tenable's documented Windows credentialed-scan requirements.

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script must be run as Administrator.
    pause
    exit /b 1
)

echo.
echo === 1. Starting required services and setting them to Automatic ===
sc config RemoteRegistry start= auto
net start RemoteRegistry

sc config Winmgmt start= auto
net start Winmgmt

sc config LanmanServer start= auto
net start LanmanServer

sc config LanmanWorkstation start= auto
net start LanmanWorkstation

echo.
echo === 2. Disabling UAC remote restrictions for local accounts ===
:: Required if the Nessus scan account is a LOCAL admin account (not built-in
:: Administrator or a domain account). Without this, UAC filters the local
:: admin token on remote connections and WMI/registry auth will fail.
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v LocalAccountTokenFilterPolicy /t REG_DWORD /d 1 /f

echo.
echo === 3. Enabling File and Printer Sharing + Network Discovery firewall rules ===
netsh advfirewall firewall set rule group="File and Printer Sharing" new enable=yes
netsh advfirewall firewall set rule group="Network Discovery" new enable=yes
netsh advfirewall firewall set rule group="Windows Management Instrumentation (WMI)" new enable=yes

echo.
echo === 4. Setting network access model to Classic (not Guest-only) ===
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v ForceGuest /t REG_DWORD /d 0 /f

echo.
echo === 5. Turning off Windows Firewall for all profiles ===
netsh advfirewall set allprofiles state off

echo.
echo === 6. Creating the local scan credential account and granting admin rights ===
:: Creates user "admin1" and adds it to the local Administrators group.
net user admin1 Anjali@123 /add
net localgroup Administrators admin1 /add

echo.
echo Done. Windows Firewall is disabled on all profiles and the account
echo "admin1" is now a member of the local Administrators group. Use it
echo as the Nessus scan credential, then re-run the scan.
pause
