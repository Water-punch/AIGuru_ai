LABEL_POSITIVE = "LABEL_1"
LABEL_NEGATIVE = "LABEL_0"

def parse_response_by_label(result):
    # 그린라이트: 1 / 레드라이트: 0
    if result[0]["label"] == LABEL_POSITIVE:
        response_message = 'positive'
    else:
        response_message = 'negative'
    return {"position": response_message}
