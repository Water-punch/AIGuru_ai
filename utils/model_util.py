import re, random

LABEL_POSITIVE = "LABEL_1"
LABEL_NEGATIVE = "LABEL_0"

def parse_response_by_label(result):
    # 그린라이트: 1 / 레드라이트: 0
    if result[0]["label"] == LABEL_POSITIVE:
        response_message = 'positive'
    else:
        response_message = 'negative'
    #return jsonify({"position": response_message})
    return {"position": response_message}

# 답변에서 '[상담]:' 다음 부분만 파싱
def parsing_gpt_answer(response_message):
  counseling_section = re.search(r'\[상담\]:([\s\S]*)', response_message)
  if counseling_section:
    counselingText = counseling_section.group(1).strip()
    print('counselingText:', counselingText)
  else: 
    counselingText = '뭐라는거야. 알아 듣게 좀 말해보게나.'
  return counselingText