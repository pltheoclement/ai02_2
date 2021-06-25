    # IA02 Projet 
Clément Douale, groupe 66
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



****Explication du programme :****

Pour lancer le programme :
    - se placer dans le path ou se situe le fichier python et le client, puis lancer : py .\projet.py

Le programme ajoute premièrement les clauses de bases sur chaque case de la grille

Le programme fait ensuite un discover sur la case donnée par l'API et récupère une liste d'info, qu'il va transformer en nouvelles clauses qu'il va ajoutée aux anciennes.

Il utilise nottament deux listes: Case_sans_animal et AnimalPossible, qui vont lui permettre d'ajouter les clauses au bon endroit et de tester les guess et discover aussi sur les bonnes cases

Pour ajouter plus de clauses, j'utilise un dictionnaire de Field qui va mettre dans le dictionnaire les cases d'indices **[i,j] : 0 si le field = sea** et **[i,j] : 1 si field = land**. Cela permet nottament d'avoir plus de précisions pour deviner les tigres et requins. De plus en fonction de la nature du field, je vais parcourir les voisins d'une case prox_count et ajouter dans une liste **terre1 les cases adjacentes terres**, dans **cpt1 toutes les cases adjacentes**, et dans **mer1 les cases adjacentes mer**. Cela permet de réduire les clauses de recherches par exemple si on cherche un tigre et qu'il y a autour 6 cases dont 1 terre, on saura directement ou est le tigre et on aura pas à faire la combinaisons pour les 6 cases  de la possibilité du tigre.
Pour chaque info récupéré dans Infos, on regarde donc si il y a un prox_count, si il n'est pas présent alors c'est une case avec un potentiel animal, si il est présent alors il n'y a pas d'animal sur cette case.

Pour chaque case où il y a un potentiel animal, je test ensuite avec gophersat les différente possibilités :
            - est ce qu'il y a un tigre?
            - est ce qu'il n'y a pas de tigre?
            - est ce qu'il y a un croco?
            - est ce qu'il n'y a pas de croco?
            - est ce qu'il y a un requin?
            - est ce qu'il n'y a pas de requin?
            
Si je trouve qu'il y a un animal dans la case [i,j] alors je guess cet animal et je récupère les infos
Si je trouve qu'il n'y a pas les 3 animaux sur la case [i,j] alors je peux discover cette case et je récupère les infos

Si après un passage sur toutes les cases potentielles d'animaux on ne sait pas conclure, alors on fait un random discover en choisissant la première case de la liste

Point faible du programme: après plusieurs découvertes / guess d'animaux le programme n'arrive pas à finir la plupart des cartes si plusieurs animaux et lignes,colonnes > 5 ,  je vais essayer d'apporter des modifications pour le repassage lundi, mais étant en entreprise en présentiel, je ne pourrais peut-être pas participer à ce nouvel essai en fonction de l'horaire.
    
