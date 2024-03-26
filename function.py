import pygame
import random
import organnels
import assents
import math
from collections import defaultdict

def addCell(dna, position, ATP, sostanze, dimension, organels):
    nCell = len(dna["cells"])
    nuCell = 0
    if organels == "dna":
        Organels = []
        a = 0
        for i in range(len(dna["cells"][nuCell]["organnels"])):
            if organnels.organels[dna["cells"][nuCell]["organnels"][i]]["type"] == "Part":
                Organels.append(
                    {
                        "type": dna["cells"][nuCell]["organnels"][i],
                        "rotation": dna["cells"][nuCell]["rotation"][a],
                        "dimension": random.randint(25, dimension)
                    }
                )
                a += 1
            else:
                Organels.append(
                    {
                        "type": dna["cells"][nuCell]["organnels"][i],
                        "rotation": random.randint(0, 360),
                        "dimension": random.randint(25, dimension)
                    }
                )
    else:
        Organels = organels
    newCell = {
        "nCell": nuCell,
        "state": "alive",
        "life": len(dna["cells"][nuCell]["organnels"]) * 5 + 5,
        "organels": Organels,
        "ATP": ATP,
        "MaxATP": nCell * 10,
        "sostanze": sostanze,
        "DNA": dna,
        "rect": pygame.Rect(position[0], position[1], 25, 25),
        "direction": random.randint(0, 360),
        "dimension": dimension
    }
    coloredCell = assents.cell.copy()
    coloredCell = pygame.transform.scale(
        coloredCell,
        (
            dimension,
            dimension,
        ),
    )
    coloredCell.fill(
        newCell["DNA"]["cells"][newCell["nCell"]]["color"],
        special_flags=pygame.BLEND_RGBA_MULT,
    )
    newCell["image"] = coloredCell
    assents.cells.append(newCell)

def CalcoloCostoVita(cell):
    CoVi = 1
    for i in range(len(cell["organels"])):
        CoVi += organnels.organels[cell["organels"][i]["type"]]["proprietes"]["CostoVita"]
    return CoVi

def CalcolaSpeedy(cell):
    Speedy = 1
    for i in range(len(cell["organels"])):
        Speedy += organnels.organels[cell["organels"][i]["type"]]["proprietes"]["Speed"]
    return max(0,Speedy)

def lifeProcess(cell):
    CoVi = CalcoloCostoVita(cell)
    cell["ATP"] -= CoVi / 200
    if cell["ATP"] <= 0:
        cell["ATP"] = 0
        cell["life"] -= 0.05
        if cell["life"] <= 0:
            cell["state"] = "dead"
            cell["image"] = assents.dead.copy()
            cell["image"] = pygame.transform.scale(
                cell["image"],
                (
                    cell["dimension"],
                    cell["dimension"],
                ),
            )
            cell["image"].fill(
                tuple(max(0, min(255, t1 - 100)) for t1 in cell["DNA"]["cells"][cell["nCell"]]["color"]),
                special_flags=pygame.BLEND_RGBA_MULT,
            )
    for i in range(len(cell["organels"][:])):
        if not i > len(cell["organels"][:]):
            if organnels.organels[cell["organels"][i]["type"]]["processo"] is not None:
                organnels.organels[cell["organels"][i]["type"]]["processo"](cell, i)

def changeLight():
    if assents.Luce >= 100:
        assents.ChangeLuce = -0.01
    elif assents.Luce <= 0:
        assents.ChangeLuce = 0.01
    assents.Luce += assents.ChangeLuce

def MovimentoBrowniani(cellula):  
    speedy = CalcolaSpeedy(cellula)
    delta_x = speedy * math.cos(math.radians(cellula["direction"]))
    delta_y = speedy * math.sin(math.radians(cellula["direction"]))
    new_x = cellula["rect"].x + delta_x
    new_y = cellula["rect"].y + delta_y
    if new_x < 0 or new_x > assents.width:
        cellula["direction"] = (180 - cellula["direction"]) % 360
    if new_y < 0 or new_y > assents.hight:
        cellula["direction"] = (- cellula["direction"]) % 360
    cellula["rect"].x += speedy * math.cos(math.radians(cellula["direction"]))
    cellula["rect"].y += speedy * math.sin(math.radians(cellula["direction"]))
    a = random.randint(0, 100)
    if a < 20:  # Possiamo regolare questo valore per controllare la probabilità di cambiare direzione
        deviation = random.randint(-8, 8)  # Modifica l'ampiezza della deviazione
        cellula["direction"] += deviation
        cellula["direction"] %= 360  # Assicuriamoci che la direzione sia compresa tra 0 e 359 gradi

def dividiListe(list):
    gruppi = ([],[])
    conteggi_per_tipo = defaultdict(int)
    for elemento in list:
        conteggi_per_tipo[elemento['type']] += 1
    indice_gruppo_per_tipo = defaultdict(int)
    for elemento in list:
        tipo = elemento['type']
        gruppi[indice_gruppo_per_tipo[tipo] % 2].append(elemento)
        indice_gruppo_per_tipo[tipo] += 1
    return (gruppi)

