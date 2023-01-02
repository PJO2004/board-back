FROM {dockerimage}

RUN pip install --upgrade pip --user && \
    pip install uvicorn[standard] --user && \
    pip install fastapi_jwt_auth --user && \
    pip install requests --user && \
    pip install gunicorn --user && \
    pip install fastapi --user

EXPOSE 8000 

WORKDIR /usr/src/app

COPY . .

RUN apt-get update && \
    apt-get install -y unzip

RUN unzip hoho.zip -d /usr/src/app

RUN pip install -r requirement.txt

CMD ["main.py"]

ENTRYPOINT [ "python3" ]
