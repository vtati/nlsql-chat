@echo off
echo Testing Natural Language to SQL Application...
echo.

echo Testing API database connections...
cd api
python scripts/test_connections.py
if %errorlevel% neq 0 (
    echo API database tests failed
    pause
    exit /b 1
)

echo.
echo Setting up database...
python scripts/setup_database.py
if %errorlevel% neq 0 (
    echo Database setup failed
    pause
    exit /b 1
)

echo.
echo Testing API endpoints...
curl -f http://localhost:8000/health > nul 2>&1
if %errorlevel% neq 0 (
    echo API server is not running. Please start it first.
    pause
    exit /b 1
)

echo API health check: OK
curl -f http://localhost:8000/database-info > nul 2>&1
if %errorlevel% equ 0 (
    echo Database info endpoint: OK
) else (
    echo Database info endpoint: FAILED
)

echo.
echo All tests completed!
pause