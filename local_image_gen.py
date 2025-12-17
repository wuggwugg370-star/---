from __future__ import annotations

import random
import uuid
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from config import GENERATED_IMAGE_DIR, GEN_IMAGES_URL_PREFIX

# 预设的 Apple 风格渐变色板
GRADIENTS = [
    ((255, 154, 158), (254, 207, 239)),  # Warm Pink
    ((161, 140, 209), (251, 194, 235)),  # Purple Dream
    ((132, 250, 176), (143, 211, 244)),  # Ocean Blue
    ((255, 236, 210), (252, 182, 159)),  # Soft Orange
    ((224, 195, 252), (142, 197, 252)),  # Soft Violet
]

def _generate_gradient(width: int, height: int, start_color: tuple, end_color: tuple) -> Image.Image:
    """生成线性渐变背景"""
    base = Image.new('RGB', (width, height), start_color)
    top = Image.new('RGB', (width, height), end_color)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def generate_local_dish_image(name: str) -> str:
    """
    在本地生成一张带有菜品名称的精美图片。
    返回前端可访问的 URL 路径。
    """
    width, height = 800, 600
    
    # 随机选择一个渐变色
    c1, c2 = random.choice(GRADIENTS)
    img = _generate_gradient(width, height, c1, c2)
    draw = ImageDraw.Draw(img)

    # 尝试加载字体，如果失败则使用默认字体
    try:
        # 优先尝试系统中的无衬线字体 (Windows/Linux/Mac 路径不同，这里做简单尝试)
        # 实际部署时建议将字体文件放在项目目录中
        font_path = "arial.ttf" 
        # Mac 可能是 "/System/Library/Fonts/PingFang.ttc"
        font = ImageFont.truetype(font_path, 64)
    except OSError:
        font = ImageFont.load_default()

    # 绘制文字 (居中)
    text = name
    # 获取文字边界框
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    text_w = right - left
    text_h = bottom - top
    
    x = (width - text_w) / 2
    y = (height - text_h) / 2
    
    # 绘制轻微阴影
    draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0, 50))
    # 绘制白字
    draw.text((x, y), text, font=font, fill=(255, 255, 255))

    # 保存
    filename = f"img_{uuid.uuid4().hex[:8]}.png"
    save_path = GENERATED_IMAGE_DIR / filename
    img.save(save_path, quality=90)

    return f"{GEN_IMAGES_URL_PREFIX}/{filename}"