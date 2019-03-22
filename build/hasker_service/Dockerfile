FROM python:3.5

WORKDIR /opt/hasker
#ENV PYTHON /usr/bin/python3
COPY . /opt/hasker

RUN apt-get update
RUN apt-get update && \
    apt-get install -y && \
    pip3 install --trusted-host pypi.python.org -r /opt/hasker/build/hasker_service/requirements.txt
RUN git config --global user.email "ilya.aurov@gmail.com"
RUN git config --global user.name "Ilya"
ENV SECRET_KEY 'vq*ag#8x3#cx!sdj!w3ij_=)3^n(f-uk0sx95-s3__0=683=r#'
ENV DATABASE_PASSWORD 'hasker'
ENV HASKER_DB_HOST 'db'
ENV HASKER_DB_PORT '5432'
EXPOSE 8000
