@echo off
echo Starting Natural Language to SQL Application (v2.0)...
echo.

echo Installing API dependencies...
cd ..\api
pip install -r config/requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install API dependencies
    pause
    exit /b 1
)

echo.
echo Starting API server...
start "API Server" cmd /k "python -m src.main"

cd ..\web
echo.
echo Installing Web dependencies...
npm install
if %errorlevel% neq 0 (
    echo Failed to install Web dependencies
    pause
    exit /b 1
)

echo.
echo Starting Web application...
timeout /t 3 /nobreak > nul
start "Web Application" cmd /k "npm start"

echo.
echo Both servers are starting...
echo API: http://localhost:8000
echo Web: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause > nul