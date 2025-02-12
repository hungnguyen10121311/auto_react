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

def send_friend_request(token, user_id):
    """Gửi yêu cầu kết bạn."""
    url = f"https://prod-sn.emso.vn/api/v1/accounts/{user_id}/friendship_requests"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': f'Bearer {token}',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }
    response = requests.post(url, headers=headers)
    return response.status_code, response.text

def main():
    try:
        tokens = load_tokens()
    except FileNotFoundError as e:
        print(e)
        return
    
    if not tokens:
        print("❌ Danh sách token trống! Vui lòng kiểm tra lại file tokens.json.")
        return
    
    user_id = input("Nhập ID tài khoản cần gửi lời mời kết bạn: ")
    print("\n🚀 Bắt đầu gửi lời mời kết bạn...\n")
    
    for idx, token in enumerate(tokens):
        status_code, response_text = send_friend_request(token, user_id)
        if status_code in [200, 201]:
            print(f"[{idx + 1}/{len(tokens)}] ✅ Gửi thành công với token: {token[:10]}... | Status: {status_code}")
        else:
            print(f"[{idx + 1}/{len(tokens)}] ❌ Lỗi với token: {token[:10]}... | Status: {status_code} | Response: {response_text}")
        time.sleep(1)  # Nghỉ 1 giây giữa các request
    
    print("\n✅ Hoàn thành gửi lời mời kết bạn!")
    input("\nNhấn Enter để thoát...")

if __name__ == "__main__":
    main()
