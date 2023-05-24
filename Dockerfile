FROM cimg/python:3.8.16

# python:3.8.16-alpine3.18
# python:3.8.16-slim-bullseye
# cimg/python:3.8.16


# ARG COMMIT_HASH
# ENV COMMIT_HASH=$COMMIT_HASH
# LABEL com.example.commit-hash=${COMMIT_HASH}

# ENV PIP_DISABLE_PIP_VERSION_CHECK 1
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

ENV PORT=8000


WORKDIR /app

COPY requirements.txt /app/

# RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
# COPY . .

# RUN mkdir -p /app/staticfiles
# RUN chmod -R 755 /app/staticfiles
# RUN python manage.py collectstatic --noinput


# Exposition du port du container
EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:$PORT"]
# CMD gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:$PORT
CMD python manage.py collectstatic --noinput; python manage.py runserver 0.0.0.0:$PORT
