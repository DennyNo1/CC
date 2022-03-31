#test
FROM python
COPY chatbot.py/ .
COPY requirements.txt/ .
EXPOSE 80
ENV ACCESS_TOKEN=5135823339:AAGUcCNQHpFHgVEOYJ51gFDri-I-T3LY9mk
ENV HOST="redis-11577.c262.us-east-1-3.ec2.cloud.redislabs.com"
ENV PASSWORD="Dolkt9Am6w9Qdc7rTGeWZZuwdKKZeWOa"
ENV REDISPORT=11577
RUN pip install pip update
RUN pip install -r requirements.txt
CMD python chatbot.py





