from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from services.gpt_service import conversation
import re, random
from utils.gpt_util import generate_random_id, parsing_gpt_answer
from utils.model_util import parse_response_by_label
import tensorflow as tf
from flask import g
from transformers import TFBertModel, pipeline , BertTokenizer, TFBertForSequenceClassification

app = Flask(__name__)
CORS(app)

# classifier를 전역 변수로 선언
classifier = False

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/test', methods=['GET'])
def test_api():
  requestData = request;
  print(requestData)

  return jsonify({"position": "요청 성공"})

# 모델을 이용하여 감정 분류
@app.route('/analysis', methods=['POST'])
def textAnalysis():
  global classifier, tokenizer
  print('classifier 확인: ', classifier)

  # 전역 변수에 저장된 classifier가 없으면 새로 정의함
  if not classifier:
      model_name = "guru.h5"
      tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
      classifier = pipeline("sentiment-analysis", model=model_name, tokenizer=tokenizer)

  requestData = request.json
  content = requestData['content']

  # model_name = "guru.h5"
  # tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
  # classifier = pipeline("sentiment-analysis", model=model_name, tokenizer=tokenizer)

  analysis_result = classifier(content)
  print("result 확인: ", analysis_result)
  
  response_json = parse_response_by_label(analysis_result)
  # response_json 예시
  #   {
  #     "position": "negative"
  #   }
  return jsonify(response_json)


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

  # {chatId, title} history [0]에 저장
  chatInfo = [chatId, title]
  history.append(chatInfo)

  # 답변에서 '[상담]:' 다음 부분만 파싱
  counselingText = parsing_gpt_answer(response_message)

  # history에 첫 문답 저장
  chat_history = [requestData['question'], counselingText]
  history.append(chat_history)
  print('history:', history)

  # message 객체의 content 속성을 사용
  return jsonify({"response": history})


# 추가채팅 API
@app.route('/chat:chatId', methods=['POST'])
def additionalConversation():

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

def load_model():
  load_model = tf.keras.models.load_model('./lib/guru.h5')
  
  return load_model

# flask run or python app.py
if __name__ == '__main__':  
  app.run(host='0.0.0.0', port=5000, debug=True)
