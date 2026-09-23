@echo off
setlocal enabledelayedexpansion

:: ---------------------------------------------------------------
:: SystemInfoLogger.bat
:: Logs Hostname, Logged-in User, IP Address and MAC Address into
:: a CSV file (opens fine in Excel) sitting next to this script.
:: Must be run "as Administrator". Skips duplicate entries.
:: ---------------------------------------------------------------

:: Require administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script must be run as Administrator.
    echo Right-click SystemInfoLogger.bat and choose "Run as administrator".
    pause
    exit /b 1
)

set "OUTFILE=%~dp0SystemInventory.csv"

:: Create the file with a header row if it does not exist yet
if not exist "%OUTFILE%" (
    echo Timestamp,Hostname,LoggedInUser,IPAddress,MACAddress> "%OUTFILE%"
)

:: --- Collect Hostname ---
set "HOSTNAME=%COMPUTERNAME%"

:: --- Collect logged in user ---
for /f "usebackq delims=" %%A in (`whoami`) do set "LOGGEDUSER=%%A"

:: --- Collect first active IPv4 address via PowerShell (locale independent) ---
set "IPADDR="
for /f "usebackq delims=" %%A in (`powershell -NoProfile -ExecutionPolicy Bypass -Command "try { (Get-NetIPAddress -AddressFamily IPv4 -ErrorAction Stop ^| Where-Object { $_.IPAddress -notlike '169.254.*' -and $_.InterfaceAlias -notmatch 'Loopback' } ^| Select-Object -First 1 -ExpandProperty IPAddress) } catch { 'PS_ERROR: ' + $_.Exception.Message }"`) do set "IPADDR=%%A"

:: --- Collect first active MAC address via PowerShell (locale independent) ---
set "MACADDR="
for /f "usebackq delims=" %%A in (`powershell -NoProfile -ExecutionPolicy Bypass -Command "try { (Get-NetAdapter -ErrorAction Stop ^| Where-Object { $_.Status -eq 'Up' } ^| Select-Object -First 1 -ExpandProperty MacAddress) } catch { 'PS_ERROR: ' + $_.Exception.Message }"`) do set "MACADDR=%%A"

if not defined IPADDR set "IPADDR=UNKNOWN"
if not defined MACADDR set "MACADDR=UNKNOWN"

:: --- Debug: show exactly what was captured, including any PowerShell error text ---
echo ---------------------------------------------
echo Captured values:
echo   Hostname   = %HOSTNAME%
echo   User       = %LOGGEDUSER%
echo   IPAddress  = %IPADDR%
echo   MACAddress = %MACADDR%
echo ---------------------------------------------
echo.

:: --- Check whether this exact entry already exists ---
set "FOUND=0"
findstr /C:",%HOSTNAME%,%LOGGEDUSER%,%IPADDR%,%MACADDR%" "%OUTFILE%" >nul 2>&1
if %errorlevel%==0 set "FOUND=1"

if "%FOUND%"=="1" (
    echo Entry already exists in %OUTFILE%. No new record added.
) else (
    set "TIMESTAMP=%date% %time%"
    echo !TIMESTAMP!,%HOSTNAME%,%LOGGEDUSER%,%IPADDR%,%MACADDR%>> "%OUTFILE%"
    echo New entry added to %OUTFILE%.
)

echo.
pause
