from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from openai import OpenAI
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/conversation', methods=['POST'])
def firstConversation():
    # db ---> flask: [text, feeling, QnA_result] 
    question = request.json['question']

    # question = '1년째 연애중인 20대 남성이야. 요즘따라 여자친구가 연락이 잘 안되고 자꾸 나를 피하는 느낌이 들어. 헤어지자는 뜻일까?'
    # question = '똥'
    feeling = 'sad' 
    QnA_result = { '분류' : '이별', } 
    
    prompt = f'''
    참고사항: `
    -질문의 종류: {QnA_result['분류']}에 관한 고민\n
    -작성자의 감정: {feeling}\n
    -질문이 연애상담과 전혀 관련이 없을 경우 "장난칠거면 가라."라고 대답할 것.
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

    # message 객체의 content 속성을 사용
    return jsonify({"response": response_message})


# flask run or python app.py
if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)
