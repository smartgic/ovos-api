FROM python:3.10

LABEL vendor=Smartgic.io \
    io.smartgic.maintainer="Gaëtan Trellu <gaetan.trellu@smartgic.io>"

RUN pip install fastapi uvicorn passlib[bcrypt] pyjwt

EXPOSE 8000

COPY ./app /app

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]