import codecs
import os
import subprocess

from lxml import etree

SITENT_DIR = '/home/martijn/Documents/JavaProjects/sitent/pretrained_system'
CRF_DIR = '/home/martijn/Documents/CppProjects/CRF++-0.58/'


def create_sitent_input(annotation):
    """
    Creates the input files for sitent
    :param annotation: the current Annotation
    """
    in_file = os.path.join(SITENT_DIR, 'sample_data', 'raw_text', '{}.txt'.format(annotation.pk))
    with codecs.open(in_file, 'wb', 'utf-8') as f:
        f.write(annotation.sentence)
        f.write('\n')


def call_sitent():
    """
    Calls sitent
    """
    command = './run_sitent_system.sh {} {}'.format(CRF_DIR, 'sample_data')
    subprocess.call(command, shell=True, cwd=SITENT_DIR)


def get_sitent_output(annotation):
    """
    Retrieves the output from sitent
    :param annotation: the current Annotation
    :return: the output file from sitent
    """
    output_file = os.path.join(SITENT_DIR, 'sample_data', 'labeled_text', '{}.xml'.format(annotation.pk))

    if not os.path.exists(output_file):
        raise ValueError('Output file for {} not found'.format(annotation.pk))

    return output_file


def read_sitent(annotation):
    """
    Finds the correct output for the current Annotation
    :param annotation: the current Annotation
    :return: a dict with the output from sitent
    """
    # Parse the output file
    tree = etree.parse(get_sitent_output(annotation))

    # Use the main verb text and the start index to find the annotation belonging to this Annotation
    xpath = './/mainVerb[text()="{}" and @begin="{}"]'
    results = []
    for n, word in enumerate(annotation.words):
        results.extend(tree.xpath(xpath.format(word, annotation.indices[n])))

    if len(results) == 0:
        print 'No annotations found for {}'.format(annotation.pk)
        return dict()
    elif len(results) > 1:
        print 'Multiple annotations found for {}'.format(annotation.pk)

    # Return the annotation tag of the last result (in case of multiple annotations, this is often the head verb)
    return results[-1].getparent().find('annotation')
