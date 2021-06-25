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
Nombre de variables total pour une grille = 5 * nbligne * nbcol
valeurs : 
- tigre : 1
- croco : 3
- requin : 2
- eau : 4
- terre : 5
ex clauses : -tigre v -eau

Pour l'écriture du fichier dimacs : reprendre principe pour sudoku 
-> insérer les clauses de bases que l'on sait pour chaque case de la grille ( par exemple le fait qu'on peut pas trouver 2 animaux par case, terre et eau sur la même etc...)
-> insérer les clauses qu'on déduit avec les informations récupérée grâce à l'API
-> après chaque découverte de cases, rajouter les nouvelles clauses qu'on peut déduire et avancer jusqu'à la fin comme ça ( par exemple des clauses qui interdisent d'avoir un crocodile si on a atteint le nombre max etc)

clauses de bases sur chaque case :
-1 v -2
-1 v -3
-2 v -3
-4 v -5
 4 v  5
-1 v -4
-3 v -5
            


fonction pour convertir une phrase en variable et inversement (cell to var, var to cell)

répertoire de travail du PROJET : 
- client/
- serveur/
    * bin/
        crocomine_serveur.sce 
    * cartes/
        croco1.croco
        croco2.croco

quand on execute : ./serveur/bin/crocomine.sce 
: 8000 serveur:cartes
pour python : ATOM avec mypy

tout sur machine 
-> lancer serveur ( executable : port,emplacement cartes(dossier))
-> ouvrir autre fenetre et faire du python dessus
-> importer module qui va bien / fichier d'exemple pour tester ( lancer sous forme impérative pour voir réponse serveur )
3 msg au serveur : "coucou, se présenter" (ping), "vouloir nouvelle carte" , requete de jeu ( soit chord, soit guess, soit discover)
renvoie sous forme triplet: statut,message,infos(dict avec mots clés)

Lors d'un GG, passer a la grille suivante, ne pas tenter de contredire le serveur en tentant une autre action etc ( même principe si KO)


ex demineur simple python:
https://openclassrooms.com/forum/sujet/exercice-debutant-intermediaire-demineur-12624?page=2#r5388663 : 
https://codes-sources.commentcamarche.net/source/101009-demineur
