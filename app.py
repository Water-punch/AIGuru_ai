from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from services.gpt_service import conversation
import re, random
from utils.gpt_util import generate_random_id, parsing_gpt_answer
from utils.model_util import parse_response_by_label, validate_by_base64
import tensorflow as tf
from flask import g
from transformers import TFBertModel, pipeline , BertTokenizer, TFBertForSequenceClassification
import base64

app = Flask(__name__)
CORS(app)


def load_model():
  global classifier
  model_name = "guru_model.h5"
  print(f"모델을 불러오고 있습니다..")

  tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
  classifier = pipeline("text-classification", model=model_name, tokenizer=tokenizer)
  
  return classifier

# classifier를 전역 변수로 선언
classifier = load_model()  

@app.route('/')
def index():
  return render_template('index.html')

# 첫 채팅 API
@app.route('/chat/first', methods=['POST'])
def firstConversation():

  history = []
  requestData = request.json
 
  # GPT에게 질문 전달, 응답 저장
  response_message = conversation(requestData)

  # title 저장
  title = response_message.split('\n')[0]

  # 임시로 생성한 10자리 난수 id
  chatId = generate_random_id()

  # [chatId, title] history [0]에 저장
  chatInfo = [chatId, title]
  history.append(chatInfo)

  # 답변에서 '[상담]:' 다음 부분만 파싱
  counselingText = parsing_gpt_answer(response_message)

  # history에 첫 문답 저장
  chat_history = [requestData['question'], counselingText]
  history.append([])
  history[1].append(chat_history)
  print('history:', history)

  # message 객체의 content 속성을 사용
  return jsonify({"response": history})


# 추가채팅 API
@app.route('/chat/<chatId>', methods=['POST'])
def additionalConversation(chatId):

  history = request.json['history']
  requestData = request.json
 
  # GPT에게 질문 전달, 응답 저장
  response_message = conversation(requestData)

  # 답변에서 '[상담]:' 다음 부분만 파싱
  counselingText = parsing_gpt_answer(response_message)

  # history에 새 문답 저장
  chat_history = [requestData['question'], counselingText]
  history[1].append(chat_history)
  print('history:', history)

  # message 객체의 content 속성을 사용
  return jsonify({"response": history})

# 모델을 이용하여 긍부정 분류
@app.route('/analysis', methods=['POST'])
def textAnalysis():
  global classifier

  # 헤더에서 인증 정보를 받아옴
  if request.headers.get('Authorization'):
    auth = request.headers.get('Authorization')
  
    username = auth.split(' ')[1].split(':')[0]
    password = auth.split(' ')[1].split(':')[1]

    if not validate_by_base64(username, password):
      print("불일치!!")
      return 'Unauthroization!', 401
    else:
      print("인증 성공")
  else:
    print("warn:: 인증 헤더가 포함되지 않았습니다!")

  # 전역 변수에 저장된 classifier가 없으면 새로 정의함
  if not classifier:
      print(f"model을 다시 불러옵니다..")
      load_model()

  content = request.json['content']
  analysis_result = classifier(content)
  print("분석결과: ", analysis_result)
  
  response_json = parse_response_by_label(analysis_result)
  return jsonify(response_json)


# flask run or python app.py
if __name__ == '__main__':  
  app.run(host='0.0.0.0', port=5000, debug=True)