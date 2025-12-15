from __future__ import annotations

import json
from pathlib import Path
from threading import Lock
from typing import Dict, List, Tuple, Any


class MenuStore:
    """线程安全的菜单存储，可选持久化到 JSON 文件。"""

    def __init__(self, data_file: Path, default_menu: Dict[str, float]):
        self._data_file = data_file
        self._lock = Lock()
        self._menu: Dict[str, Dict[str, Any]] = {}
        self._load(default_menu)

    @staticmethod
    def _normalize_entry(value: Any) -> Dict[str, Any]:
        if isinstance(value, dict):
            price = float(value.get("price", 0.0))
            image = value.get("image")
        else:
            price = float(value)
            image = None
        return {"price": price, "image": image}

    def _load(self, default_menu: Dict[str, float]):
        if self._data_file.exists():
            try:
                with self._data_file.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    self._menu = {
                        str(k): self._normalize_entry(v) for k, v in data.items()
                    }
                    return
            except (json.JSONDecodeError, OSError, ValueError):
                # 如果文件损坏，则回退到默认菜单
                pass
        self._menu = {str(k): self._normalize_entry(v) for k, v in default_menu.items()}
        self._save()

    def _save(self):
        try:
            with self._data_file.open("w", encoding="utf-8") as f:
                json.dump(self._menu, f, ensure_ascii=False, indent=2)
        except OSError:
            # 在嵌入式环境下可能没有写权限，忽略即可
            pass

    def get_menu(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            return {name: dict(payload) for name, payload in self._menu.items()}

    def upsert_item(self, name: str, price: float | None = None, image: str | None = None):
        with self._lock:
            record = self._menu.get(name, {"price": 0.0, "image": None})
            if price is not None:
                record["price"] = float(price)
            if image is not None:
                record["image"] = image
            self._menu[name] = record
            self._save()

    def delete_item(self, name: str) -> bool:
        with self._lock:
            if name in self._menu:
                del self._menu[name]
                self._save()
                return True
            return False

    def calc_order(self, items: List[str]) -> Tuple[float, List[str], List[Dict[str, float]]]:
        total = 0.0
        not_found: List[str] = []
        detail = []
        with self._lock:
            for name in items:
                record = self._menu.get(name)
                if not record:
                    not_found.append(name)
                else:
                    price = float(record.get("price", 0.0))
                    total += price
                    detail.append({"name": name, "price": price})
        return total, not_found, detail
