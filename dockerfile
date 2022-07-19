FROM python:3.10.5

WORKDIR /Exchange_rates_tg_bot

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]