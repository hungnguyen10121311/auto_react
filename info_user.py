import requests
import json
import time

def check_response(response, success_status_code=200):
    """ Kiểm tra xem response có thành công không """
    return response.status_code == success_status_code

def get_user_info(username, password):
    login_payload = {
        'username': username,
        'password': password,
        'grant_type': 'password',
        'client_id': 'Ev2mh1kSfbrea3IodHtNd7aA4QlkMbDIOPr4Y5eEjNg',
        'client_secret': 'f2PrtRsNb7scscIn_3R_cz6k_fzPUv1uj7ZollSWBBY',
        'scope': 'write read follow'
    }

    login_response = requests.post(
        'https://prod-sn.emso.vn/oauth/token',
        json=login_payload,
        headers={'Content-Type': 'application/json'}
    )

    if check_response(login_response):
        login_data = login_response.json()
        token = login_data.get('access_token')

        user_response = requests.get(
            'https://prod-sn.emso.vn/api/v1/me',
            headers={'Authorization': f'Bearer {token}'}
        )

        if check_response(user_response):
            user_data = user_response.json()
            user_info = {
                "display_name": user_data['display_name'],
                "email": username,
                "user_id": user_data['id'],
                "token": token
            }
            
            with open("user_info.json", "a", encoding="utf-8") as file:
                json.dump(user_info, file, ensure_ascii=False, indent=4)
                file.write("\n")

            print("----------------------------------")
            print(f"👤 Display Name: {user_data['display_name']}")
            print(f"📧 Email: {username}")
            print(f"📝 Username: {user_data['username']}")
            print(f"🆔 User ID: {user_data['id']}")
            print(f"🔑 Token: {token}")
            print("----------------------------------")
        else:
            print("❌ Lỗi khi lấy thông tin user")
    else:
        print("❌ Đăng nhập thất bại, vui lòng kiểm tra tài khoản/mật khẩu")

def main():
    enter_count = 0
    while True:
        username = input("Nhập tài khoản: ")
        password = input("Nhập mật khẩu: ")
        get_user_info(username, password)
        key = input("Nhấn Enter để tiếp tục hoặc Enter 2 lần để thoát... ")
        if key == "":
            enter_count += 1
            if enter_count >= 2:
                print("🚪 Thoát chương trình...")
                break
        else:
            enter_count = 0
        print("\n")

if __name__ == '__main__':
    main()
