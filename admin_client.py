import requests


BASE_URL = "http://127.0.0.1:5000"


def get_menu():
    try:
        resp = requests.get(f"{BASE_URL}/menu", timeout=5)
        return resp.json()
    except Exception as e:
        return {"status": "error", "message": f"请求菜单失败: {e}"}


def set_item():
    name = input("请输入菜名（新增或修改）：").strip()
    if not name:
        print("菜名不能为空")
        return
    price_str = input("请输入价格（留空代表不修改）：").strip()
    price = None
    if price_str:
        try:
            price = float(price_str)
        except ValueError:
            print("价格必须是数字")
            return
    image_url = input("如果已有图片 URL，可直接粘贴（留空跳过）：").strip() or None
    try:
        resp = requests.post(
            f"{BASE_URL}/admin/menu",
            json={"name": name, "price": price, "image": image_url},
            timeout=10,
        )
        data = resp.json()
    except Exception as e:
        print(f"请求失败: {e}")
        return

    if data.get("status") == "ok":
        print("设置成功。")
    else:
        print("设置失败：", data.get("message"))


def delete_item():
    name = input("请输入要删除的菜名：").strip()
    if not name:
        print("菜名不能为空")
        return
    try:
        resp = requests.delete(
            f"{BASE_URL}/admin/menu/{name}",
            timeout=5,
        )
        data = resp.json()
    except Exception as e:
        print(f"请求失败: {e}")
        return

    if data.get("status") == "ok":
        print("删除成功。")
    else:
        print("删除失败：", data.get("message"))


def show_menu():
    data = get_menu()
    if data.get("status") != "ok":
        print("获取菜单失败：", data.get("message"))
        return
    menu = data.get("menu", {})
    print("\n=== 当前菜单 ===")
    if not menu:
        print("暂无菜品")
        return
    for i, (name, info) in enumerate(menu.items(), start=1):
        if isinstance(info, dict):
            price = float(info.get("price", 0))
            has_image = "是" if info.get("image") else "否"
        else:
            price = float(info)
            has_image = "否"
        print(f"{i}. {name} - ￥{price:.2f} | 图片：{has_image}")


def generate_ai_image():
    name = input("请输入需要生成图片的菜名：").strip()
    if not name:
        print("菜名不能为空")
        return
    prompt = input("可选：自定义提示词（留空使用默认风格）：").strip()
    payload = {"prompt": prompt} if prompt else {}
    try:
        resp = requests.post(
            f"{BASE_URL}/admin/menu/{name}/ai-image",
            json=payload,
            timeout=60,
        )
        data = resp.json()
    except Exception as e:
        print(f"请求失败: {e}")
        return

    if data.get("status") == "ok":
        print("图片已生成：", data.get("image"))
    else:
        print("生成失败：", data.get("message"))


def main():
    print("=== 后台管理客户端 ===")
    print(f"服务地址：{BASE_URL}")
    while True:
        print("\n1. 查看菜单")
        print("2. 新增/修改菜品")
        print("3. 删除菜品")
        print("4. 使用 AI 生成菜品图片")
        print("q. 退出")
        choice = input("请选择操作：").strip().lower()
        if choice == "1":
            show_menu()
        elif choice == "2":
            set_item()
        elif choice == "3":
            delete_item()
        elif choice == "4":
            generate_ai_image()
        elif choice == "q":
            print("已退出后台管理客户端。")
            break
        else:
            print("无效选择，请重新输入。")


if __name__ == "__main__":
    main()


