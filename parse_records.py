import csv
import numpy as np
import os


class StudentRecord:

    @classmethod
    def from_file(cls, path, course):
        if not os.path.isfile(path):
            raise FileExistsError(f'Make sure the filename follows the pattern "BIO1001-A-A19-Notes.csv" '
                                  f'and is in the CSV directory')
        if course not in ['1001', '3150']:
            raise ValueError(f'Course {course} not yet validated')
        students = []
        with open(path, 'r', encoding='utf-8') as inputfile:
            reader = csv.reader(inputfile)
            next(reader)
            if course == '1001':
                for row in reader:
                    scores = np.array(row[5:12], dtype=float)
                    student = cls(row[1], row[0], row[4], scores)
                    student.letter = cls.get_letter(student)
                    students.append(student)
            if course == '3150':
                scale = np.array([0.35, 0.35, 0.30])
                for row in reader:
                    scores = np.array(row[5:8], dtype=float)
                    student = cls(row[1], row[0], row[4], scores * scale)
                    student.letter = cls.get_letter(student)
                    students.append(student)
        return students

    def __init__(self, name, first_name, id, scores):
        self.name = name
        self.first_name = first_name
        self.id = id
        self.scores = scores
        self.total = round(np.sum(scores), 1)
        self.letter = ''

    def get_letter(student):
        bins = [0, 34, 49, 53, 56, 59, 64, 69, 72, 76, 79, 84, 89, 100.5]
        letters = ['F', 'E', 'D', 'D+', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A',
                 'A+']
        index = np.digitize(student.total, bins) - 1
        return letters[index]
