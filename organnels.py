import pygame
import assents
import random

def find(cell, cosa):
    for i in cell["organels"]:
        if i["type"] == cosa:
            return i
    return None

def findNumb(cell, cosa):
    a = 0
    for i in cell["organels"]:
        if i["type"] == cosa:
            a += 1
    return a

def addOrganel(cell, organel, rotation):
    if organels[organel]["type"] != "Part":
        if CalcoloDimension(cell) >= organels[organel]["proprietes"]["dimension"]:
            cell["organels"].append(
                {
                    "type": organel,
                    "rotation": random.randint(0, 360),
                    "dimension": random.randint(25, len(cell["DNA"]["cells"][cell["nCell"]]["organnels"]) * 5 + 25)
                }
            )
    else:
        cell["organels"].append(
                {
                    "type": organel,
                    "rotation": rotation,
                    "dimension": random.randint(25, len(cell["DNA"]["cells"][cell["nCell"]]["organnels"]) * 5 + 25)
                }
            )

def CalcoloMaxSostanza(cell):
    MaxS = 1
    for i in range(len(cell["organels"])):
        if "stoccaggio" in organels[cell["organels"][i]["type"]]["proprietes"]:
            MaxS += organels[cell["organels"][i]["type"]]["proprietes"]["stoccaggio"]
    return MaxS

def CalcoloDimension(cell):
    SpaceRim = cell["dimension"] - 25
    for i in range(len(cell["organels"])):
        if organels[cell["organels"][i]["type"]]["type"] == "organnel":
            SpaceRim -= organels[cell["organels"][i]["type"]]["proprietes"]["dimension"]
    return SpaceRim

def glucoisi(cell, organel):
    if "glucosio" in cell["sostanze"]:
        if cell["sostanze"]["glucosio"] >= 0.1:
            cell["sostanze"]["glucosio"] -= 0.1 
            cell["ATP"] += 0.5
            if cell["ATP"] > cell["MaxATP"]:
                cell["ATP"] = cell["MaxATP"]

def respirazioneAerobica(cell, organel):
    if "glucosio" in cell["sostanze"] and cell["sostanze"]["glucosio"] >= 0.1:
        if assents.ossigeno > 0.05:  # Assicurati che ci sia abbastanza ossigeno
            cell["sostanze"]["glucosio"] -= 0.05
            # Aggiungi una quantità di ATP che riflette la respirazione aerobica, ipotizziamo qui 18 volte il tasso anaerobico
            incremento_ATP = 1.8  # Più realistico rispetto a 0.1 * ossigeno, ma ancora una semplificazione
            cell["ATP"] += incremento_ATP
            assents.ossigeno -= 0.1  # Consuma una quantità fissa di ossigeno
            if cell["ATP"] > cell["MaxATP"]:
                cell["ATP"] = cell["MaxATP"]
        else:
            # Gestisci il caso di basso ossigeno (potresti decidere di passare a una via metabolica differente o ridurre l'ATP prodotto)
            glucoisi(cell, organel)
    a = random.randint(0,10)
    if a == 10 and "Proteine" in cell["sostanze"] and cell["sostanze"]["Proteine"] >= 1:
        cell["sostanze"]["Proteine"] -= 1
        if "stage" in cell["organels"][organel]:
            cell["organels"][organel]["stage"] += 1
            if cell["organels"][organel]["stage"] == 5:
                addOrganel(cell, "mitocondro", None)
        else:
            cell["organels"][organel]["stage"] = 1
        
def aminoacidi(cell):
    MaxS = CalcoloMaxSostanza(cell)
    if "Ammoniaca" in cell["sostanze"]:
        if cell["sostanze"]["Ammoniaca"] >= 0.1:
            cell["sostanze"]["Ammoniaca"] -= 0.1 
            if not "Aminoacidi" in cell["sostanze"]:
                cell["sostanze"]["Aminoacidi"] = 0.1
            else:
                NewAminoacidi =  cell["sostanze"]["Aminoacidi"] + 0.1
                cell["sostanze"]["Aminoacidi"] = min(MaxS, NewAminoacidi)

