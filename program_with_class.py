import os
import click
import parse_records
import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter


@click.command()
@click.option('--course', prompt='Course number (BIO____) : ', default='1001',
              help='Course name e.g. BIO1001, enter 1001')
@click.option('--semester', prompt='Semester: ', default='A19',
              help='Course semester (e.g.: A19')
def main(course, semester):
    """A program to generate grade file for administration from scores exported from Studium"""
    base_folder = os.path.dirname(__file__)
    file = f'BIO{course}-A-{semester}-Notes.csv'
    filename = os.path.join(base_folder, 'CSV', file)
    students = parse_records.StudentRecord.from_file(filename, course)
    print_stats(students)
    show_distribution(students, file)
    create_outout_file(students, file)


def print_stats(data):
    scores = []
    for student in data:
        scores.append(student.total)

    print("\n--------------\nStats: \n--------------")
    print("Mean :\t", np.mean(scores))
    print("Median :\t", np.median(scores))
    print("Std :\t", np.std(scores))
    print('N : \t', len(scores))
    print('Max :\t', max(scores))
    print('Min : \t', min(scores))


def show_distribution(data, file):
    bins = [0, 34, 49, 53, 56, 59, 64, 69, 72, 76, 79, 84, 89, 100.5]
    letters = ['F', 'E', 'D', 'D+', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'A+']
    scores = []

    for student in data:
        scores.append(student.total)
    distribution = np.histogram(scores, bins)[0]
    index = np.arange(len(letters))

    plt.bar(index, distribution)
    for x, y in zip(index, distribution):
        plt.text(x, y, y, ha='center', va='bottom')
    plt.title(file[:-4])
    plt.xticks(index, letters)
    plt.ylim(0, max(distribution) + 2)
    plt.ylabel("Number of students")
    plt.tight_layout()

    base_folder = os.path.dirname(__file__)
    filename = os.path.join(base_folder, 'OUTPUT', f'{file[:13]}_graph.png')

    plt.savefig(filename, bbox_inches='tight')


def create_outout_file(data, file):
    """
    An excel file containing only the following columns:
    [NAME, First Name]; [Student ID]; [Final Score (letter)].
    """

    base_folder = os.path.dirname(__file__)
    filename = os.path.join(base_folder, 'OUTPUT', f'{file[:13]}_letters.xlsx')
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    worksheet.write('A1', 'NAME, First name')
    worksheet.write('B1', 'ID')
    worksheet.write('C1', 'Letter')

    row, col = 1, 0

    for student in data:
        worksheet.write(row, col, f'{student.name.upper()}, {student.first_name.title()}')
        worksheet.write(row, col + 1, student.id)
        worksheet.write(row, col + 2, student.letter)
        row += 1

    workbook.close()


if __name__ == '__main__':
    main()