def CalcoloSplitTime(cell):
    Speedy = 1000
    for i in range(len(cell["organels"])):
        Speedy += 500
        if "SplitProces" in organnels.organels[cell["organels"][i]["type"]]["proprietes"]:
            Speedy += organnels.organels[cell["organels"][i]["type"]]["proprietes"]["SplitProces"]
    return Speedy

def muteDNA(DNA):
    azione = random.choice(["remove", "remove", "duplicate", "duplicate", "changeColor", "changeColor", "changeColor", "changeColor","ChangeMR","ChangeMR","ChangeMR"])
    organelli = list(organnels.organels.keys())  # Assumi che questo elenchi tutti i possibili organelli
    Cell = random.randint(0, len(DNA["cells"]) - 1)
    if azione == "add":
        nuovo_organello = random.choice(organelli)
        DNA["cells"][Cell]["organnels"].append(nuovo_organello)
    elif azione == "duplicate":
        if DNA["cells"][Cell]["organnels"]:
            nuovo_organello = random.choice(DNA["cells"][Cell]["organnels"])
            DNA["cells"][Cell]["organnels"].append(nuovo_organello)
    elif azione == "remove" and DNA["cells"][Cell]["organnels"]:
        indice_da_rimuovere = random.randint(0, len(DNA["cells"][Cell]["organnels"]) - 1)
        DNA["cells"][Cell]["organnels"].pop(indice_da_rimuovere)
    elif azione == "changeColor":
        newColor = tuple(max(0, min(255, t1 + random.randint(-20, 20))) for t1 in DNA["cells"][Cell]["color"])
        DNA["cells"][Cell]["color"] = newColor
    elif azione == "ChangeMR":
        DNA["cells"][Cell]["MembraneResisten"] = max(0, DNA["cells"][Cell]["MembraneResisten"] + random.randint(-1,1))
    return DNA

def canSplit(cell):
    conteggi_organelli = {}
    for organello in cell["organels"]:
        tipo = organello['type']
        if tipo in conteggi_organelli:
            conteggi_organelli[tipo] += 1
        else:
            conteggi_organelli[tipo] = 1

    # Verifica se ci sono almeno due organelli per ogni tipo previsto nel DNA
    mancanti = []
    for tipo_previsto in cell["DNA"]["cells"][cell["nCell"]]["organnels"]:
        if conteggi_organelli.get(tipo_previsto, 0) < 2:
            mancanti.append(tipo_previsto)

    # Stampa il risultato della verifica
    if not mancanti:
        return True
    else:
        return False

def split(cell):
    if canSplit(cell):
        larghezza, altezza = cell["image"].get_size()
        cell["splitProces"] = 0
        x = cell["rect"].x + larghezza / 4
        y = cell["rect"].y + altezza / 4
        cell["ATP"] /= 2
        for sostanza in cell["sostanze"]:
            cell["sostanze"][sostanza] /= 2
        a = random.randint(0,15)
        if a == 5:
            NewDNA = muteDNA(cell["DNA"])
        else:
            NewDNA = cell["DNA"] #anche questo si ripete due volte, è necessario?
        # hai veramente bisogno di due if uguali?
        #potresti fare una funzione che faccia solo questa operazione
        if a == 1:
            cell["DNA"] = muteDNA(cell["DNA"])
        cell["organels"], NewOrganels = dividiListe(cell["organels"])
        cell["dimension"] / 2
        addCell(NewDNA, (x, y),cell["ATP"] ,cell["sostanze"], cell["dimension"], NewOrganels)

def addSostanza(type, quantity, xposition, yposition, xscale ,yscale):
    NewSostanza = {"type": type, "position":[xposition,yposition,xscale,yscale], "quantity": quantity}
    assents.sostanze.append(NewSostanza)

def AggiungiRobeACaso(n):
    for i in range(random.randint(1,n)):
        chiavi = list(assents.TypeSostanze.keys())
        type = chiavi[random.randint(0,len(chiavi)-1)]
        xp = random.randint(0,assents.width)
        yp = random.randint(0,assents.hight)
        xs = random.randint(100,400)
        ys = random.randint(100,400)
        q = random.randint(100,400)
        addSostanza(type, q, xp, yp, xs, ys)

def Crescita(cell):
    a = random.randint(0,100)
    if a == 10 and cell["sostanze"].get("lipidi", 0) >= 1 and cell["sostanze"].get("Proteine", 0) >= 1:
        if "tilacoidi" in cell["DNA"]["cells"][cell["nCell"]]["organnels"]:
            cell["sostanze"]["lipidi"] -= 0.2
            cell["sostanze"]["Proteine"] -= 0.2
            organnels.addOrganel(cell, "tilacoidiMat", random.randint(0,360))
        cell["sostanze"]["lipidi"] -= 0.25 * cell["DNA"]["cells"][cell["nCell"]]["MembraneResisten"]
        cell["sostanze"]["Proteine"] -= 0.25 * cell["DNA"]["cells"][cell["nCell"]]["MembraneResisten"]
        cell["dimension"] += 1
        coloredCell = assents.cell.copy()
        coloredCell = pygame.transform.scale(
            coloredCell,
            (
                cell["dimension"],
                cell["dimension"],
            ),
        )
        coloredCell.fill(
            cell["DNA"]["cells"][cell["nCell"]]["color"],
            special_flags=pygame.BLEND_RGBA_MULT,
        )
        cell["image"] = coloredCell
        for i in cell["organels"]:   
            i["dimension"] += 1

