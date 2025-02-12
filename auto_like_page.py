import requests
import json
import time
import os


def load_tokens():
    script_dir = os.getcwd()  # Lấy thư mục hiện tại nơi chạy file .py
    file_path = os.path.join(script_dir, "tokens.json")  # Ghép đường dẫn với tên file
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Không tìm thấy file: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def like_page(page_id, token):
    url = f'https://prod-sn.emso.vn/api/v1/pages/{page_id}/likes'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': f'Bearer {token}',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
    }
    response = requests.post(url, headers=headers)
    return response.status_code


def main():
    tokens = load_tokens()
    
    if not tokens:
        print("Không có token nào được tải.")
        return

    page_ids = []
    print("Nhập ID trang cần like (Nhấn Enter hai lần để bắt đầu):")
    while True:
        page_id = input("📌 Nhập ID: ").strip()
        if page_id == "":
            if len(page_ids) > 0:
                break  # Thoát khi nhấn Enter lần thứ hai
            else:
                print("⚠️ Cần nhập ít nhất một ID trang!")
                continue
        page_ids.append(page_id)
    
    print("\n🚀 Bắt đầu like các trang...")
    for page_id in page_ids:
        print(f"\n📌 Đang like trang ID: {page_id}")
        for idx, token in enumerate(tokens):
            status = like_page(page_id, token)
            print(f"  [{idx + 1}/{len(tokens)}] Token: {token} | Status: {status}")    
    print("\n✅ Hoàn thành tất cả lượt like!")


if __name__ == "__main__":
    main()
