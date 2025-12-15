@echo off
REM 打包客户端为单文件 exe：dist\order_client.exe
cd /d %~dp0
python -m PyInstaller --onefile --name order_client client.py
echo.
echo 打包完成，如果没有报错，可在 dist\order_client.exe 中找到客户端程序。
pause


