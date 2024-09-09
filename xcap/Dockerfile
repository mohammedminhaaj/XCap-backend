FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SECRET_KEY=django-insecure-n7ldr5emk7p3$o(!x%q54k*ocxz410+o%g_v70qe5honpjs8vc

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



