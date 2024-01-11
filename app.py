from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from openai import OpenAI
from flask_cors import CORS
import random

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI()

# 10자리 난수 id 생성함수(임시)
def generate_random_id():
  return ''.join([str(random.randint(0, 9)) for _ in range(10)])

@app.route('/')
def index():
  return render_template('index.html')

'''
* 임시 데이터
question = '1년째 연애중인 20대 남성이야. 요즘따라 여자친구가 연락이 잘 안되고 자꾸 나를 피하는 느낌이 들어. 헤어지자는 뜻일까?'
question = '똥'
QnA_result = { '분류' : '이별', } 
'''

# 첫 채팅 API
@app.route('/chat/first', methods=['POST'])
def firstConversation():
  # db ---> flask: {text, QnA_result}

  history = []

  # 임시로 생성한 10자리 난수 id
  chatId = generate_random_id()

  question = request.json['question']
  # QnA_result = { '분류' : '이별', } 
  #현재 원인 모를 에러 발생
 
  prompt = f'''
  참고사항: `
  -질문의 종류: 이별에 관한 고민
  -연애에 대한 내용이 아닐 경우 해결책을 제시하지 말 것.
  -질문이 연애상담과 관련이 없을 경우 "장난칠거면 가라."라고 짧게 대답할 것.
  -답변을 시작하기 전에 []에 질문을 요약하고 줄바꿈을 한 뒤 답변을 시작할 것.
  `

  ```{question}```

  참고사항을 참고해서 ```로 감싸진 질문에 대해 답변해줘.
  답변에 [답변]을 붙이지마.
  연애와 관련없는 질문에는 짧게 대답해.

  '''

  # OpenAI 프롬프트 생성 및 실행
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {
          'role': 'system',
          'content': '너는 연애의 달인으로, 너의 역할은 사람들의 고민에 공감하고 명확한 해결책을 제시하는거야. 공자, 맹자의 말투, 반말을 사용해서 대답해야해. 너의 역할에 대해서는 언급하지마.'
      },
      {
          'role': 'user',
          'content': prompt
      },
    ],
    temperature=0.7
  )

  # 응답 반환
  response_message = response.choices[0].message.content  
  print(response.choices[0].message)

  # title 저장
  title = response_message.split('\n')[0]

  # {chatId, title} history [0]에 저장
  chatInfo = [chatId, title]
  history.append(chatInfo)

  # history에 input과 output 저장
  history.append([question, response_message])
  print(history)

  # message 객체의 content 속성을 사용
  return jsonify({"response": history})


# 추가채팅 API
@app.route('/chat:chatId', methods=['POST'])
def additionalConversation():
  # db ---> flask: { chatHistory, newChat, lastChat }

  history = []
  history = request.json['chatHistory']
  lastChat = request.json['lastChat']
  question = request.json['newChat']['question']
  # QnA_result = request.json.get('QnA_result', {'분류': '연애'})
  QnA_result = { '분류' : '이별', }
  
  
  prompt = f'''
  참고사항: `
  -이전 대화: ${lastChat}\n
  -이전 대화를 참고해서 답변을 작성할 것.
  -질문이 연애상담과 전혀 관련이 없을 경우 "장난칠거면 가라."라고 대답할 것.
  -답변을 시작하기 전에 []에 질문을 요약하고 줄바꿈을 한 뒤 답변을 시작할 것.
  `

  ```{question}```

  참고사항을 참고해서 ```로 감싸진 질문에 대해 답변해줘.

  '''

  # OpenAI 프롬프트 생성 및 실행
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {
          'role': 'system',
          'content': '너는 연애의 달인으로, 너의 역할은 사람들의 고민에 공감하고 명확한 해결책을 제시하는거야. 공자, 맹자의 말투, 반말을 사용해서 대답해야해. 너의 역할에 대해서는 언급하지마.'
      },
      {
          'role': 'user',
          'content': prompt
      },
    ],
    temperature=0.7
  )

  # 응답 반환
  response_message = response.choices[0].message.content  
  print(response.choices[0].message)

  # history에 input과 output 저장
  history.append([question, response_message])

  # message 객체의 content 속성을 사용
  return jsonify({"response": history})

# flask run or python app.py
if __name__ == '__main__':  
  app.run('0.0.0.0',port=5000,debug=True)
