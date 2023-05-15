FROM python:3.8.16-alpine3.18 AS base


ARG COMMIT_HASH
LABEL com.example.commit-hash=${COMMIT_HASH}


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .


RUN pytest

# Exposition du port du container
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]