FROM python:3.7
EXPOSE 5000
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD python run app.py --server.port 5000

