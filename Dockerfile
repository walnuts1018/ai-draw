FROM nvidia/cuda:11.7.0-cudnn8-devel-ubuntu22.04 
USER root

RUN apt update
RUN apt install python3 python3-pip locales nano less -y&& \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade setuptools
RUN python3 -m pip install python-dotenv slack_bolt diffusers==0.3.0 transformers scipy ftfy dill torch==1.12.0+cu113 torchvision==0.13.0+cu113 torchaudio==0.12.0 -f https://download.pytorch.org/whl/torch_stable.html

RUN mkdir /stable-diffusion
CMD python3 gen.py & python3 regist.py
