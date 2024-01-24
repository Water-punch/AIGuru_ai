from dotenv import load_dotenv
from openai import OpenAI
import copy

load_dotenv()
client = OpenAI()

def conversation(requestData):
  question = requestData.get('question')
  history = requestData.get('history', None)
  testResult = requestData.get('testResult', None)
  imageUrl = requestData.get('imageUrl', None)

  # 추가 채팅을 위한 history
  if history:
    lastChatArray = copy.deepcopy(history[1])
    lastChat = ''
    for chat in lastChatArray:
      chat[0] = "[user's question]:" + chat[0] +'\n'
      chat[1] = "[your answer]:" + chat[1] + '\n'
      lastChat = lastChat + chat[0] + chat[1]
  else: 
    lastChat = '없음'

  # 사전질문 처리
  if testResult:
    questionType = testResult['questionType']
  else: 
    questionType = '설정되지 않음'
  
  # 첨부파일 image -> text 변환 과정
  if imageUrl:
    # additional_info = image_to_text(imageUrl)
    additional_info = '없음'
  else:
    additional_info = '없음'

  prompt = f'''
    참고사항: 
    `
    -질문의 카테고리: {questionType}
    -이전 대화: {lastChat}
    -질문이 연애와 관련이 없을 경우 "장난칠거면 가라."라고 짧게 대답할 것.
    `

    ''{question}''

    질문에 대한 추가 정보:
    `{additional_info}`

    참고사항과 추가정보를 참고해서 ''로 감싸진 질문에 대해 답변해줘.
    아래 답변 포맷을 지켜서 그대로 답변해.
    
    <답변 포맷>
    [주제]: '질문을 한 문장 이내로 요약' \n [상담]: \n  '질문에 대한 답변.'
    '''

  # OpenAI 프롬프트 생성 및 실행
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {
          'role': 'system',
          'content': '너는 연애의 달인으로, 너의 역할은 사람들의 고민에 공감하고 해결책을 제시하는거야. 공자, 맹자의 말투, 반말을 사용해서 대답해야해. 너의 역할에 대해서는 언급하지마.'
      },
      {
          'role': 'user',
          'content': prompt
      },
    ],
    temperature=0.7
  )

  # 응답 반환
  response_message = response.choices[0].message.content or '... 서버 오류가 발생했습니다.'
  print(response.choices[0].message)

  return response_message