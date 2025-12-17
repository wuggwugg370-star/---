from __future__ import annotations

import logging
from flask import Flask, jsonify, request
from flask_cors import CORS

from config import (
    ALLOWED_ORIGINS,
    DEFAULT_MENU,
    HOST,
    MENU_DATA_FILE,
    PORT,
    WEB_DIR,
)
# 替换引入
from local_image_gen import generate_local_dish_image
from menu_store import MenuStore


def create_app() -> Flask:
    app = Flask(__name__, static_folder=str(WEB_DIR), static_url_path="")

    if ALLOWED_ORIGINS == ["*"]:
        CORS(app)
    else:
        CORS(app, resources={r"/*": {"origins": ALLOWED_ORIGINS}})

    store = MenuStore(MENU_DATA_FILE, DEFAULT_MENU)

    @app.route("/", methods=["GET"])
    def index_page():
        return app.send_static_file("index.html")

    @app.route("/healthz", methods=["GET"])
    def healthz():
        return jsonify({"status": "ok"})

    @app.route("/menu", methods=["GET"])
    def get_menu():
        return jsonify({"status": "ok", "menu": store.get_menu()})

    @app.route("/order", methods=["POST"])
    def order():
        data = request.get_json(silent=True) or {}
        items = data.get("items")
        if not isinstance(items, list) or not items:
            return jsonify({"status": "error", "message": "点餐列表不能为空"}), 400

        total, not_found, detail = store.calc_order(items)
        if not_found:
            return jsonify({
                "status": "error",
                "message": f"以下菜品不存在：{', '.join(not_found)}"
            }), 400

        return jsonify({
            "status": "ok",
            "message": "点餐成功",
            "total": total,
            "detail": detail,
        })

    @app.route("/admin/menu", methods=["POST", "PUT"])
    def admin_set_item():
        data = request.get_json(silent=True) or {}
        name = data.get("name")
        price = data.get("price")
        image = data.get("image")
        
        if not name:
            return jsonify({"status": "error", "message": "需要提供 name"}), 400
            
        parsed_price = None
        if price is not None:
            try:
                parsed_price = float(price)
            except (TypeError, ValueError):
                return jsonify({"status": "error", "message": "price 必须是数字"}), 400
                
        store.upsert_item(name, price=parsed_price, image=image)
        return jsonify({"status": "ok", "message": "设置成功", "menu": store.get_menu()})

    @app.route("/admin/menu/<name>", methods=["DELETE"])
    def admin_delete_item(name):
        ok = store.delete_item(name)
        if not ok:
            return jsonify({"status": "error", "message": "菜单中不存在该菜品"}), 404
        return jsonify({"status": "ok", "message": "删除成功", "menu": store.get_menu()})

    # 修改后的图片生成接口
    @app.route("/admin/menu/<name>/gen-image", methods=["POST"])
    def admin_generate_image(name):
        """本地生成图片接口"""
        try:
            # 即使前端不传 prompt，我们也不需要了，直接用 name 生成
            image_path = generate_local_dish_image(name)
        except Exception as exc:
            logging.exception("生成图片失败：%s", exc)
            return jsonify({"status": "error", "message": "生成图片失败"}), 500

        store.upsert_item(name, image=image_path)
        return jsonify({
            "status": "ok",
            "message": "图片已生成",
            "image": image_path,
            "menu": store.get_menu(),
        })

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"status": "error", "message": "接口不存在"}), 404

    @app.errorhandler(500)
    def server_error(_):
        return jsonify({"status": "error", "message": "服务器内部错误"}), 500

    @app.after_request
    def add_headers(response):
        response.headers["X-App-Version"] = "2.0-local"
        return response

    return app

def configure_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app = create_app()

if __name__ == "__main__":
    configure_logging()
    logging.info("Server running at http://%s:%s", HOST, PORT)
    app.run(host=HOST, port=PORT, debug=False)