def Nucelo(cell):
    aminoacidi(cell)
    a = random.randint(0,100)
    if a == 10 and "Proteine" in cell["sostanze"] and cell["sostanze"]["Proteine"] >= 1:
        cell["sostanze"]["Proteine"] -= 1 
        addOrganel(cell, "ribosoma", None)
    if "flagello" in cell["DNA"]["cells"][cell["nCell"]]["organnels"]:
        numero_flagelli = sum(1 for org in cell["organels"] if org["type"] in ["MINIflagello", "flagello"])
        limite = 0
        for i in cell["DNA"]["cells"][cell["nCell"]]["organnels"]:
            if  i == "flagello":
                limite += 2
        if numero_flagelli < limite:
            b  = find(cell, "MINIflagello")
            a = random.randint(0,10)
            if b is None:  
                if a == 10 and "Proteine" in cell["sostanze"] and cell["sostanze"]["Proteine"] >= 1:
                    cell["sostanze"]["Proteine"] -= 1 
                    addOrganel(cell, "MINIflagello",  cell["DNA"]["cells"][cell["nCell"]]["rotation"][random.randint(0,len(cell["DNA"]["cells"][cell["nCell"]]["rotation"])-1)] + random.randint(-20,20))

def proteine(cell, organel):
    MaxS = CalcoloMaxSostanza(cell)
    if "Aminoacidi" in cell["sostanze"]:
        if cell["sostanze"]["Aminoacidi"] >= 0.05:
            cell["sostanze"]["Aminoacidi"] -= 0.05 
            if not "Proteine" in cell["sostanze"]:
                cell["sostanze"]["Proteine"] = 0.05
            else:
                NewProteine =  cell["sostanze"]["Proteine"] + 0.05
                cell["sostanze"]["Proteine"] = min(MaxS, NewProteine)
        if random.randint(0,50) == 10:
            LisomaNumb = findNumb(cell, "lisoma")
            if LisomaNumb != 0:
                if cell["sostanze"]["Aminoacidi"] >= 1:
                    cell["sostanze"]["Aminoacidi"] -= 1 
                    if not "Enzimi" in cell["sostanze"]:
                        cell["sostanze"]["Enzimi"] = 1
                    else:
                        NewEnzimi =  cell["sostanze"]["Enzimi"] + 1
                        cell["sostanze"]["Enzimi"] = min(LisomaNumb*10, NewEnzimi)

def fotosintesi(cell, organel):
    MaxS = CalcoloMaxSostanza(cell)
    if not "glucosio" in cell["sostanze"]:
        cell["sostanze"]["glucosio"] = 0
    NewGlucosio =  cell["sostanze"]["glucosio"] + assents.Luce / 1000
    cell["sostanze"]["glucosio"] = min(MaxS, NewGlucosio)
    assents.ossigeno += 0.01

def fotosintesiMat(cell, organel):
    MaxS = CalcoloMaxSostanza(cell)
    if not "glucosio" in cell["sostanze"]:
        cell["sostanze"]["glucosio"] = 0
    NewGlucosio =  cell["sostanze"]["glucosio"] + assents.Luce / 2500
    cell["sostanze"]["glucosio"] = min(MaxS, NewGlucosio)
    assents.ossigeno += 0.003
    a = random.randint(0,10)
    if a == 10 and "Proteine" in cell["sostanze"] and cell["sostanze"]["Proteine"] >= 1 and "lipidi" in cell["sostanze"] and cell["sostanze"]["lipidi"] >= 1:
        cell["sostanze"]["Proteine"] -= 1
        cell["sostanze"]["lipidi"] -= 1 
        if "stage" in cell["organels"][organel]:
            cell["organels"][organel]["stage"] += 1
            if cell["organels"][organel]["stage"] == 10:
                addOrganel(cell, "tilacoidi", cell["organels"][organel]["rotation"])
                cell["organels"].remove(cell["organels"][organel])
        else:
            cell["organels"][organel]["stage"] = 1

def flagelloGrow(cell, organel):
    a = random.randint(0,10)
    if a == 10 and "Proteine" in cell["sostanze"] and cell["sostanze"]["Proteine"] >= 1:
        cell["sostanze"]["Proteine"] -= 1 
        if "stage" in cell["organels"][organel]:
            cell["organels"][organel]["stage"] += 1
            if cell["organels"][organel]["stage"] == 20:
                addOrganel(cell, "flagello", cell["organels"][organel]["rotation"])
                cell["organels"].remove(cell["organels"][organel])
        else:
            cell["organels"][organel]["stage"] = 1

def vacuoloRP(cell, organel):
    a = random.randint(0,10)
    if a == 10 and "Proteine" in cell["sostanze"] and cell["sostanze"]["Proteine"] >= 1:
        cell["sostanze"]["Proteine"] -= 1 
        if "stage" in cell["organels"][organel]:
            cell["organels"][organel]["stage"] += 1
            if cell["organels"][organel]["stage"] == 7:
                addOrganel(cell, "vacuoloRPR", cell["organels"][organel]["rotation"])
                cell["organels"].remove(cell["organels"][organel])
        else:
            cell["organels"][organel]["stage"] = 1

