FROM python:3.13-slim

WORKDIR /src

COPY ./requirements.txt /requirements.txt

RUN python3 -m venv .venv

RUN chmod +x .venv/bin/activate

RUN .venv/bin/activate

RUN pip install --upgrade pip && pip install --no-cache-dir -r /requirements.txt

COPY . .

EXPOSE 8000

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["bash", "./entrypoint.sh"]
