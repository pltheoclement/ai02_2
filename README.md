# IA02 Projet 

Projet IA02 sur le problème du démineur avec les tigres, crocodiles et requins

API: 
info [ {
    pos : (i,j)
    field : "sea"/"land"
    proxCount : (#tiger,#shark,#croco) // Optionnal
},
... ]

DIMACS avec tout les infos qu'on a 
clauses : 5 variables par case: tigre,croco,requin,eau,terre
ex clauses : -tigre v -eau
                terre et eau 
fonction pour convertir une phrase en variable et inversement (cell to var, var to cell)


pour python : ATOM avec mypy


ex demineur simple python:
https://openclassrooms.com/forum/sujet/exercice-debutant-intermediaire-demineur-12624?page=2#r5388663 : 
https://codes-sources.commentcamarche.net/source/101009-demineur
