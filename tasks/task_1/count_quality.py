#!/usr/bin/env python

# This program will calculate quality of work of a classifier.

import os
import sys

import numpy as np
from sklearn.metrics import roc_auc_score

# round float up to this number of characters after decimal point.
round_chars = 5


def usage():
    """Prints usage"""
    print (
        "\n{delim}\n"
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


def convert_to_bin(num_list, threshold=0.6):
    """Rounds list of floats.
    :param num_list: List of floats.
    :param threshold: Threshold to count float is 1 or 0.
    :return: List of floats.
    """
    rounded = []
    for one in num_list:
        if one > threshold:
            rounded.append(1.0)
        else:
            rounded.append(0.0)
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


def count_fpr(fp, tn):
    """Counts 'False Positive Rate'.
    :param fp: num of False Positive.
    :param tn: num of True Negative.
    :return: num
    """
    return round((fp / (fp + tn)), round_chars)


def count_tpr(tp, fn):
    """Counts 'True Positive Rate'.
    :param tp: num of True Positive.
    :param fn: num of False Negative.
    :return: Num
    """
    return round((tp / (tp + fn)), round_chars)


def get_answers_and_samples():
    """Read and return floats from files.
    :return: Two list of floats: samples, answers
    """
    sample_file = get_args()['samples_file']
    answer_file = get_args()['answers_file']

    samples = parse_file(sample_file)
    answers = parse_file(answer_file)

    assert len(samples) == len(answers), (
        "Number of samples is not equal to the number of answers")

    return samples, answers


def convert_with_best_threshold():
    """Get best threshold based on roc_auc_score. And convert to samples to bin
    using it.
    :return: float, list, list
    """
    thresholds = np.arange(0.01, 1.00, 0.01)

    samples, answers = get_answers_and_samples()
    answers = convert_to_bin(answers)

    print 'Calculating best threshold . . .'
    threshold_score = {}
    for threshold in thresholds:
        score = roc_auc_score(
            answers,
            convert_to_bin(samples, threshold=threshold))
        score = round(score, round_chars)
        threshold_score[score] = round(threshold, 2)

    values = threshold_score.keys()
    best_value = max(values)
    best_threshold = threshold_score[best_value]
    print 'Calculating best threshold . . . it is "{0}"'.format(best_threshold)

    samples = convert_to_bin(samples, threshold=best_threshold)

    return best_threshold, answers, samples


def main():
    sample_file = get_args()['samples_file']
    answer_file = get_args()['answers_file']

    best_threshold, answers, samples = convert_with_best_threshold()

    results = get_results(samples, answers)

    precision = count_precision(tp=results['TP'], fp=results['FP'])
    recall = count_recall(tp=results['TP'], fn=results['FN'])
    harmonic_mean = count_harmonic_mean(precision, recall)

    tpr = count_tpr(tp=results['TP'], fn=results['FN'])
    fpr = count_fpr(fp=results['FP'], tn=results['TN'])

    print (
        "\nResults:\n"
        "File with samples: {sample_file}\n"
        "File with answers: {answer_file}\n\n"
        "Precision: {precision}\n"
        "Recall:    {recall}\n"
        "Harmonic mean of Precision and Recall = {hm}\n\n"
        "Threshold: {threshold}\n"
        "True Positive Rate: {tpr}\n"
        "False Positive Rate: {fpr}\n"
    ).format(sample_file=sample_file,
             answer_file=answer_file,
             precision=precision,
             recall=recall,
             hm=harmonic_mean,
             threshold=best_threshold,
             fpr=fpr,
             tpr=tpr)


if __name__ == "__main__":
    main()

# ./count_quality.py ./data/LogisticRegression_pred.csv ./data/test_labels.csv
# ./count_quality.py ./data/NaiveBayes_pred.csv ./data/test_labels.csv
