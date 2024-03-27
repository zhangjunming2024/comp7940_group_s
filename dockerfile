FROM python:3.11
WORKDIR /comp7940_group_s
COPY . /comp7940_group_s
RUN pip install update
RUN pip install -r requirements.txt


CMD python chatbot.py