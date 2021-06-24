from typing import List, Tuple
from itertools import combinations


def cell_to_var(i: int, j: int, n: int, val: int) -> int:
    return (i*(n*5)) + j*5 + val

def var_to_cell(n: int, m: int, nb: int) -> Tuple[int, int, int]:
    return ( (nb //(n*5)), (nb // 5)% n, (nb %(n*m) % 5))


def at_least_one(vars: List[int]) -> List[int]:
    return vars


def unique(vars: List[int]) -> List[List[int]]:
    clauses = []
    clauses.append(at_least_one(vars))
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
def create_cell_constraints(n: int, m: int) -> List[List[int]]:
    clauses = []
    for i in range(m):
        for j in range(n):
            var = []
            var2 = []
            var3 = []
            var4 = []
            for k in range(1, 4):
                var.append(cell_to_var(i, j, m, k))
            clauses += unique(var)
            for k in range(4, 6):
                var2.append(cell_to_var(i, j, m, k))
            clauses += unique(var2)
            var3.append(cell_to_var(i, j, m, 1))
            var3.append(cell_to_var(i, j, m, 4))
            clauses += landanimal(var3)
            var4.append(cell_to_var(i, j, m, 3))
            var4.append(cell_to_var(i, j, m, 5))
            clauses += landanimal(var4)
    return clauses


*** # Fonction qui crée des clauses en fct des variables globales??? ne pas faire 
def create_value_constraints(grid: List[List[int]]) -> List[List[int]]:
    clauses = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != 0:
                clauses.append([cell_to_variable(i, j, grid[i][j])])
    return clauses
***

#Fonction qui crée les clauses de départ de notre grille
def generate_problem(grid: List[List[int]]) -> List[List[int]]:
    clauses = []
    clauses += create_cell_constraints()
    return clauses

#Fonction qui met sous format dimacs les clauses créées
def clauses_to_dimacs(clauses: List[List[int]], nb_vars: int) -> str:
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
def Infos_to_clauses (Infos : List[info], m: int, n: int, clauses :List[List[int]], Case_sans_animal: List[int,int] ) -> List[List[int]] :
    for i in Infos:
        pos=i["pos"]
        ligne=pos[0]
        colonne=pos[1]
        field=i["field"]
        if (field == "sea"):
            f=4
        else
            f=5
        DictField=dict[Tuple[int,int],int]
        dict = {}
        for c in range(m):
            for d in range(n):
                if(ligne=c and colonne=d):
                    dict[(c,d)]= (f-4)
        
        clauses.append([cell_to_var(ligne,colonne,n,f)]) # ajoute toutes les clauses sur le type de field de toutes les cases pour lesquelles on a des infos
        if prox_count in Infos[i]:
            Case_sans_animal.append([ligne,colonne])
            prox_count=i["prox_count"]
            if(prox_count==[0,0,0]):
                for(k in range (1,4)):
                    var= cell_to_var(ligne,colonne,n,k)
                    clauses.append([-var])
            else:
                animal=1 # parcours des 3 animaux en commençant par le tigre, puis crocodile, puis requin
                for j in prox_count :
                    if (j==0):
                        clauses.append([-cell_to_var(ligne-1,colonne-1,n,f)])
                        clauses.append([-cell_to_var(ligne-1,colonne,n,f)])
                        clauses.append([-cell_to_var(ligne-1,colonne+1,n,f)])
                        clauses.append([-cell_to_var(ligne,colonne-1,n,f)])
                        clauses.append([-cell_to_var(ligne,colonne+1,n,f)])
                        clauses.append([-cell_to_var(ligne+1,colonne-1,n,f)])
                        clauses.append([-cell_to_var(ligne+1,colonne,n,f)])
                        clauses.append([-cell_to_var(ligne+1,colonne+1,n,f)])
                    if(j!=0):
                        terre=0
                        mer=0
                        cpt=0
                        for a in range(ligne-1,ligne+1):
                            for b in range(colonne-1,colonne+1):
                                if([a,b] not in Case_sans_animal):
                                    cpt++
                                    if(dict[a,b]==1):
                                        terre++
                                    else:
                                        mer++
                                        
                                if (animal == 1):
                                    for a, b in combinations(
                                        terre, j
                                    ):
                                        c = []
                                        c = [-a, -b]
                                        clauses.append(c)

                                                                        
                                if (animal == 2):
                                    for a, b in combinations(
                                        cpt, j
                                    ):
                                        c = []
                                        c = [-a, -b]
                                        clauses.append(c)


                                if (animal == 3):
                                    for a, b in combinations(
                                        mer, j
                                    ):
                                        c = []
                                        c = [-a, -b]
                                        clauses.append(c)
                                        
                    animal+=1
                                    
                                    
                                    
                        
                        

           
            
        

#fonction qui test des cases avec gophersat ( rajouté inverse de ce qu'on pense, si c est unsat, alors ce qu'on pense est vrai )
#regarder case, regarder variable, et tester
def gophersat_test(clauses: List[List[int]], i : int, j : int, n : int,  val : int  ) ->Tuple[bool, List[int]]:
    clauses.append(-cell_to_var(i,j,val)
   
    
def main()

server = "http://localhost:8000/"
    group = "Groupe 66"
    members = "Clément DOUALE"
    croco = CrocomineClient(server, group, members)

(Status, Msg, Infos) = croco.new_grid()
m=Infos["m"]
n=Infos["n"]
start=Infos["start"]
Case_sans_animal=[[start[0],start[1]]
(Status, Msg, Infos) = croco.discover(start[0],start[1])
