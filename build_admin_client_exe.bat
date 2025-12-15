@echo off
REM 打包后台管理客户端为单文件 exe：dist\order_admin_client.exe
cd /d %~dp0
python -m PyInstaller --onefile --name order_admin_client admin_client.py
echo.
echo 打包完成，如果没有报错，可在 dist\order_admin_client.exe 中找到后台管理客户端程序。
pause


