import requests
import json
import os
import glob

# API lấy token
API_TOKEN = "https://prod-sn.emso.vn/oauth/token"

# Client ID & Client Secret (cần giữ bí mật)
CLIENT_ID = "Ev2mh1kSfbrea3IodHtNd7aA4QlkMbDIOPr4Y5eEjNg"
CLIENT_SECRET = "f2PrtRsNb7scscIn_3R_cz6k_fzPUv1uj7ZollSWBBY"

def find_token_files():
    """Tìm tất cả file 'tokens.json' trong thư mục hiện tại và thư mục con."""
    return glob.glob("**/tokens.json", recursive=True)

def load_tokens(file_path):
    """Tải danh sách token từ file JSON."""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_tokens(file_path, tokens):
    """Lưu danh sách token vào file JSON."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(tokens, file, indent=4, ensure_ascii=False)

def get_token(username, password):
    """Gửi request lấy token từ API."""
    payload = {
        "username": username,
        "password": password,
        "grant_type": "password",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "write read follow"
    }
    
    headers = {"Content-Type": "application/json"}
    response = requests.post(API_TOKEN, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"❌ Lỗi đăng nhập! Mã lỗi: {response.status_code}")
        print(response.text)
        return None

def main():
    """Chương trình chính"""
    token_files = find_token_files()
    
    if not token_files:
        print("⚠️ Không tìm thấy file 'tokens.json' nào trong project!")
        return
    
    print(f"\n🔍 Tìm thấy {len(token_files)} file 'tokens.json':")
    for idx, file in enumerate(token_files, 1):
        print(f"  [{idx}] {file}")

    while True:
        print("\n🔹 Nhập tài khoản để lấy token (Nhấn Enter để thoát)")
        username = input("📧 Email: ").strip()
        if not username:
            break
        
        password = input("🔑 Mật khẩu: ").strip()
        if not password:
            break
        
        token = get_token(username, password)
        if token:
            print(f"✅ Token nhận được: {token} (đang lưu vào tất cả file)")
            
            # Cập nhật tất cả file tokens.json
            for file in token_files:
                tokens = load_tokens(file)
                tokens.append(token)
                save_tokens(file, tokens)
                print(f"📂 Đã lưu vào {file}")
        else:
            print("⚠️ Không thể lấy token!")

    print("\n✅ Hoàn thành cập nhật tất cả file tokens.json!")
    input("\nNhấn Enter để thoát...")

if __name__ == "__main__":
    main()
