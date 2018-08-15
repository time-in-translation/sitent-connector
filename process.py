import argparse
import codecs
import csv

from models import Annotation
from sitent import create_sitent_input, call_sitent, read_sitent
from utils import unicode_csv_reader


def import_csv(filename):
    result = []

    with codecs.open(filename, 'rb', 'utf-8') as f:
        word_columns = []
        index_columns = []
        sentence_column = 0

        reader = unicode_csv_reader(f, delimiter=';')
        for i, row in enumerate(reader):
            if i == 0:  # header row
                for j, r in enumerate(row):
                    if r.startswith('w'):
                        word_columns.append(j)
                    if r.startswith('index'):
                        index_columns.append(j)
                    if r.startswith('full'):
                        sentence_column = j
            else:  # other rows
                pk = int(row[0])
                words = [row[c] for c in word_columns]
                indices = [row[c] for c in index_columns]
                sentence = row[sentence_column]
                result.append(Annotation(pk, words, indices, sentence))

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieve annotation from sitent')
    parser.add_argument('file_in', type=str, help='Input file')
    parser.add_argument('file_out', type=str, help='Output file')
    args = parser.parse_args()

    annotations = import_csv(args.file_in)

    for annotation in annotations:
        create_sitent_input(annotation)

    # call_sitent()

    results = []
    for annotation in annotations:
        result_an = read_sitent(annotation)

        se_type = result_an.get('seType')
        genericity = result_an.get('mainReferentGenericity')
        habituality = result_an.get('habituality')
        asp_class = result_an.get('mainVerbAspectualClass')
        results.append([annotation.pk, ' '.join(annotation.words), se_type, genericity, habituality, asp_class])

    with codecs.open(args.file_out, 'wb', 'utf-8') as f:
        csv_writer = csv.writer(f, delimiter='\t')
        csv_writer.writerow(['id', 'words', 'se_type', 'genericity', 'habituality', 'asp_class'])
        csv_writer.writerows(results)
