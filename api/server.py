from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from core.model_handler import ModelHandler
from data.image_pipeline import load_and_preprocess_image

app = FastAPI()
model_handler = ModelHandler()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, 'wb') as f:
        f.write(contents)
    
    image_tensor = load_and_preprocess_image(temp_file_path)
    prediction = model_handler.predict(image_tensor)

    os.remove(temp_file_path)
    return {"class": prediction}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)