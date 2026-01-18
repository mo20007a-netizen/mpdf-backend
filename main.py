from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import subprocess, uuid, os

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/word-to-pdf")
async def word_to_pdf(file: UploadFile = File(...)):
    uid = str(uuid.uuid4())
    input_path = f"{UPLOAD_DIR}/{uid}.docx"
    output_path = f"{OUTPUT_DIR}/{uid}.pdf"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    subprocess.run([
        "libreoffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", OUTPUT_DIR,
        input_path
    ], check=True)

    return FileResponse(output_path, filename="word.pdf")