def decomposizione(cell):
    if random.randint(0,10) == 10:
        if "DecomState" in cell:
            cell["DecomState"] += 1
            if cell["DecomState"] == 500:
                assents.cells.remove(cell)
        else:
            cell["DecomState"] = 1

def inglobate(cell):
    cell["rect"].x, cell["rect"].y = cell["ParentCell"]["rect"].x, cell["ParentCell"]["rect"].y
    for Bsostanze, Bsostanza in cell["sostanze"].items():
        if Bsostanze in cell["ParentCell"]["sostanze"]:
            cell["ParentCell"]["sostanze"][Bsostanze] += 0.1
            Bsostanza -= 0.1
        else:
            cell["ParentCell"]["sostanze"][Bsostanze] = 0.1
            Bsostanza -= 0.1
    if "Enzimi" in cell["ParentCell"]["sostanze"]:
        EnzimiPower = max(0,round(cell["ParentCell"]["sostanze"]["Enzimi"] / 5 - cell["DNA"]["cells"][cell["nCell"]]["MembraneResisten"] / 2))
        ToDamege = random.randint(0, len(cell["organels"]))
        if ToDamege == len(cell["organels"]):
            cell["dimension"] -= EnzimiPower 
            cell["dimension"] = max(0, cell["dimension"])
            if "Proteine" in cell["ParentCell"]["sostanze"]:
                cell["ParentCell"]["sostanze"]["Proteine"] = min(organnels.CalcoloMaxSostanza(cell["ParentCell"]),cell["ParentCell"]["sostanze"]["Proteine"] + cell["ParentCell"]["sostanze"]["Enzimi"] / 2)
            else:
                cell["PParentCell"]["sostenze"]["Proteine"] = min(organnels.CalcoloMaxSostanza(cell["ParentCell"]),cell["ParentCell"]["sostanze"]["Enzimi"] / 2)
            if "lipidi" in cell["ParentCell"]["sostanze"]:
                cell["ParentCell"]["sostanze"]["lipidi"] = min(organnels.CalcoloMaxSostanza(cell["ParentCell"]),cell["ParentCell"]["sostanze"]["lipidi"] + cell["ParentCell"]["sostanze"]["Enzimi"] / 2)
            else:
                cell["ParentCell"]["sostanze"]["lipidi"] = min(organnels.CalcoloMaxSostanza(cell["ParentCell"]), cell["ParentCell"]["sostanze"]["Enzimi"] / 2)
            if cell["dimension"] <= 0:
                assents.cells.remove(cell)
                return
            coloredCell = assents.cell.copy()
            coloredCell = pygame.transform.scale(
                coloredCell,
                (
                    cell["dimension"],
                    cell["dimension"],
                ),
            )
            coloredCell.fill(
                cell["DNA"]["cells"][cell["nCell"]]["color"],
                special_flags=pygame.BLEND_RGBA_MULT,
            )
            cell["image"] = coloredCell
            for i in cell["organels"]:  
                i["dimension"] = max( 0 , i["dimension"] - EnzimiPower )
        else:
            if "damege" in cell["organels"][ToDamege]:
                cell["organels"][ToDamege]["damege"] += EnzimiPower 
                if cell["organels"][ToDamege]["damege"] >= organnels.organels[cell["organels"][ToDamege]["type"]]["proprietes"]["damageToDead"]:
                    for sostanza, quantità in organnels.organels[cell["organels"][ToDamege]["type"]]["ricicle"].item():
                        if sostanza in cell["ParentCell"]["sostanze"]:
                            cell["ParentCell"]["sostanze"][sostanza] = min(organnels.CalcoloMaxSostanza(cell["ParentCell"]),cell["ParentCell"]["sostanze"][sostanza] + quantità)
                        else:
                            cell["ParentCell"]["sostanze"][sostanza] = min(organnels.CalcoloMaxSostanza(cell["ParentCell"]),quantità)
                        cell["organels"].pop(ToDamege)
    if "EscapeStage" in cell:
        cell["EscapeStage"] += random.randint(0, round(CalcolaSpeedy(cell)) + 1)
        if cell["EscapeStage"] >= 400:
            cell["state"] = "alive"
            cell["rect"].x += cell["ParentCell"]["rect"].width * 2
            cell["rect"].y += cell["ParentCell"]["rect"].height * 2
            del cell["ParentCell"]
            del cell["EscapeStage"]
    else:
        cell["EscapeStage"] = random.randint(0, round(CalcolaSpeedy(cell)) + 1)