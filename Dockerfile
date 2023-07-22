FROM python:3.11

WORKDIR /app
RUN pip install -U pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [ "./entrypoint.sh" ] 
