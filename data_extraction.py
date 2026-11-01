import pandas as pd
import requests
import os


# definim cele clădirile pe care le vrem
cladirile_alese = {
    "123731": "Castelul_Peles",
    "34840": "Castelul_Bran",
    "47378": "Turnul_Eiffel",
    "114046":"Milan_Duomo",
    "145268":"Louvre",
    "16146":"Koln_Cathedral"
}

NUMAR_POZE_PER_CLADIRE = 100

def construieste_dataset():
    print("Incarcam fisierele CSV...")
    train_df = pd.read_csv('train.csv')
    
    headere = {'User-Agent': 'ProiectAcademic_ComputerVision/1.0 (contact_student@univ.ro)'}

    for landmark_id, nume_folder in cladirile_alese.items():
        print(f"Procesam: {nume_folder}...")
        cale_folder = os.path.join("Dataset_Proiect", nume_folder)
        os.makedirs(cale_folder, exist_ok=True)
        
        # filtrare dupa id
        imagini_cladire = train_df[train_df['landmark_id'] == int(landmark_id)]
        imagini_alese = imagini_cladire.head(NUMAR_POZE_PER_CLADIRE)
        
        # descarcare
        count = 0
        for index, rand in imagini_alese.iterrows():
            id_imagine = rand['id']
            url_poza = rand['url']
            nume_fisier = f"{cale_folder}/{id_imagine}.jpg"

            if os.path.exists(nume_fisier):
                #print(f"Poza {id_imagine} exista deja. Trecem peste.")
                count += 1
                continue
            

            try:
                raspuns = requests.get(url_poza,headers=headere, timeout=10)
                if raspuns.status_code == 200:
                    with open(nume_fisier, 'wb') as f:
                        f.write(raspuns.content)
                        count += 1
            except:
                pass#daca linkul nu functioneaza
                    
        print(f"Am descarcat {count} poze pentru {nume_folder}.")


construieste_dataset()