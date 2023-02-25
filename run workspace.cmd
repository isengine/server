@echo off
setlocal enableextensions enabledelayedexpansion

cd /d "%USERPROFILE%\AppData\Local" && (
    rem start "" /min "GitHubDesktop\GitHubDesktop.exe"
    start "" /min "insomnia\Insomnia.exe"
)

cd /d "%ProgramFiles%" && (
    start "" /min "Docker\Docker\Docker Desktop.exe"
    start "" /min "PostgreSQL\15\pgAdmin 4\bin\pgAdmin4.exe"
    start "" /max "Notepad++\notepad++.exe"
    start "" /max "Google\Chrome\Application\chrome.exe"
    start "" /max "totalcmd\TOTALCMD64.EXE"
)

rem cd /d "D:\dev" && (
rem     start "" "https://ya.ru"
rem )

cd /d "D:\dev" && (
    start "" "powershell"
    docker-compose up -d nginx
)

cd /d "%USERPROFILE%\AppData\Local" && (
    start "" /max "Programs\Microsoft VS Code\Code.exe" D:\dev
)

endlocal
exit /b 0
