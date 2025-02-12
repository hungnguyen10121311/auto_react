import requests
import json
import time
import os
import random

def load_tokens():
    script_dir = os.getcwd()  # Lấy thư mục hiện tại nơi chạy file .py
    file_path = os.path.join(script_dir, "tokens.json")  # Ghép đường dẫn với tên file
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Không tìm thấy file: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def send_comment(token, comment, reply_id):
    """Gửi bình luận bằng token tương ứng."""
    url = "https://prod-sn.emso.vn/api/v1/statuses"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': f'Bearer {token}',
        'content-type': 'application/json',
    }
    payload = json.dumps({
        "status": comment,
        "in_reply_to_id": reply_id,
        "sensitive": False,
        "media_ids": [],
        "spoiler_text": "",
        "visibility": "public",
        "poll": None,
        "extra_body": None,
        "tags": [],
        "page_owner_id": None,
    })
    
    response = requests.post(url, headers=headers, data=payload)
    return response.status_code

def main():
    tokens = load_tokens()
    random.shuffle(tokens)  # Đảo thứ tự token ngẫu nhiên

    # Nhập ID bài viết cần trả lời
    reply_id = input("Nhập ID bài viết cần trả lời: ")

    # Nhập danh sách bình luận từ nhiều dòng
    print("\nNhập danh sách bình luận (mỗi dòng là 1 comment, nhập xong nhấn Enter 2 lần để kết thúc):")
    comments = []
    while True:
        comment = input()
        if comment == "":
            break  # Nhấn Enter 2 lần để dừng nhập
        comments.append(comment)

    # Gửi bình luận tự động chỉ khi còn token và comment
    print("\n🚀 Bắt đầu gửi bình luận...\n")
    for idx, (token, comment) in enumerate(zip(tokens, comments)):
        status = send_comment(token, comment, reply_id)
        print(f"[{idx + 1}/{min(len(tokens), len(comments))}] Token: {token[:10]}... | Bình luận: {comment} | Status: {status}")
        sleep_time = random.randint(120, 180)  # Chờ ngẫu nhiên từ 2 đến 3 phút
        print(f"⏳ Chờ {sleep_time} giây trước khi gửi bình luận tiếp theo...")
        time.sleep(sleep_time)

    print("\n✅ Hoàn thành gửi bình luận!")

    # Chờ người dùng nhấn phím trước khi đóng cửa sổ
    input("\nNhấn Enter để thoát...")

if __name__ == "__main__":
    main()
