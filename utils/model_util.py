import base64

LABEL_POSITIVE = "LABEL_1"
LABEL_NEGATIVE = "LABEL_0"

def validate_by_base64(username, password):
    decoded_name_bytes = base64.b64decode(username)
    decoded_name = decoded_name_bytes .decode('ascii')
    
    decoded_pwd_bytes = base64.b64decode(password)
    decoded_pwd = decoded_pwd_bytes .decode('ascii')

    if decoded_name == 'guru_back_server' and decoded_pwd == 'back!Password123!':
        return True
    return False

def parse_response_by_label(result):
    # 그린라이트: 1 / 레드라이트: 0
    if result[0]["label"] == LABEL_POSITIVE:
        response_message = 'positive'
    else:
        response_message = 'negative'
    return {"position": response_message}