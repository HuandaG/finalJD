# Base de AWS Lambda Python 3.11
FROM public.ecr.aws/lambda/python:3.11

# Copiar requirements y app
COPY requirements.txt .
COPY app.py ${LAMBDA_TASK_ROOT}/

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando Lambda
CMD ["app.mangum"]
