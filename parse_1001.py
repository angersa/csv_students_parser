import os
import csv
import collections
import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter


data = []

FILE = 'BIO1001-A-A19-Notes.csv'

# Choisir arrondi 0,5:
# bins = [0, 34.5, 49.5, 53.5, 56.5, 59.5, 64.5, 69.5, 72.5, 76.5, 79.5, 84.5, 89.5, 100.5]

# ou 0,1:
bins = [0, 34, 49, 53, 56, 59, 64, 69, 72, 76, 79, 84, 89, 100.5]

cotes = ['F', 'E', 'D', 'D+', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A',
         'A+']


def init():
    base_folder = os.path.dirname(__file__)
    filename = os.path.join(base_folder, 'CSV', FILE)

    data.clear()
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        fields = next(reader)
        fields = fields + ['total', 'cote']
        Record = collections.namedtuple('Etudiant', fields)

        for row in reader:
            fields = row
            fields += [get_total(row), '']
            record = Record(*fields)
            record = record._replace(cote=calcul_cote(record.total))

            data.append(record)
            

def get_total(row):
    return float(row[5]) + float(row[6]) + float(row[7]) + float(row[8]) + \
           float(row[9]) + float(row[10]) + float(row[11])


def trouve_echecs():
    echecs = []
    for etudiant in data:
        if etudiant.total < 60:
            echecs.append(etudiant)
    return echecs


def print_stats():
    notes = []
    for etudiant in data:
        notes.append(etudiant.total)

    print("\n--------------\nStats: \n--------------")
    print("Moyenne :\t", np.mean(notes))
    print("Médiane :\t", np.median(notes))
    print("Std :\t", np.std(notes))
    print('N : \t', len(notes))
    print('Max :\t', max(notes))
    print('Min : \t', min(notes))


def calcul_cote(note):
    index = np.digitize(note, bins) - 1
    return cotes[index]


def show_distribution():
    notes = []
    for etudiant in data:
        notes.append(etudiant.total)
    distribution = np.histogram(notes, bins)[0]
    index = np.arange(len(cotes))

    plt.bar(index, distribution)
    for x, y in zip(index, distribution):
        plt.text(x, y, y, ha='center', va='bottom')

    plt.title(FILE[:-4])
    plt.xticks(index, cotes)
    plt.ylim(0, max(distribution) + 2)
    plt.ylabel("Nombre d'étudiants")
    plt.tight_layout()

    base_folder = os.path.dirname(__file__)
    filename = os.path.join(base_folder, 'OUTPUT', FILE[:-4] + '.png')

    plt.savefig(filename, bbox_inches='tight')
    plt.show()


def create_outout_file():
    base_folder = os.path.dirname(__file__)
    filename = os.path.join(base_folder, 'OUTPUT', FILE[:-4] + '.xlsx')
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    worksheet.write('A1', 'Prénom, Nom')
    worksheet.write('B1', 'Matricule')
    worksheet.write('C1', 'Cote')

    row, col = 1, 0

    for etudiant in data:
        worksheet.write(row, col, f'{etudiant.Prenom}, {etudiant.Nom}')
        worksheet.write(row, col + 1, etudiant.Matricule)
        worksheet.write(row, col + 2, etudiant.cote)
        row += 1

    workbook.close()
