import pygame
import assents
import random
import organnels
import math
import function

pygame.init()

schermo = pygame.display.set_mode((assents.width, assents.hight), pygame.RESIZABLE)

def drawnFromCenter(immagine, x, y):
    larghezza, altezza = immagine.get_size()
    schermo.blit(immagine, (x - larghezza // 2, y - altezza // 2))

def SpawnSostaze():
    a = random.randint(0,400)
    if a == 50:
        function.AggiungiRobeACaso(1)

def drawnOrganels(cell):
    for i in range(len(cell["organels"])):
        if  organnels.organels[cell["organels"][i]["type"]]["type"] == "Organnel":
            ThiseOrganels = pygame.transform.rotate(
                organnels.organels[cell["organels"][i]["type"]]["image"],
                cell["organels"][i]["rotation"],
            )
            ThiseOrganels = pygame.transform.scale(
                ThiseOrganels,
                (cell["organels"][i]["dimension"],cell["organels"][i]["dimension"]),
            )
            cell["organels"][i]["rotation"] += random.uniform(0.0001, 0.1)
            if cell["organels"][i]["rotation"] >= 360:
                cell["organels"][i]["rotation"] = 0
            drawnFromCenter(ThiseOrganels, cell["rect"].x, cell["rect"].y)
        if  organnels.organels[cell["organels"][i]["type"]]["type"] == "Part":
            ThiseOrganels = pygame.transform.rotate(
                organnels.organels[cell["organels"][i]["type"]]["image"],
                cell["direction"] + cell["organels"][i]["rotation"],
            )
            ThiseOrganels = pygame.transform.scale(
                ThiseOrganels, 
                (cell["dimension"] * 3, cell["dimension"] * 3)
            )
            drawnFromCenter(ThiseOrganels, cell["rect"].x, cell["rect"].y)

function.AggiungiRobeACaso(10)
function.addCell(assents.baseDNA, (500, 200), 10, {}, 30, "dna")
function.addCell(assents.bobDNA, (500, 400), 10, {}, 70, "dna")
for i in range(5):
    function.addCell(assents.plantDNA, (500+i*50, 600), 10, {}, 40, "dna")

def doCellsThings():
    for sss in assents.sostanze:
        pygame.draw.rect(schermo, assents.TypeSostanze[sss["type"]]["color"], sss["position"])
    for cell in assents.cells:              
        drawnFromCenter(
            cell["image"],
            cell["rect"].x,
            cell["rect"].y,
        )
        drawnOrganels(cell)
        if cell["state"] != "dead":
            function.Crescita(cell)
            organnels.Nucelo(cell)
            function.lifeProcess(cell)
            function.split(cell)
            organnels.glucoisi(cell, 0)
            if cell["state"] == "alive":
                function.MovimentoBrowniani(cell)
                for sss in assents.sostanze:
                    rect = pygame.Rect(sss["position"])
                    if rect.colliderect(cell["rect"]):
                        MaxS = organnels.CalcoloMaxSostanza(cell)
                        if not sss["type"] in cell["sostanze"]:
                            cell["sostanze"][sss["type"]] = 0
                        if cell["sostanze"][sss["type"]] < MaxS:
                            cell["sostanze"][sss["type"]] += 1
                            sss["quantity"] -= 1
                            if sss["quantity"] <= 0:
                                assents.sostanze.remove(sss)
                    sss["position"][0] -= 0.01 * math.cos(math.radians(assents.waterDirection))
                    if sss["position"][0] >= assents.width:
                        sss["position"][0] = 0
                    elif sss["position"][0] <= 0 - sss["position"][2]:
                        sss["position"][0] = assents.width
                    sss["position"][1] += 0.01 * math.sin(math.radians(assents.waterDirection))
                    if sss["position"][1] >=  assents.hight:
                        sss["position"][1] = 0
                    elif sss["position"][1] <= 0 - sss["position"][3]:
                        sss["position"][1] = assents.hight
                    a = random.randint(0,100)
                    if a == 100:
                        assents.waterDirection += random.randint(-1,1)
                for bCell in assents.cells:
                    if not cell == bCell:
                        if bCell["rect"].colliderect(cell["rect"]):
                            if bCell["state"] == "dead":
                                for Bsostanze, Bsostanza in bCell["sostanze"].items():
                                    if Bsostanze in cell["sostanze"]:
                                        cell["sostanze"][Bsostanze] += 0.1
                                        Bsostanza -= 0.1
                                    else:
                                        cell["sostanze"][Bsostanze] = 0.1
                                        Bsostanza -= 0.1
                            if bCell["state"] == "alive":
                                if organnels.CalcoloDimension(cell) > bCell["dimension"] * 1.1:
                                    bCell["state"] = "inglobed"
                                    bCell["ParentCell"] = cell
            if cell["state"] == "inglobed":
                function.inglobate(cell)
        else:
            function.decomposizione(cell)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.VIDEORESIZE:
            schermo = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            assents.width, assents.hight = schermo.get_size()
    schermo.fill((assents.Luce * 2, assents.Luce * 2, min(255,assents.ossigeno * 10)))
    doCellsThings()
    function.changeLight()
    SpawnSostaze()
    pygame.display.update()
    print(assents.cells)