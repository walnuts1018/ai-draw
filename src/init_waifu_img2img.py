import dill
import torch
from dotenv import load_dotenv
import os
from diffusers import StableDiffusionImg2ImgPipeline

load_dotenv()
YOUR_TOKEN=os.environ.get("HUG_TOKEN")

# StableDiffusionパイプライン
pipe = StableDiffusionImg2ImgPipeline.from_pretrained("hakurei/waifu-diffusion",torch_dtype=torch.float32, use_auth_token=YOUR_TOKEN)
pipe.to("cuda")
pipe.safety_checker = lambda images, **kwargs: (images, False)

with open('pipe_waifu_img.pkl', 'wb') as p:
    dill.dump(pipe, p)
