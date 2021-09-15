FROM python:3.9.7-slim

ENV LANG C.UTF-8

WORKDIR /app
COPY . /app

# 更换源
RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN sed -i s@/security.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get clean
RUN apt-get update
RUN apt-get install -y sudo
# 安装opencv运行时依赖
RUN sudo apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxrender1 libxext6

# 设置python安装源
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

EXPOSE 5001

VOLUME ["/logs"]

CMD ["python", "api.py"]
