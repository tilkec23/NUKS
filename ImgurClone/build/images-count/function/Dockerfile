FROM python:3.9-slim

RUN pip install pymongo

COPY . /ImgurClone

WORKDIR /ImgurClone

CMD ["python", "handler.py"]
