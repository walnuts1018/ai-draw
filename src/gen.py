import dill
import uuid
import os
from numpy import source
import requests
import time
from torch import autocast 
from PIL import Image
from torch import autocast
import time
import urllib.error
import urllib.request
from dotenv import load_dotenv

load_dotenv()
slack_token=os.environ.get("SLACK_BOT_TOKEN")

def draw(source_list):
    if source_list[2]=="stable":
        with open('pipe_stable.pkl', 'rb') as p:
            pipe = dill.load(p)
    elif source_list[2]=="waifu":
        with open('pipe_waifu.pkl', 'rb') as p:
            pipe = dill.load(p)
    filename = f"../outputs/{str(uuid.uuid4())}"
    prompt = source_list[1]
    image = pipe(prompt)["sample"][0]
    del pipe
    image.save(filename+".png")
    del image
    files = {'file': open(filename+".png", 'rb')}
    if source_list[3]=="public":
        channel="C045RAYE3DH"
    elif source_list[3]=="private":
        channel=source_list[0]
    param = {
        'token':slack_token, 
        'channels':channel,
        'filename':filename,
        'initial_comment': "<@"+source_list[0]+"> : "+source_list[1]+"(mode: "+source_list[2]+")",
        'title': "title"
    }
    result=requests.post(url="https://slack.com/api/files.upload",data=param, files=files)
    if source_list[3]=="public":
        pass
    elif source_list[3]=="private":
        os.remove(filename+".png")
        print("removed"+filename)
    #print(result.json())

def draw_img(source_list):
    cache_path=str(uuid.uuid4())+".png"
    headers = {f"Authorization': 'Bearer {slack_token}"}
    try:
        response = requests.get(source_list[4], allow_redirects=True, headers=headers, stream=True)
        with open(f"./cache/{cache_path}", 'wb') as f:
            # ファイルを保存する 
            f.write(response.content)
    except Exception as e:
        print('ダウンロードできませんでした。エラー：')
        print(e)
        return

    # 画像生成
    init_image = Image.open(f"./cache/{cache_path}").convert("RGB")
    init_image = init_image.resize((512, 512))
    prompt = source_list[1]
    with open('pipe_waifu.pkl', 'rb') as p:
        pipe = dill.load(p)

    filename = f"../outputs/{str(uuid.uuid4())}"
    with autocast("cuda"):
        images = pipe(
            prompt=prompt,          # プロンプト
            init_image=init_image,  # 入力画像
            strength=0.01,          # 入力画像と出力画像と相違度 (0.0〜1.0)
            guidance_scale=7.5,     # プロンプトと出力画像の類似度　(7〜11)
            num_inference_steps=50, # 画像生成に費やすステップ数
            ).images
    images[0].save(filename+".png")
    del pipe
    del images
    files = {'file': open(filename+".png", 'rb')}
    if source_list[3]=="public":
        channel="C045RAYE3DH"
    elif source_list[3]=="private":
        channel=source_list[0]
    param = {
        'token':slack_token, 
        'channels':channel,
        'filename':filename,
        'initial_comment': "<@"+source_list[0]+"> : "+source_list[1]+"(mode: "+source_list[2]+")",
        'title': "title"
    }
    result=requests.post(url="https://slack.com/api/files.upload",data=param, files=files)
    if source_list[3]=="public":
        pass
    elif source_list[3]=="private":
        os.remove(filename+".png")
        print("removed"+filename)

print("gen ready")
while True:
    files = sorted(os.listdir("./queue"))
    #print(files)
    if files != []:
        with open('./queue/'+files[0]) as f:
            lines = [s.strip() for s in f.readlines()]
        if len(lines)==5:
            draw_img(lines)
        else:
            draw(lines)
        os.remove('./queue/'+files[0])
    if len(files)<2:
        time.sleep(10)
