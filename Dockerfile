FROM python:3.10

RUN pip3 install --upgrade pip

RUN mkdir /chatbot

COPY requirements.txt /chatbot

WORKDIR /chatbot

RUN pip3 install -r requirements.txt 

COPY . /chatbot

EXPOSE 8030

CMD ["python3", "websocket_app.py"]
