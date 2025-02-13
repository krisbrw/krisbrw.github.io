FROM amazonlinux:latest

WORKDIR /bin/src/app

RUN yum update -y && \
    yum install wget -y 

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm && \
    yum install -y \
    ./google-chrome-stable_current_x86_64.rpm \
    python3 \
    python3-pip

RUN pip install pandas \
    selenium \
    webdriver_manager \
    flask \
    jsons

COPY app.py .

EXPOSE 5000

CMD ["sh", "-c", "python3 app.py && tail -f /dev/null"]