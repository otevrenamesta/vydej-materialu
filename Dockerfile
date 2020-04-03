FROM python:3.8-slim

RUN mkdir /app
WORKDIR /app

COPY requirements requirements/
RUN pip install -r requirements/base.txt -r requirements/prod.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE "config.settings.production"

# fake values for required env variables used to run collectstatic during build
RUN DJANGO_SECRET_KEY=x DATABASE_URL=postgres://x/x DJANGO_ALLOWED_HOSTS=x SITE_URL=x\
    python manage.py collectstatic

EXPOSE 8000

CMD ["bash", "run.sh"]
