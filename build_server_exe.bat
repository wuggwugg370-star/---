@echo off
REM 打包服务端为单文件 exe：dist\order_server.exe
cd /d %~dp0
python -m PyInstaller --onefile --name order_server server.py
echo.
echo 打包完成，如果没有报错，可在 dist\order_server.exe 中找到服务端程序。
pause


