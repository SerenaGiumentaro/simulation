import pygame

# image
cell = pygame.image.load("assents/cell.png")
dead = pygame.image.load("assents/deadCell.png")

# variable
width = 1000
hight = 800
baseDNA = {"cells": [{"organnels": ["ribosoma"], "color": (255, 255, 255), "splitCell": [0, 0], "rotation": [],"MembraneResisten": 1}]}
bobDNA = {
    "cells": [
        {
            "organnels": ["mitocondro","flagello","ribosoma","lisoma"],
            "color": (255, 70, 70),
            "splitCell": [0, 0],
            "rotation": [0],
            "MembraneResisten": 3
        }
    ]
}
plantDNA = {
    "cells": [
        {
            "organnels": ["tilacoidi", "tilacoidi", "tilacoidi","vacuolo","tilacoidi","ribosoma"],
            "color": (120, 255, 120),
            "splitCell": [0, 0],
            "rotation": [],
            "MembraneResisten": 4
        }
    ]
}
cells = []
sostanze = []
TypeSostanze = {"glucosio":{"color":(255,255,255)},"lipidi":{"color":(255,200,100)}, "Ammoniaca":{"color":(255,100,0)}}
Luce = 50
ossigeno = 20
ChangeLuce = 0.01
waterDirection = 45
