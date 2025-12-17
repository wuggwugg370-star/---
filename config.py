from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

HOST = os.getenv("ORDER_APP_HOST", "127.0.0.1")
PORT = int(os.getenv("ORDER_APP_PORT", "5000"))

# 默认菜单
DEFAULT_MENU = {
    "宫保鸡丁": 28.0,
    "鱼香肉丝": 24.0,
    "麻婆豆腐": 22.0,
    "黑椒牛柳": 36.0,
    "香煎三文鱼": 58.0,
    "清炒时蔬": 18.0,
    "蟹粉狮子头": 42.0,
    "鲜虾云吞": 26.0,
    "牛油果沙拉": 32.0,
    "椰汁西米露": 16.0,
    "手工酸奶": 15.0,
    "柚子气泡水": 12.0,
    "法式焦糖布丁": 25.0,
    "宇治抹茶拿铁": 28.0,
    "葡萄柚冷萃茶": 22.0,
    "松露蘑菇浓汤": 38.0,
    "米饭": 3.0,
}

# CORS 配置
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ORDER_APP_ALLOWED_ORIGINS", "*").split(",")
    if origin.strip()
]

# 路径配置
MENU_DATA_FILE = DATA_DIR / "menu_data.json"
WEB_DIR = BASE_DIR / "web"

# 图片生成路径
GENERATED_IMAGE_DIR = WEB_DIR / "assets" / "dishes"
GEN_IMAGES_URL_PREFIX = "/assets/dishes"
GENERATED_IMAGE_DIR.mkdir(parents=True, exist_ok=True)