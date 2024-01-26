# 1. Installer fastapi dans l'environnement: conda install fastapi
# 2. Installer uvicorn : conda install "uvicorn[standard]"
# 3. Lancer uvicorn dans un terminal: uvicorn main:app --reload
# 4. Ouvrir une page web http://127.0.0.1:8000/docs ou 

from fastapi import FastAPI, File, UploadFile
from ultralytics import YOLO
# import cv2
# from typing import Union
from datetime import datetime
from pydantic import BaseModel

model_path = r'./model_v2/v2.1_25_epochs/last.pt'
model = YOLO(model_path)

app = FastAPI()


class Image(BaseModel):
    path : str


@app.post("/predict/")
async def predict(f:Image):
    # return {"fichier":f.path}
    # # i = cv2.imread(f.path)
    # # im = cv2.cvtColor(i, cv2.COLOR_BGR2RGB)
    conf = 0.3
    results = model.predict(source=f.path, # image_to_predict
                            show=False, 
                            conf=conf,
                            save=False, 
                            line_width=3,
                            project='Board_counter',
                            );
    return {"nb de planches":results[0].__len__() , "fichier":f.path}
    
@app.get("/healthcheck")
def health():
    return {"Hello": f"It is now: {datetime.now()}"}

