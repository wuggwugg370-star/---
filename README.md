## 点餐系统（前后端分离 · 可产品化部署）

> 现代化的点餐演示项目，提供 Flask API、命令行客户端、苹果官网质感的 Web UI、PyInstaller 打包脚本以及 nginx 部署示例。

---

### 1. 目录速览

- `server.py`：Flask 应用（REST API + 可选本地静态托管）
- `config.py`：运行配置（端口、默认菜单、CORS、持久化路径等）
- `menu_store.py`：线程安全且可持久化的菜单存储
- `client.py` / `admin_client.py`：命令行客户端（点餐 & 后台管理）
- `web/`：全新重制的 Web 前端，极简 Apple 风
- `run_*.bat` / `build_*.bat`：开发期一键运行 & Windows exe 打包脚本

---

### 2. 环境准备

```bash
# 1) 安装 Python 3.9+
# 2) 安装依赖
pip install -r requirements.txt
```

#### 豆包（Doubao）AI 图像生成配置

若要在后台一键生成菜品图片，需要在系统环境变量里提供豆包接口信息：

| 变量名 | 说明 | 默认值 |
| --- | --- | --- |
| `DOUBAO_API_KEY` | **必填**，在火山方舟控制台申请的 API Key | 无 |
| `DOUBAO_API_URL` | ImageGenerations REST 接口地址 | `https://ark.cn-beijing.volces.com/api/v3/images/generations` |
| `DOUBAO_MODEL_ID` | 模型 ID，例如 `image-creation` | `image-creation` |
| `DOUBAO_IMAGE_SIZE` | 输出尺寸，比如 `512x512` | `512x512` |

设置示例（PowerShell）：

```powershell
$env:DOUBAO_API_KEY="替换成你的key"
```

可选：如需打包 exe，再安装 PyInstaller：

```bash
python -m pip install pyinstaller
```

---

### 3. 后端（Flask API）

#### 启动

```bash
python server.py
# 或： ORDER_APP_PORT=8000 python server.py
```

内置特性：

- `config.py` 控制 HOST / PORT / 默认菜单 / 菜单持久化路径
- 菜单自动持久化到 `data/menu_data.json`
- 自带 `/healthz` 探针、统一错误响应、CORS（可配置允许域名）
- 可作为 WSGI 应用导入：`from server import app` / `create_app()`

#### API 一览

| 方法 | 路径              | 说明                       |
| ---- | ----------------- | -------------------------- |
| GET  | `/menu`           | 获取菜单                   |
| POST | `/order`          | 下单，JSON `{items: [...]}`|
| POST/PUT | `/admin/menu` | 新增或更新菜品（支持 price / image） |
| DELETE | `/admin/menu/<name>` | 删除菜品             |
| POST | `/admin/menu/<name>/ai-image` | 调用豆包接口生成菜品图片 |
| GET  | `/healthz`        | 健康检查                   |

---

### 4. 前端（Web / Apple 官网风格）

- 所有源码位于 `web/index.html`，纯静态文件即可部署。
- JS 通过 `API_BASE` 调用后端接口，默认同域（适合 nginx 反代）。

#### 本地开发

```bash
# 方式一：后端托管（推荐）
python server.py
浏览器访问 http://127.0.0.1:5000

# 方式二：独立静态服务器
cd web && python -m http.server 8000
# 将 index.html 中的 API_BASE 改成 http://127.0.0.1:5000
```

#### 生产部署（示例 nginx）

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 1) 静态前端
    root /opt/order-app/web;
    index index.html;

    # 2) 反向代理 API
    location /menu        { proxy_pass http://127.0.0.1:5000/menu; }
    location /order       { proxy_pass http://127.0.0.1:5000/order; }
    location /admin/menu  { proxy_pass http://127.0.0.1:5000/admin/menu; }
    location /healthz     { proxy_pass http://127.0.0.1:5000/healthz; }
}
```

如果前后端使用不同域名，请在 `config.py` 中配置 `ORDER_APP_ALLOWED_ORIGINS` 或设置环境变量，开放对应 CORS。

---

### 5. 命令行客户端（可打包 exe）

```bash
python client.py        # 点餐
python admin_client.py  # 管理菜单 & 触发 AI 生成图片
```

若需直接双击，可使用：

- `run_client.bat` / `run_admin_client.bat`
- 打包脚本：`build_client_exe.bat` / `build_admin_client_exe.bat`

（生成的 exe 在 `dist/` 目录，可分发给无 Python 环境的用户）

---

### 6. 一键体验（可选）

- `run_server.bat`：仅启动后端 API。
- `start_web_client.bat`：开发期快速体验，后台拉起后端并自动打开浏览器。

> 生产环境请还是将前端部署在 nginx / CDN 上，后端使用 `python server.py` 或 `gunicorn server:app`。

---

### 7. 打包 & 发布

```bash
build_server_exe.bat
build_client_exe.bat
build_admin_client_exe.bat

# 输出
dist/
  ├─ order_server.exe
  ├─ order_client.exe
  └─ order_admin_client.exe
```

把 `dist` 目录里的 exe + `data/menu_data.json`（如果有自定义菜单）一起发布即可。

---

### 8. 下一步可以做什么？

- 接入登录/权限，将后台接口限制给管理员
- 换成数据库（SQLite / Postgres）管理菜单与订单
- 引入消息推送、厨房屏、实时订单状态等
- 使用 Docker / k8s 镜像部署
- 扩展豆包请求参数（风格、参考图、分辨率）或接入其他国内模型

当前版本已经具备“开箱即用 + 产品化”特性，可直接 demo / 教学 / 快速原型展示。祝使用愉快 🚀
