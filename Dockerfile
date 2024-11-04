FROM python:3
EXPOSE 5000
WORKDIR /app
RUN pip3 install flask
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]