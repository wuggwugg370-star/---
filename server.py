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
from doubao_client import DoubaoError, generate_dish_image
from menu_store import MenuStore


def create_app() -> Flask:
    app = Flask(__name__, static_folder=str(WEB_DIR), static_url_path="")

    # CORS：允许前端部署在其他域名下
    if ALLOWED_ORIGINS == ["*"]:
        CORS(app)
    else:
        CORS(app, resources={r"/*": {"origins": ALLOWED_ORIGINS}})

    store = MenuStore(MENU_DATA_FILE, DEFAULT_MENU)

    @app.route("/", methods=["GET"])
    def index_page():
        """前端网页客户端：返回 web/index.html"""
        return app.send_static_file("index.html")

    @app.route("/healthz", methods=["GET"])
    def healthz():
        return jsonify({"status": "ok"})

    @app.route("/menu", methods=["GET"])
    def get_menu():
        """获取当前菜单。"""
        return jsonify({"status": "ok", "menu": store.get_menu()})

    @app.route("/order", methods=["POST"])
    def order():
        """点餐接口"""
        data = request.get_json(silent=True) or {}
        items = data.get("items")
        if not isinstance(items, list) or not items:
            return (
                jsonify({"status": "error", "message": "点餐列表不能为空"}),
                400,
            )

        total, not_found, detail = store.calc_order(items)
        if not_found:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"以下菜品不存在：{', '.join(not_found)}",
                    }
                ),
                400,
            )

        return jsonify(
            {
                "status": "ok",
                "message": "点餐成功",
                "total": total,
                "detail": detail,
            }
        )

    @app.route("/admin/menu", methods=["POST", "PUT"])
    def admin_set_item():
        """新增或更新菜品：JSON {name, price?, image?}"""
        data = request.get_json(silent=True) or {}
        name = data.get("name")
        price = data.get("price")
        image = data.get("image")
        if not name or (price is None and image is None):
            return (
                jsonify(
                    {"status": "error", "message": "需要提供 name，并指定 price 或 image"}
                ),
                400,
            )
        parsed_price = None
        if price is not None:
            try:
                parsed_price = float(price)
            except (TypeError, ValueError):
                return (
                    jsonify({"status": "error", "message": "price 必须是数字"}),
                    400,
                )
        store.upsert_item(name, price=parsed_price, image=image)
        return jsonify(
            {"status": "ok", "message": "设置成功", "menu": store.get_menu()}
        )

    @app.route("/admin/menu/<name>", methods=["DELETE"])
    def admin_delete_item(name):
        """删除菜品。"""
        ok = store.delete_item(name)
        if not ok:
            return (
                jsonify({"status": "error", "message": "菜单中不存在该菜品"}),
                404,
            )
        return jsonify(
            {"status": "ok", "message": "删除成功", "menu": store.get_menu()}
        )

    @app.route("/admin/menu/<name>/ai-image", methods=["POST"])
    def admin_generate_image(name):
        """调用豆包接口生成菜品图片"""
        data = request.get_json(silent=True) or {}
        prompt = data.get("prompt")
        try:
            image_path = generate_dish_image(name, prompt)
        except DoubaoError as exc:
            return jsonify({"status": "error", "message": str(exc)}), 400
        except Exception as exc:  # noqa: BLE001
            logging.exception("生成菜品图片失败：%s", exc)
            return jsonify({"status": "error", "message": "生成图片失败"}), 500

        store.upsert_item(name, image=image_path)
        return jsonify(
            {
                "status": "ok",
                "message": "菜品图片已生成",
                "image": image_path,
                "menu": store.get_menu(),
            }
        )

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"status": "error", "message": "接口不存在"}), 404

    @app.errorhandler(500)
    def server_error(_):
        return jsonify({"status": "error", "message": "服务器内部错误"}), 500

    @app.after_request
    def add_headers(response):
        response.headers["X-App-Version"] = "1.0"
        return response

    return app


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


app = create_app()


if __name__ == "__main__":
    configure_logging()
    logging.info(
        "HTTP 点餐服务已启动，GET /menu, POST /order, /admin/menu ... (%s:%s)",
        HOST,
        PORT,
    )
    app.run(host=HOST, port=PORT, debug=False)
