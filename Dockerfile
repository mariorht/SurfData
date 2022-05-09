FROM python:3.8.10

RUN apt update
RUN apt install -y --no-install-recommends
RUN apt install -y python3-opencv

RUN pip install --upgrade pip

RUN mkdir /app
WORKDIR /app
COPY ./surfData /app
COPY requirements.txt /app


RUN pip install -r requirements.txt

# ENTRYPOINT ["python"]
# CMD ["update_db.py"]