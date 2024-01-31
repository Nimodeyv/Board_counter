# 1. Installer fastapi dans l'environnement: conda install fastapi
# 2. Installer uvicorn : conda install "uvicorn[standard]"
# 3. Ouvrir un terminal dans le répertoire app
# 4. Se placer dans l'environnement conda, Lancer uvicorn dans le terminal: uvicorn main:app --reload
# 5. Ouvrir une page web http://127.0.0.1:8000/docs
# 6. Pour lancer depuis Docker: Creer une image docker avec Dockerfile
# 7. Pour utiliser Docker, Voir tutorial

from fastapi import FastAPI
from fastapi.responses import FileResponse
from ultralytics import YOLO
from datetime import datetime
from pydantic import BaseModel, Field
import cv2
import import_functions

model_path = r'./model/last.pt'
model = YOLO(model_path)

app = FastAPI(title="Wood board Counter",
             version='5.1',
              contact={'name':'nimodeyv'})


class Image(BaseModel):
    seuil_de_detection : float = Field(default = 0.3)
    path : str = Field(default =  "./raw_images/IMG_0287.JPG")
    crop_horiz_min : int = Field(default = 0)
    crop_horiz_max : int = Field(default = 0)
    crop_vert_min : int = Field(default = 0)
    crop_vert_max : int = Field(default = 0)

@app.post("/predict/")
async def predict(f:Image):
    img = cv2.imread(f.path)
    if f.crop_horiz_max == 0: f.crop_horiz_max = img.shape[0]
    if f.crop_vert_max == 0: f.crop_vert_max = img.shape[1]  
    img = img[f.crop_horiz_min:f.crop_horiz_max, f.crop_vert_min:f.crop_vert_max, :]
    
    results = model.predict(source=img, # image_to_predict
                            show=False, 
                            conf=f.seuil_de_detection,
                            save=False, 
                            line_width=3,
                            project='Board_counter',
                            );
    # import_functions.show(results, f.crop_horiz_min, f.crop_horiz_max, 
    #                       f.crop_vert_min, f.crop_vert_max)
    import_functions.show(results)
    return FileResponse('./predict/predict_image.JPG')#,headers={"nb de planches":results[0].__len__() , "fichier":f.path})
    
@app.get("/healthcheck")
def health():
    return {"Hello": f"It is now: {datetime.now()}"}

