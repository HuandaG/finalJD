from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import csv
import io

# Inicializa la app
app = FastAPI(title="FastAPI CSV S3 App")

# Clase Pydantic para validar la entrada
class Persona(BaseModel):
    nombre: str
    edad: int
    altura: float

# Configura boto3 para S3
s3 = boto3.client("s3")
BUCKET_NAME = "ec2-jd"
FILE_NAME = "personas.csv"

# Endpoint POST: agregar datos al CSV en S3
@app.post("/agregar")
def agregar_persona(persona: Persona):
    # Intentar descargar el CSV existente
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
        csv_content = response["Body"].read().decode("utf-8")
        reader = list(csv.reader(io.StringIO(csv_content)))
    except s3.exceptions.NoSuchKey:
        # Si no existe, iniciamos la lista vacía
        reader = []

    # Agregar nueva fila
    reader.append([persona.nombre, persona.edad, persona.altura])

    # Guardar CSV actualizado en S3
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(reader)
    s3.put_object(Bucket=BUCKET_NAME, Key=FILE_NAME, Body=output.getvalue())

    return {"msg": "Persona agregada", "total": len(reader)}

# Endpoint GET: cantidad de filas en el CSV
@app.get("/cantidad")
def cantidad():
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
        csv_content = response["Body"].read().decode("utf-8")
        reader = list(csv.reader(io.StringIO(csv_content)))
        return {"filas": len(reader)}
    except s3.exceptions.NoSuchKey:
        return {"filas": 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
