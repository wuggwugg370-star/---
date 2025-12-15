@echo off
REM 一键启动：后端服务 + 浏览器前端客户端
cd /d %~dp0

REM 在新窗口中启动 Flask 服务端
start "OrderServer" /min cmd /c "cd /d %~dp0 && python server.py"

REM 简单等待几秒，确保服务端起来
timeout /t 3 >nul

REM 打开浏览器访问由 Flask 提供的前端页面
start "" "http://127.0.0.1:5000/"
exit


