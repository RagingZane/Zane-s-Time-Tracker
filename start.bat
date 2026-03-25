@echo off
cd /d "%~dp0"
start http://localhost:8080/time_tracker.html
start "Time Tracker Server" cmd /k node server.js
echo Server started in a new window. Close that window to stop the server.
