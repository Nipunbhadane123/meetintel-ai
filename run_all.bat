@echo off
echo ========================================================
echo MeetIntel AI - Service Launcher
echo ========================================================
echo Select service to launch:
echo 1) Modern Next.js Web Application (Port 3000)
echo 2) Streamlit SaaS Interface (Port 8501)
echo 3) FastAPI Core Engine (Port 8000)
echo 4) Launch All (Web + Backend in separate windows)
echo ========================================================
set /p choice="Enter option [1-4]: "

if "%choice%"=="1" goto run_web
if "%choice%"=="2" goto run_streamlit
if "%choice%"=="3" goto run_backend
if "%choice%"=="4" goto run_all

:run_web
call run_web.bat
goto end

:run_streamlit
call run_streamlit.bat
goto end

:run_backend
call run_backend.bat
goto end

:run_all
start "MeetIntel FastAPI Backend" cmd /k run_backend.bat
start "MeetIntel Web App" cmd /k run_web.bat
goto end

:end
