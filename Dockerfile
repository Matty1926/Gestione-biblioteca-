FROM python:3.8-slim
WORKDIR /app
COPY  app.py .
COPY  templates ./templates 
RUN pip install flask
CMD ["python",  "/app/app.py"]
EXPOSE 5000