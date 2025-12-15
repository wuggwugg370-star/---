@echo off
REM 启动 HTTP 点餐系统后台管理客户端
cd /d %~dp0
python admin_client.py
echo.
echo 如果上面有报错信息，请截图或复制给我。
pause


