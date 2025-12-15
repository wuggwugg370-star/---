import requests


BASE_URL = "http://127.0.0.1:5000"


def get_menu():
    try:
        resp = requests.get(f"{BASE_URL}/menu", timeout=5)
        return resp.json()
    except Exception as e:
        return {"status": "error", "message": f"请求菜单失败: {e}"}


def send_order(items):
    try:
        resp = requests.post(
            f"{BASE_URL}/order",
            json={"items": items},
            timeout=5,
        )
        return resp.json()
    except Exception as e:
        return {"status": "error", "message": f"请求下单失败: {e}"}


def _price_of(entry) -> float:
    if isinstance(entry, dict):
        return float(entry.get("price", 0.0))
    return float(entry)


def show_menu(menu: dict):
    print("\n=== 菜单 ===")
    if not menu:
        print("暂无菜品")
        return
    for idx, (name, info) in enumerate(menu.items(), start=1):
        price = _price_of(info)
        print(f"{idx}. {name} - ￥{price:.2f}")


def main():
    while True:
        # 先从服务器获取最新菜单（HTTP）
        resp = get_menu()
        if resp.get("status") != "ok":
            print("获取菜单失败：", resp.get("message"))
            break
        menu = resp.get("menu", {})
        show_menu(menu)

        print("\n输入要点的菜品名称，多个菜品用逗号分隔；输入 q 退出。")
        user_input = input("请点餐：").strip()
        if user_input.lower() == "q":
            print("已退出点餐客户端。")
            break
        if not user_input:
            continue

        items = [x.strip() for x in user_input.split(",") if x.strip()]
        if not items:
            continue

        resp = send_order(items)
        if resp.get("status") == "ok":
            print("\n=== 点餐结果 ===")
            print(resp.get("message", "点餐成功"))
            print("详情：")
            for item in resp.get("detail", []):
                print(f"- {item['name']}: ￥{item['price']:.2f}")
            print(f"合计：￥{resp.get('total', 0.0):.2f}\n")
        else:
            print("点餐失败：", resp.get("message"), "\n")


if __name__ == "__main__":
    main()


