# 1. Installer fastapi dans l'environnement: conda install fastapi
# 2. Installer uvicorn : conda install "uvicorn[standard]"
# 3. Lancer uvicorn dans un terminal: uvicorn main:app --reload
# 4. Ouvrir une page web http://127.0.0.1:8000/docs
# TEST WITH ../raw_images/IMG_0287.JPG

# 5. Creer une image et lancer docker https://fastapi.tiangolo.com/fr/deployment/docker/  NE FONCTIONNE PAS

from fastapi import FastAPI
from fastapi.responses import FileResponse
from ultralytics import YOLO
from datetime import datetime
from pydantic import BaseModel, Field
import import_functions

model_path = r'../model_v2/v2.1_25_epochs/last.pt'
model = YOLO(model_path)

app = FastAPI()


class Image(BaseModel):
    seuil_de_detection : float = Field(default = 0.3)
    path : str = Field(default =  "../raw_images/IMG_0287.JPG")

@app.post("/predict/")
async def predict(f:Image):
    results = model.predict(source=f.path, # image_to_predict
                            show=False, 
                            conf=f.seuil_de_detection,
                            save=False, 
                            line_width=3,
                            project='Board_counter',
                            );
    import_functions.show(results)
    return FileResponse('./predict_image.JPG')#,headers={"nb de planches":results[0].__len__() , "fichier":f.path})
    
@app.get("/healthcheck")
def health():
    return {"Hello": f"It is now: {datetime.now()}"}

