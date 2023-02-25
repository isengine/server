@echo off
setlocal enableextensions enabledelayedexpansion

cd /d "%USERPROFILE%\AppData\Local" && (
    rem start "" "GitHubDesktop\GitHubDesktop.exe"
    start "" "insomnia\Insomnia.exe"
)

cd /d "%ProgramFiles%" && (
    start "" "Docker\Docker\Docker Desktop.exe"
    start "" "PostgreSQL\15\pgAdmin 4\bin\pgAdmin4.exe"
    start "" "Notepad++\notepad++.exe"
    start "" "Google\Chrome\Application\chrome.exe"
    start "" "totalcmd\TOTALCMD64.EXE"
)

rem cd /d "D:\dev" && (
rem     start "" "https://ya.ru"
rem )

cd /d "D:\dev" && (
    start "" "powershell"
    docker-compose up -d nginx
)

cd /d "%USERPROFILE%\AppData\Local" && (
    start "" "Programs\Microsoft VS Code\Code.exe" D:\dev
)

endlocal
exit /b 0
