#!/usr/bin/python3
from numpy import source
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import time
from dotenv import load_dotenv
import os

load_dotenv()
SLACK_BOT_TOKEN=os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN=os.environ.get("SLACK_APP_TOKEN")

app = App(token=SLACK_BOT_TOKEN)

@app.message("おえかき")
def draw_new(message, say):
    #print(message)
    mode="stable"
    user = message['user']
    tmp = message['text'].split()
    tmp.pop(0)
    text = " ".join(tmp)
    if message['channel']=="C045RAYE3DH":
        with open('./queue/'+str(time.time()), 'w') as f:
            f.write(user+"\n"+text+"\n"+mode+"\n"+"public")
        say(f"<@{user}>"+" キューに追加しました:"+text)

@app.message("イラスト")
def draw_new(message, say):
    #print(message)
    mode="waifu"
    user = message['user']
    tmp = message['text'].split()
    tmp.pop(0)
    text = " ".join(tmp)
    if message['channel']=="C045RAYE3DH":
        if 'root' in message:
            if message["root"]["files"][0]["filetype"]=="png":
                image_url = "\n"+message["root"]["files"][0]["url_private"]
        else:
            image_url=""
        with open('./queue/'+str(time.time()), 'w') as f:
            f.write(user+"\n"+text+"\n"+mode+"\n"+"public"+image_url)
        say(f"<@{user}>"+" キューに追加しました:"+image_url+" "+text)

@app.command("/waifu")
def todo(ack, respond, command):
    ack()
    userInput = command['text']
    mode="waifu"
    userid = str(command['user_id'])
    with open('./queue/'+str(time.time()), 'w') as f:
        f.write(userid+"\n"+userInput+"\n"+mode+"\n"+"private")
    respond(f"<@{userid}>"+" プライベートキューに追加しました:"+userInput)

@app.command("/stable")
def todo(ack, respond, command):
    ack()
    userInput = command['text']
    mode="stable"
    userid = str(command['user_id'])
    with open('./queue/'+str(time.time()), 'w') as f:
        f.write(userid+"\n"+userInput+"\n"+mode+"\n"+"private")
    respond(f"<@{userid}>"+" プライベートキューに追加しました:"+userInput)

@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)

SocketModeHandler(app, SLACK_APP_TOKEN).start()
