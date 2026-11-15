import pandas as pd
import requests
import os
import time


# definim cele clădirile pe care le vrem
cladirile_alese = {
    #"123731": "Castelul_Peles",
    #"34840": "Castelul_Bran",
    "47378": "Turnul_Eiffel",
    "114046":"Milan_Duomo",
    "145268":"Louvre",
    "16146":"Koln_Cathedral",
    "80402":"Big_Ben",
    "163459":"Burj_Khalifa",
    "22029":"Sagrada_Familia",
    "55350":"Sydney_Opera_House",
    "38055":"London_Eye",
    "28949":"Moulin_Rouge"
}

NUMAR_POZE_PER_CLADIRE = 100

def construieste_dataset():
    print("Incarcam fisierele CSV...")
    train_df = pd.read_csv('train.csv')
    
    sesiune = requests.Session()
    sesiune.headers.update({
        'User-Agent': 'ProiectAcademicMonumente/1.0 (contact_student@univ.ro)'
    })

    for landmark_id, nume_folder in cladirile_alese.items():
        print(f"Procesam: {nume_folder}...")
        cale_folder = os.path.join("Dataset_Proiect", nume_folder)
        os.makedirs(cale_folder, exist_ok=True)
        
        # filtrare dupa id
        imagini_cladire = train_df[train_df['landmark_id'] == int(landmark_id)]
        print(f"\nProcesam: {nume_folder} (ID: {landmark_id}) -> {len(imagini_cladire)} linkuri gasite in CSV")

        #imagini_alese = imagini_cladire.head(NUMAR_POZE_PER_CLADIRE)
        if len(imagini_cladire) == 0:
            print(f"  ATENTIE: ID-ul {landmark_id} nu exista in fisierul train.csv!")
            continue
        # descarcare
        count = 0
        eroare=False
        for index, rand in imagini_cladire.iterrows():
            if count >= NUMAR_POZE_PER_CLADIRE:
                break
            id_imagine = rand['id']
            url_poza = rand['url']
            nume_fisier = f"{cale_folder}/{id_imagine}.jpg"

            if os.path.exists(nume_fisier):
                #print(f"Poza {id_imagine} exista deja. Trecem peste.")
                count += 1
                continue
            
            
            incercari = 0
            max_incercari = 3

            while incercari < max_incercari:
                try:
                    raspuns = sesiune.get(url_poza, timeout=10)
                    
                    if raspuns.status_code == 200:
                        with open(nume_fisier, 'wb') as f:
                            f.write(raspuns.content)
                        count += 1
                        time.sleep(0.5)
                        break  # Poza a fost salvata -> iesim din while si trecem la urmatoarea
                        
                    elif raspuns.status_code == 429:
                        incercari += 1
                        print(f"  Serverul cere pauza (429). Reincercam aceeasi poza ({incercari}/{max_incercari}) in 20s...")
                        time.sleep(20)
                        
                    else:
                        if not eroare:
                            print(f"  Exemplu eroare HTTP {raspuns.status_code} la linkul: {url_poza}")
                            eroare = True
                        time.sleep(1.0)
                        break  
                        
                except Exception as e:
                    incercari += 1
                    if not eroare:
                        print(f"  Eroare conexiune: {e}")
                        eroare = True
                    time.sleep(2)
                    
        print(f"Am descarcat {count} poze pentru {nume_folder}.")


construieste_dataset()