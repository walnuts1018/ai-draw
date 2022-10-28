import dill
from dotenv import load_dotenv
import os
from diffusers import StableDiffusionPipeline

load_dotenv()
YOUR_TOKEN=os.environ.get("HUG_TOKEN")

# StableDiffusion pipe
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", use_auth_token=YOUR_TOKEN)
pipe.to("cuda")
pipe.safety_checker = lambda images, **kwargs: (images, False)

#pipe保存
with open('pipe_stable.pkl', 'wb') as p:
    dill.dump(pipe, p)
