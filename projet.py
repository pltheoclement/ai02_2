from typing import List, Tuple
from itertools import combinations,product
from crocomine_client1 import CrocomineClient
import requests
import subprocess
import random
from pprint import pprint
info=dict

def cell_to_var(i: int, j: int, n: int, val: int) -> int:
    return (i*(n*5)) + j*5 + val

def var_to_cell(n: int, m: int, nb: int) -> Tuple[int, int, int]:
    return ( (nb //(n*5)), (nb // 5)% n, (nb %(n*m) % 5))


def at_least_one(vars: List[int]) -> List[int]:
    return vars


def unique(vars: List[int]) -> List[List[int]]:
    clauses = []
    for a, b in combinations(
        vars, 2
    ):  # L'appel à combinations empêche directement la redondance, puisque la fonction ne retourne jamais 2 tuples équivalents (si on a (1,2), on n'aura pas (2,1)).
        c = []
        c = [-a, -b]
        clauses.append(c)
    return clauses

#fonction créant les clauses suivantes pour chaque case : impossibilité d'avoir un tigre sur de l'eau et un requin sur de la terre
def landanimal(vars: List[int]) -> List[List[int]]:
    clauses = []
    for a, b in combinations(
        vars, 2
    ):
        c = []
        c = [-a, -b]
        clauses.append(c)
    return clauses


#fonction créant les clauses de départ pour chaque case de la grille
def create_clauses_depart(m: int, n: int) -> List[List[int]]:
    clauses = []
    for i in range(m):
        for j in range(n):
            var = []
            var2 = []
            var3 = []
            var4 = []
            for k in range(1, 4):
                var.append(cell_to_var(i, j, n, k))
            clauses += unique(var)
            for k in range(4, 6):
                var2.append(cell_to_var(i, j, n, k))
            clauses.append(at_least_one(var2))
            clauses += unique(var2)
            var3.append(cell_to_var(i, j, n, 1))
            var3.append(cell_to_var(i, j, n, 4))
            clauses += landanimal(var3)
            var4.append(cell_to_var(i, j, n, 2))
            var4.append(cell_to_var(i, j, n, 5))
            clauses += landanimal(var4)
    return clauses



#Fonction qui met sous format dimacs les clauses créées
def clauses_to_dimacs(clauses: List[List[int]], m: int, n: int) -> str:
    s = f"p cnf {5*m*n} {len(clauses)}\n"
    for i in range(len(clauses)):
        for j in range(len(clauses[i])):
            s += f"{clauses[i][j]} "
        s += "0\n"
    return s


def write_dimacs_file(dimacs: str, filename: str):
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)


def exec_gophersat(
    filename: str, cmd: str = "./gophersat", encoding: str = "utf8"
) -> Tuple[bool, List[int]]:
    result = subprocess.run(
        [cmd, filename], capture_output=True, check=True, encoding=encoding
    )
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return False, []

    model = lines[2][2:].split(" ")

    return True, [int(x) for x in model]

#fonction pour convertir infos récupérées en clauses
def Infos_to_clauses (Infos , m: int, n: int, clauses :List[List[int]], Case_sans_animal: List[List[int]] ) -> List[List[int]] :
    DictField=dict[Tuple[int,int],int]
    DictField = {}
    for i in Infos:
        pos=i["pos"]
        ligne=pos[0]
        colonne=pos[1]
        field=i["field"]
        if (field == "sea"):
            f=4
        else:
            f=5
        clauses.append([cell_to_var(ligne,colonne,n,f)]) # ajoute toutes les clauses sur le type de field de toutes les cases pour lesquelles on a des infos
        DictField[(ligne,colonne)]= (f-4)
        if "prox_count" in i:
            Case_sans_animal.append([ligne,colonne])
            prox_count=i["prox_count"]
        
                
    for i in Infos:
        pos=i["pos"]
        ligne=pos[0]
        colonne=pos[1]
        field=i["field"]
        if (field == "sea"):
            f=4
        else:
            f=5
        if "prox_count" in i:
            prox_count=i["prox_count"]
            if(prox_count==[0,0,0]):
                for k in range (1,4):
                    var= cell_to_var(ligne,colonne,n,k)
                    clauses.append([-var])
                    
            else:
                animal=0 # parcours des 3 animaux en commençant par le tigre, puis crocodile, puis requin
                for nb in prox_count :
                    animal+=1
                    terre1=[]
                    mer1=[]
                    cpt1=[]
                    for i in [ligne-1,ligne,ligne+1]:
                        for j in [colonne-1,colonne,colonne+1]:
                            if([i,j] not in Case_sans_animal and i>=0 and j>=0 and i<m and j<n):
                                if(DictField[i,j]==1):
                                    terre1.append([i,j])
                                    cpt1.append([i,j])
                                else:
                                    mer1.append([i,j])
                                    cpt1.append([i,j])
                                    
                    if (nb==0):
                        for i in [ligne-1,ligne,ligne+1]:
                            for j in [colonne-1,colonne,colonne+1]:
                                if( i>=0 and j>=0 and i<m and j<n):
                                    clauses.append([-cell_to_var(i,j,n,animal)])
                    
                    if(nb!=0):
                        if (animal == 1):
                            c = []
                            var=[]
                            for u in combinations(
                                terre1, nb
                            ):
                                c.append(u)
                            if(len(c)<5):
                                for j in product(*c):
                                    for h in range (len(j)):
                                        output = set(tuple(sorted(x)) for x in j) 
                                        var.append(cell_to_var(j[h][0],j[h][1],n,1))
                                    clauses.append(var)
                                    var=[]
                            c=[]
                            for v in combinations(
                                terre1, (len(terre1)-nb)
                            ):
                                c.append(v)
                            if(len(c)<5):
                                for j in product(*c):
                                    for h in range(len(j)):
                                        output = set(tuple(sorted(x)) for x in j) 
                                        var.append(-cell_to_var(j[h][0],j[h][1],n,1))
                                    clauses.append(var)
                                    var=[]
                            
                        if (animal == 2):
                            c = []
                            var=[]
                            for u in combinations(
                                mer1, nb
                            ):
                                c.append(u)
                            if(len(c)<5):
                                for j in product(*c):
                                    for h in range(len(j)):
                                        output = set(tuple(sorted(x)) for x in j) 
                                        var.append(cell_to_var(j[h][0],j[h][1],n,2))
                                    clauses.append(var)
                                    var=[]
                            c=[]
                            for v in combinations(
                                mer1, (len(mer1)-nb)
                            ):
                                c.append(v)
                            if(len(c)<5):
                                for j in product(*c):
                                    for h in range(len(j)):
                                        output = set(tuple(sorted(x)) for x in j) 
                                        var.append(-cell_to_var(j[h][0],j[h][1],n,2))
                                    clauses.append(var)
                                    var=[]
        

                        if (animal == 3):
                            c = []
                            var=[]
                            for u in combinations(
                                cpt1, nb
                            ):
                                c.append(u)
                            if(len(c)<5):
                                for j in product(*c):
                                    for h in range(len(j)):
                                        output = set(tuple(sorted(x)) for x in j) 
                                        var.append(cell_to_var(j[h][0],j[h][1],n,3))
                                    clauses.append(var)
                                    var=[]
                            c=[]                       
                            for v in combinations(
                                cpt1, (len(cpt1)-nb)
                            ):
                                c.append(v)
                            if(len(c)<5):
                                for j in product(*c):
                                    for h in range(len(j)):
                                        output = set(tuple(sorted(x)) for x in j) 
                                        var.append(-cell_to_var(j[h][0],j[h][1],n,3))
                                    clauses.append(var)
                                    var=[]
                                        
                

    return clauses
                                    
                                    
                                    
                        

#fonction qui test des cases avec gophersat ( rajouté inverse de ce qu'on pense, si c est unsat, alors ce qu'on pense est vrai )
#regarder case, regarder variable, et tester
def test_tigre(clauses: List[List[int]], i : int, j : int, n : int, m: int ) ->Tuple[bool, List[int]]:
    clauses.append([-cell_to_var(i,j,n,1)])
    write_dimacs_file(clauses_to_dimacs(clauses,n,m),"test.cnf")
    result = exec_gophersat("test.cnf")
    clauses.pop()
    if not result[0]:
        return 1
    else:
        return 0

def test_not_tigre(clauses: List[List[int]], i : int, j : int, n : int, m: int ) ->Tuple[bool, List[int]]:
    clauses.append([cell_to_var(i,j,n,1)])
    write_dimacs_file(clauses_to_dimacs(clauses,n,m),"test.cnf")
    result = exec_gophersat("test.cnf")
    clauses.pop()
    if not result[0]:
        return 1
    else:
        return 0

def test_croco(clauses: List[List[int]], i : int, j : int, n : int , m: int ) ->Tuple[bool, List[int]]:
    clauses.append([-cell_to_var(i,j,n,3)])
    write_dimacs_file(clauses_to_dimacs(clauses,n,m),"test.cnf")
    result = exec_gophersat("test.cnf")
    clauses.pop()
    if not result[0]:
        return 1
    else:
        return 0

def test_not_croco(clauses: List[List[int]], i : int, j : int, n : int , m: int ) ->Tuple[bool, List[int]]:
    clauses.append([cell_to_var(i,j,n,3)])
    write_dimacs_file(clauses_to_dimacs(clauses,n,m),"test.cnf")
    result = exec_gophersat("test.cnf")
    clauses.pop()
    if not result[0]:
        return 1
    else:
        return 0
        

def test_requin(clauses: List[List[int]], i : int, j : int, n : int ,m : int ) ->Tuple[bool, List[int]]:
    clauses.append([-cell_to_var(i,j,n,2)])
    write_dimacs_file(clauses_to_dimacs(clauses,n,m),"test.cnf")
    result = exec_gophersat("test.cnf")
    clauses.pop()
    if not result[0]:
        return 1
    else:
        return 0

def test_not_requin(clauses: List[List[int]], i : int, j : int, n : int ,m : int ) ->Tuple[bool, List[int]]:
    clauses.append([cell_to_var(i,j,n,2)])
    write_dimacs_file(clauses_to_dimacs(clauses,n,m),"test.cnf")
    result = exec_gophersat("test.cnf")
    clauses.pop()
    if not result[0]:
        return 1
    else:
        return 0

def test_case(clauses: List[List[int]], i : int, j : int, n : int, m: int, croco, Case_sans_animal)-> Tuple[int, List[info], str]:
    pasanimal=0
    if (test_tigre(clauses,i,j,n,m)==1):
        (Status, Msg, Infos) = croco.guess(i,j,"T")
        return (1, Infos, Status)


    if (test_not_tigre(clauses,i,j,n,m)==1):
        pasanimal+=1
        
    if (test_croco(clauses,i,j,n,m)==1):
        (Status, Msg, Infos) = croco.guess(i,j,"C")
        return (1, Infos, Status)

    if (test_not_croco(clauses,i,j,n,m)==1):
        pasanimal+=1
        
    if (test_requin(clauses,i,j,n,m)==1):
        (Status, Msg, Infos) = croco.guess(i,j,"S")
        return (1, Infos, Status)

    if (test_not_requin(clauses,i,j,n,m)==1):
        pasanimal+=1
        
    if (pasanimal==3):
        if([i,j] not in Case_sans_animal):
            (Status, Msg, Infos) = croco.discover(i,j)
            for i in Infos:
                if "prox_count" in i :
                    pos=i["pos"]
                    ligne=pos[0]
                    colonne=pos[1]
                    Case_sans_animal.append([ligne,colonne])
                    clauses.append([-cell_to_var(ligne,colonne,n,1)])
                    clauses.append([-cell_to_var(ligne,colonne,n,2)])
                    clauses.append([-cell_to_var(ligne,colonne,n,3)])
            return (1, Infos, Status)

    return (0,[],"")
        
    
def main():
    server = "http://localhost:8000"  #"http://croco.lagrue.ninja:80"
    #password = "ce que je veux"
    group = "Groupe 66"
    members = "Clément DOUALE"
    croco = CrocomineClient(server, group, members)
    grille_presente = "oui"
    while( grille_presente == "oui" ):
        Status, Msg, Infos = croco.new_grid()
        if(Status == "Err"):
            grille_presente= "non"
        m=Infos["m"]
        n=Infos["n"]
        start=Infos["start"]
        Case_sans_animal=[]
        clauses = create_clauses_depart(m,n)
        (Status, Msg, Infos) = croco.discover(start[0],start[1])
        Infosback=Infos

        while Status =="OK":
            AnimalPossible=[]
            Infos_to_clauses(Infosback,m,n,clauses,Case_sans_animal)
            for i in Infosback:
                if "prox_count" not in i:
                    if "animal" not in i:
                        pos=i["pos"]
                        ligne=pos[0]
                        colonne=pos[1]
                        AnimalPossible.append([ligne,colonne])
                if "animal" in i or "prox_count" in i:
                    pos=i["pos"]
                    ligne=pos[0]
                    colonne=pos[1]
                    if([ligne,colonne] in AnimalPossible):
                        AnimalPossible.remove([ligne,colonne])    
            tests=0
            for i in range (len(AnimalPossible)):
                TestCase=test_case(clauses,AnimalPossible[i][0],AnimalPossible[i][1],n,m, croco, Case_sans_animal)
                Infosback+=TestCase[1]
                if(TestCase[2]!=""):
                    Status=TestCase[2]    
                if(TestCase[0]==0):
                    tests+=1
            if( tests >= len(AnimalPossible)):
                print("random",AnimalPossible[0][0],AnimalPossible[0][1])
                (Status, Msg, Infos)= croco.discover(AnimalPossible[0][0],AnimalPossible[0][1])
                Infosback+=Infos


                

        
        
            
                
                

            
            
                

        
        


if __name__ == "__main__":
    main()
    
    

                  
                  
