@echo off
cd /d "%~dp0"
start http://localhost:8080/time_tracker.html
node server.js