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
for /f "tokens=*" %%A in ('whoami') do set "LOGGEDUSER=%%A"

:: --- Collect first IPv4 address ---
set "IPADDR="
for /f "tokens=2 delims=:" %%A in ('ipconfig ^| findstr /R /C:"IPv4 Address"') do (
    if not defined IPADDR (
        set "IPADDR=%%A"
        set "IPADDR=!IPADDR: =!"
    )
)

:: --- Collect first physical (MAC) address ---
set "MACADDR="
for /f "tokens=1,* delims=:" %%A in ('getmac /fo list /v ^| findstr /C:"Physical Address"') do (
    if not defined MACADDR (
        set "MACADDR=%%B"
        set "MACADDR=!MACADDR: =!"
    )
)

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
echo Hostname........ %HOSTNAME%
echo Logged In User.. %LOGGEDUSER%
echo IP Address...... %IPADDR%
echo MAC Address..... %MACADDR%
echo.
pause
