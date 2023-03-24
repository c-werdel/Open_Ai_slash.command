import urllib3
import openai
import os
import json
import base64

http = urllib3.PoolManager()
openai.api_key = os.environ["API_KEY"]
  
def chat():
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "when did the US land on the moon?"}
      ]
  )
  return(response["choices"][0]["message"]["content"])

def lambda_handler(event, context):
  print("Event: ")
  print(event)
  decoded_string = base64.b64decode(event["body"])
  print("Event body decoded: ")
  print(decoded_string)
  
  content = chat()

  SLACK_TOKEN = os.environ["SLACK_BOT_TOKEN"]
  payload = {
  	"blocks": [
  		{
  			"type": "section",
  			"text": {
  				"type": "mrkdwn",
  				"text": f"{content}" 
  			}
  		}
  	]
  }
  print(payload)
  encoded_data = json.dumps(payload).encode('utf-8')
  response =  http.request(
              'POST',
              SLACK_TOKEN,
              body=encoded_data,
              headers={'Content-Type': 'application/json'})
  
  print('This is gpt test')
  print(response.status)
  print(response.data)
