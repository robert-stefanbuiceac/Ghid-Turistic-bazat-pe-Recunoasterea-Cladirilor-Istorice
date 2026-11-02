import os
import shutil
import random

random.seed(42)

def split_date():
    if not os.path.exists("Dataset_Proiect"):
        return

    for nume_clasa in os.listdir("Dataset_Proiect"):
        cale_clasa_sursa=os.path.join("Dataset_Proiect",nume_clasa)
        if not os.path.isdir(cale_clasa_sursa):
            continue

        imagini=[f for f in os.listdir(cale_clasa_sursa) if f.lower().endswith(('.jpg','.jpeg','.png'))]
        random.shuffle(imagini)

        numar_train=int(len(imagini)*0.8)
        imagini_train=imagini[:numar_train]
        imagini_validare=imagini[numar_train:]

        cale_train=os.path.join("Dataset_Proiect_Split","train",nume_clasa)
        cale_validare=os.path.join("Dataset_Proiect_Split","val",nume_clasa)

        os.makedirs(cale_train,exist_ok=True)
        os.makedirs(cale_validare,exist_ok=True)

        for img in imagini_train:
            shutil.copy(os.path.join(cale_clasa_sursa,img),os.path.join(cale_train,img))

        for img in imagini_validare:
            shutil.copy(os.path.join(cale_clasa_sursa,img),os.path.join(cale_validare,img))
        print(f" {nume_clasa}: {len(imagini_train)} imagini în Train | {len(imagini_validare)} imagini în Val")

split_date()