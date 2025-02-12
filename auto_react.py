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


def send_react(post_id, token):
    url = f'https://prod-sn.emso.vn/api/v1/statuses/{post_id}/favourite'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': f'Bearer {token}',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
    }
    payload = json.dumps({"custom_vote_type": "like", "page_id": None})
    
    response = requests.post(url, headers=headers, data=payload)
    return response.status_code


def main():
    tokens = load_tokens()
    
    if not tokens:
        print("Không có token nào được tải.")
        return

    post_ids = []
    print("Nhập ID bài post (Nhấn Enter hai lần để bắt đầu):")
    while True:
        post_id = input("📌 Nhập ID: ").strip()
        if post_id == "":
            if len(post_ids) > 0:
                break  # Thoát khi nhấn Enter lần thứ hai
            else:
                print("⚠️ Cần nhập ít nhất một ID bài post!")
                continue
        post_ids.append(post_id)
    
    print("\n🚀 Bắt đầu gửi react...")
    for post_id in post_ids:
        print(f"\n📌 Đang react cho bài post ID: {post_id}")
        for idx, token in enumerate(tokens):
            status = send_react(post_id, token)
            print(f"  [{idx + 1}/{len(tokens)}] Token: {token}... | Status: {status}")    
    print("\n✅ Hoàn thành tất cả react!")


if __name__ == "__main__":
    main()
