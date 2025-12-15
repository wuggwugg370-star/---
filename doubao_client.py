from __future__ import annotations

import base64
import os
import re
import uuid
from pathlib import Path
from typing import Optional

import requests

from config import (
    DOUBAO_API_KEY,
    DOUBAO_API_URL,
    DOUBAO_IMAGE_SIZE,
    DOUBAO_MODEL_ID,
    DOUBAO_TIMEOUT,
    GEN_IMAGES_URL_PREFIX,
    GENERATED_IMAGE_DIR,
)


class DoubaoError(RuntimeError):
    """自定义异常，便于在 Flask 中统一返回。"""


def _slugify(name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()
    return slug or "dish"


def _ensure_key():
    if not DOUBAO_API_KEY:
        raise DoubaoError("未配置 DOUBAO_API_KEY，无法调用豆包图像接口")


def _download_to(path: Path, url: str):
    resp = requests.get(url, timeout=DOUBAO_TIMEOUT)
    resp.raise_for_status()
    path.write_bytes(resp.content)


def _decode_b64_to(path: Path, b64_data: str):
    path.write_bytes(base64.b64decode(b64_data))


def generate_dish_image(name: str, prompt: Optional[str] = None) -> str:
    """
    调用豆包（火山方舟）ImageGenerations 接口生成菜品图，返回可以直接在前端引用的相对路径。
    """
    _ensure_key()
    final_prompt = prompt or f"{name} 高端餐饮摄影，4K, soft light, detail, appetizing"

    headers = {
        "Authorization": f"Bearer {DOUBAO_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": DOUBAO_MODEL_ID,
        "prompt": final_prompt,
        "size": DOUBAO_IMAGE_SIZE,
        # 一些常用可选参数，可按需扩展
        "n": 1,
        "response_format": "url",
    }

    resp = requests.post(
        DOUBAO_API_URL,
        json=payload,
        headers=headers,
        timeout=DOUBAO_TIMEOUT,
    )
    if resp.status_code >= 400:
        raise DoubaoError(f"豆包接口调用失败：{resp.text}")

    data = resp.json()
    items = data.get("data") or []
    if not items:
        raise DoubaoError(f"豆包返回异常：{data}")

    entry = items[0]
    filename = f"{_slugify(name)}-{uuid.uuid4().hex[:8]}.png"
    output_path = GENERATED_IMAGE_DIR / filename

    if "url" in entry and entry["url"]:
        _download_to(output_path, entry["url"])
    elif "b64_json" in entry and entry["b64_json"]:
        _decode_b64_to(output_path, entry["b64_json"])
    else:
        raise DoubaoError("豆包返回数据中没有 url 或 b64_json 字段")

    return f"{GEN_IMAGES_URL_PREFIX}/{filename}"



