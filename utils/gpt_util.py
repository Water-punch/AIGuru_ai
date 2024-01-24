import re, random

# 10자리 난수 id 생성함수(임시)
def generate_random_id():
  return ''.join([str(random.randint(0, 9)) for _ in range(10)])

# 답변에서 '[상담]:' 다음 부분만 파싱
def parsing_gpt_answer(response_message):
  counseling_section = re.search(r'\[상담\]:([\s\S]*)', response_message)
  if counseling_section:
    counselingText = counseling_section.group(1).strip()
    print('counselingText:', counselingText)
  else: 
    counselingText = '뭐라는거야. 알아 듣게 좀 말해보게나.'
  return counselingText