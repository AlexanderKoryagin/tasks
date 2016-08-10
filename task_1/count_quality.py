#!/usr/bin/env python

# This program will calculate quality of work of a classifier.

import os
import sys

# round float up to this number of characters after decimal point.
round_chars = 5


def usage():
    """Prints usage"""
    print ("\n{delim}\n"
           "\nThis program will calculate quality of work of a classifier.\n"
           "Usage:\n"
           "\t{file} file1 file2\n"
           "Where:\n"
           "\tfile1 - File with test samples.\n"
           "\tfile2 - File with correct answers for provided sample.\n"
           "For example:\n"
           "{file} ./data/LogisticRegression_pred.csv ./data/test_labels.csv\n"
           "{file} ./data/NaiveBayes_pred.csv ./data/test_labels.csv\n"
           "\n{delim}\n"
           ).format(delim='-' * 40, file=__file__)


def get_args():
    """Get args. Assume first arg is samples. Second- answers.
    :return: Dict with file names.
    """
    args = sys.argv[1:]
    if len(args) == 0:
        usage()
        raise ValueError('Please provide two files')
    return {'samples_file': args[0], 'answers_file': args[1]}


def parse_file(file_path):
    """Read file and return only list of number-values in it.
    :param file_path: Path to file for parsing.
    :return: List of floats.
    """
    assert os.path.isfile(file_path), (
        'File [{0}] not exists'.format(file_path))

    results = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            num = line.strip('\n')
            try:
                num = float(num)
            except Exception:
                raise ValueError('Input is not a number: %s' % num)
            results.append(num)
    return results


def round_results(num_list, round_to=0):
    """Rounds list of floats.
    :param num_list: List of floats.
    :param round_to: Number of digits after the decimal point.
    :return: Rounded list of floats.
    """
    rounded = []
    for one in num_list:
        num = round(one, round_to)
        rounded.append(num)
    return rounded


def get_results(samples, answers):
    """Returns dict with type of error and it's count.
    :param samples: List with samples
    :param answers: List with correct answers.
    :return: Dict like:
    :   {'FN': 4744.0, 'FP': 573.0, 'TN': 72267.0, 'TP': 292932.0}
    """
    tp = 0.0  # True Positive    sampl= 1 ; answ= 1
    fp = 0.0  # False Positive   sampl= 1 ; answ= 0
    fn = 0.0  # False Negative   sampl= 0 ; answ= 1
    tn = 0.0  # True Negative    sampl= 0 ; answ= 0

    for sample, answer in zip(samples, answers):
        if sample == answer:
            if answer > 0:
                tp += 1
            else:
                tn += 1
        if sample != answer:
            if answer > 0:
                fn += 1
            else:
                fp += 1

    return {'TP': tp, 'FP': fp, 'FN': fn, 'TN': tn}


def count_precision(tp, fp):
    return round((tp / (tp + fp)), round_chars)


def count_recall(tp, fn):
    return round((tp / (tp + fn)), round_chars)


def count_harmonic_mean(precision, recall):
    return round((2 * precision * recall) / (precision + recall), round_chars)


def main():

    sample_file = get_args()['samples_file']
    answer_file = get_args()['answers_file']

    samples = parse_file(sample_file)
    answers = parse_file(answer_file)

    assert len(samples) == len(answers), (
        "Number of samples is not equal to the number of answers")

    samples = round_results(samples)
    answers = round_results(answers)

    results = get_results(samples, answers)

    precision = count_precision(results['TP'], results['FP'])
    recall = count_recall(results['TP'], results['FN'])
    harmonic_mean = count_harmonic_mean(precision, recall)

    print (
        "\nResults:\n"
        "File with samples: {sample_file}\n"
        "File with answers: {answer_file}\n"
        "---\n"
        "Precision: {precision}\n"
        "Recall:    {recall}\n"
        "Harmonic mean of Precision and Recall = {hm}\n"
    ).format(sample_file=sample_file,
             answer_file=answer_file,
             precision=precision,
             recall=recall,
             hm=harmonic_mean)


if __name__ == "__main__":
    main()

# ./count_quality.py ./data/LogisticRegression_pred.csv ./data/test_labels.csv
# ./count_quality.py ./data/NaiveBayes_pred.csv ./data/test_labels.csv