def vaculoGrow(cell, organel):
    a = random.randint(0,10)  
    if a == 10 and "Proteine" in cell["sostanze"] and cell["sostanze"]["Proteine"] >= 1:
        cell["sostanze"]["Proteine"] -= 1 
        if "stage" in cell["organels"][organel]:
            cell["organels"][organel]["stage"] += 1
            if cell["organels"][organel]["stage"] == 10:
                addOrganel(cell, "vacuolo", cell["organels"][organel]["rotation"] + random.randint(-15,15))
                addOrganel(cell, "vacuolo", cell["organels"][organel]["rotation"] + random.randint(-15,15))
                cell["organels"].remove(cell["organels"][organel])
        else:
            cell["organels"][organel]["stage"] = 1

def lisomaRP(cell, organel):
    if random.randint(0,10) == 10 and "Proteine" in cell["sostanze"] and cell["sostanze"]["Proteine"] >= 1:
        cell["sostanze"]["Proteine"] -= 1
        if "stage" in cell["organels"][organel]:
            cell["organels"][organel]["stage"] += 1
            if cell["organels"][organel]["stage"] == 5:
                addOrganel(cell, "lisoma", None)
        else:
            cell["organels"][organel]["stage"] = 1

organels = {
    "metabolosoma": {
        "processo": glucoisi,
        "image": pygame.image.load("assents/organelli/digestilo.png"),
        "proprietes": {"stoccaggio": +1, "CostoVita": +1,"dimension":5, "Speed":-0.07, "damegeToDead": 3},
        "type":"Organnel",
        "ricicle":{"proteine":3}
    },
    "mitocondro": {
        "processo": respirazioneAerobica,
        "image": pygame.image.load("assents/organelli/mitocondro.png"),
        "proprietes": {"stoccaggio": +1, "CostoVita": +2,"dimension":7, "Speed":-0.1, "damegeToDead": 5},
        "type":"Organnel",
    },
    "tilacoidi": {
        "processo": fotosintesi,
        "image": pygame.image.load("assents/organelli/fotosensibile.png"),
        "proprietes": {"stoccaggio": +1, "CostoVita": +1,"dimension":5, "Speed":-0.07, "damegeToDead": 3},
        "type":"Organnel",
        "ricicle":{"proteine":5,"lipidi":5}
    },
    "tilacoidiMat": {
        "processo": fotosintesiMat,
        "image": pygame.image.load("assents/organelli/fotosensibileMat.png"),
        "proprietes": {"CostoVita": +0.7,"dimension":3, "Speed":-0.05, "damegeToDead": 2},
        "type":"Organnel",
        "ricicle":{"proteine":3,"lipidi":3}
    },
    "centriolo": {
        "processo": None,
        "image": pygame.image.load("assents/organelli/centriolo.png"),
        "proprietes": {"CostoVita": +1, "SplitProces": -700,"dimension":4, "Speed": -0.05},
        "type":"Organnel"
    },
    "vacuolo": {
        "processo": vacuoloRP,
        "image": pygame.image.load("assents/organelli/vacuolo.png"),
        "proprietes": {"CostoVita": +1, "stoccaggio": +5,"dimension":10, "Speed": -0.5, "damegeToDead": 8},
        "type":"Organnel",
        "ricicle":{"proteine":14}
    },
    "vacuoloRPR": {
        "processo": vaculoGrow,
        "image": pygame.image.load("assents/organelli/vacuoloRPR.png"),
        "proprietes": {"CostoVita": +1.3, "stoccaggio": +6,"dimension":12, "Speed": -0.6, "damegeToDead": 10},
        "type":"Organnel",
        "ricicle":{"proteine":16}
    },
    "flagello":{
        "processo":None,
        "image":pygame.image.load("assents/organelli/flagello.png"),
        "proprietes": {"CostoVita": +3, "Speed": +3, "damegeToDead": 7},
        "type":"Part",
        "ricicle":{"proteine":10}
    },
    "MINIflagello":{
        "processo":flagelloGrow,
        "image":pygame.image.load("assents/organelli/SMALLflagello.png"),
        "proprietes": {"CostoVita": +1, "Speed": +1, "damegeToDead": 5},
        "type":"Part",
        "ricicle":{"proteine":5}
    },
    "ribosoma": {
        "processo":proteine,
        "image":pygame.image.load("assents/organelli/ribosoma.png"),
        "proprietes": {"CostoVita": +0.5,"dimension":0.5, "Speed": -0.0007, "damegeToDead": 1},
        "type":"Organnel",
        "ricicle":{"proteine":0.05}
    },
    "lisoma": {
        "processo":lisomaRP,
        "image":pygame.image.load("assents/organelli/lisoma.png"),
        "proprietes": {"CostoVita": +1,"dimension":4, "Speed": -0.05},
        "type":"Organnel"
    }
}