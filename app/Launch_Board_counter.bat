# When running on Windows
cd C:\Users\nimod\Documents\Board_counter

docker start board_counter
timeout /nobreak /t 2 >nul

start chrome.exe http://127.0.0.1:8000/docs
