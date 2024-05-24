FROM python:3.11 as requirements-stage

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "add_tag_openapi.py"]