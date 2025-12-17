from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

HOST = os.getenv("ORDER_APP_HOST", "127.0.0.1")
PORT = int(os.getenv("ORDER_APP_PORT", "5000"))

# === 升级版默认菜单 ===
DEFAULT_MENU = {
    # --- 招牌热菜 ---
    "宫保鸡丁": 28.0,
    "鱼香肉丝": 24.0,
    "麻婆豆腐": 22.0,
    "黑椒牛柳": 46.0,
    "香煎三文鱼": 68.0,
    "红烧肉": 48.0,
    "水煮鱼": 58.0,
    "糖醋排骨": 38.0,
    "清蒸鲈鱼": 52.0,
    "蒜蓉粉丝扇贝": 36.0,

    # --- 精致冷盘 & 小食 ---
    "蟹粉狮子头": 42.0,
    "鲜虾云吞": 26.0,
    "口水鸡": 32.0,
    "凉拌海蜇皮": 28.0,
    "夫妻肺片": 35.0,
    "炸春卷": 18.0,

    # --- 健康时蔬 ---
    "清炒时蔬": 18.0,
    "牛油果沙拉": 32.0,
    "干煸四季豆": 20.0,
    "上汤娃娃菜": 22.0,
    "白灼芥兰": 18.0,

    # --- 主食 ---
    "扬州炒饭": 26.0,
    "干炒牛河": 28.0,
    "招牌牛肉面": 32.0,
    "米饭": 3.0,

    # --- 甜品 & 饮品 ---
    "椰汁西米露": 16.0,
    "手工酸奶": 15.0,
    "柚子气泡水": 12.0,
    "法式焦糖布丁": 25.0,
    "宇治抹茶拿铁": 28.0,
    "葡萄柚冷萃茶": 22.0,
    "杨枝甘露": 26.0,
    "松露蘑菇浓汤": 38.0,
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

# 图片生成路径 (保持原样，用于兼容)
GENERATED_IMAGE_DIR = WEB_DIR / "assets" / "dishes"
GEN_IMAGES_URL_PREFIX = "/assets/dishes"
GENERATED_IMAGE_DIR.mkdir(parents=True, exist_ok=True)