@echo off
echo ========================================================
echo Starting MeetIntel AI - FastAPI Core REST Engine
echo Documentation: http://127.0.0.1:8000/docs
echo ========================================================
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
pause
