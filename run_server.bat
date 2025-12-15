@echo off
REM 启动 HTTP 点餐服务端
cd /d %~dp0
python server.py
echo.
echo 如果上面有报错信息，请截图或复制给我。
pause


