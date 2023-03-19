import csv
import random

random.seed(0)  # que les random soient à chaque exécution les mêmes


def read_csv(file):
    liste = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            l = []
            for elem in row:
                l.append(int(elem))
            liste.append(l)
            line_count += 1
        print("There are ", line_count, " elements in the list.")
        return liste


def run(x, permutation):
    """
    xij proviennent de la liste besoins
    t est la matrice comportant les temps de finitions de chaque objet (une ligne par objet, une colonne par machine)
    """
    t = [[0 for i in range(10)] for j in range(200)]

    for i in permutation:  # 200 rangées (200 objets)
        for j in range(10):  # 10 colonnes (10 machines)
            if (i == 0 and j == 0):
                t[i][j] = x[i][j+2]
            elif(i == 0):
                t[i][j] = t[i][j-1] + x[i][j+2]
            elif(j == 0):
                t[i][j] = t[i-1][j] + x[i][j+2]
            else:
                t[i][j] = max(t[i-1][j], t[i][j-1]) + x[i][j+2]
    return t


def weighted_tardiness(x, t):
    tardinesses = [0 for i in range(200)]
    for i in range(len(t)):
        if (t[i][9] > x[i][1]):  # verif que deadline est dépassée
            # poids * (temps de fin - deadline)
            tardinesses[i] = x[i][0]*(t[i][-1]-x[i][1])
    return sum(tardinesses)


def calculate_score(individu, permutation):
    """Calcule le score de chaque individu"""
    t = run(individu, permutation)
    weight_tard = weighted_tardiness(individu, t)
    makespan = max(max(t))
    return 1*weight_tard+1*makespan


def get_all_permutations(it):
    """ Renvoie une liste de it permutations de listes de 200 chiffres (de 0 à 199)"""
    liste = list(range(0, 200))
    ret = []
    for i in range(it):
        l = liste[:]
        random.shuffle(l)
        ret.append(l)
    return ret


def score_of_permutations(csv_matrix, all_permutations):
    """ Calcule les scores pour chaque permutation et renvoie la liste de tous les scores (l'index de chaque score est le meme que celui de sa permutation)"""
    scores = []
    for permutation in all_permutations:
        scores.append(calculate_score(csv_matrix, permutation))
    return scores


def reproduction(scores, listes_perm):
    """3eme étape"""
    childlist = []
    sorted_score = scores[:]
    sorted_score.sort()
    # index des meilleurs scores (du meilleur au pire)
    index_best_score = [scores.index(i) for i in sorted_score]
    for i in index_best_score:
        parent1 = listes_perm[i][:]  # modifier les facons de mélanger
        if i == max(index_best_score):
            parent2 = listes_perm[i][:]
        else:
            parent2 = listes_perm[i+1][:]
        child1 = parent1[:99]
        for i in parent2:
            if i in parent1[99:]:
                child1.append(i)

        child2 = parent1[99:]
        for i in parent2:
            if i in parent1[:99]:
                child2.append(i)
        childlist.append(child1)
        childlist.append(child2)
    return childlist


def main():
    population_number = 20  # nombre pair
    incomming_file = "instance.csv"
    csv_matrix = read_csv(incomming_file)
    all_permutations = get_all_permutations(population_number)
    for nb_generation in range(10): #Nombre de générations
        score_of_population = score_of_permutations(
            csv_matrix, all_permutations)
        all_permutations = reproduction(score_of_population, all_permutations)
        print("Génération "+str(nb_generation+1)+" terminée")
    print("Writing into csv file...")
    with open('results.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(all_permutations)
    print("Saved in csv file")

main()