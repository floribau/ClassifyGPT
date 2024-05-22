import pandas
from sklearn.metrics import f1_score
from statsmodels.stats.contingency_tables import mcnemar
from sklearn.metrics import cohen_kappa_score


def micro_f1_score(y_true: pandas.Series, y_pred: pandas.Series) -> float:
    """
    Calculates the micro f1 score for the given predictions.

    :param y_true: the correct labels
    :param y_pred: the predicted labels
    :return: micro f1 score
    """
    return f1_score(y_true, y_pred, average='micro')


def macro_f1_score(y_true: pandas.Series, y_pred: pandas.Series) -> float:
    """
    Calculates the macro f1 score for the given predictions.

    :param y_true: the correct labels
    :param y_pred: the predicted labels
    :return: macro f1 score
    """
    return f1_score(y_true, y_pred, average='macro')


def eval_f1_scores(paths_true: pandas.Series, paths_pred: pandas.Series) -> dict[str: float]:
    """
    Calculates micro and macro f1 scores for the category paths, second-level categories, and third-level categories.

    :param paths_true: the correct paths
    :param paths_pred: the predicted paths
    :return: Results for all six f1 scores. Keys: Paths Micro F1, Paths Macro F1, Second-Level Micro F1,
    Second-Level Macro F1, Third-Level Micro F1, Third-Level Macro F1
    """
    try:
        paths_micro_f1 = micro_f1_score(paths_true, paths_pred)
        paths_macro_f1 = macro_f1_score(paths_true, paths_pred)

        second_level_true = paths_true.apply(lambda x: x.split('>')[1])
        second_level_pred = paths_pred.apply(lambda x: x.split('>')[1])
        second_level_micro_f1 = micro_f1_score(second_level_true, second_level_pred)
        second_level_macro_f1 = macro_f1_score(second_level_true, second_level_pred)

        third_level_true = paths_true.apply(lambda x: x.split('>')[2])
        third_level_pred = paths_pred.apply(lambda x: x.split('>')[2])
        third_level_micro_f1 = micro_f1_score(third_level_true, third_level_pred)
        third_level_macro_f1 = macro_f1_score(third_level_true, third_level_pred)

        result_dict = {'Paths Micro F1': paths_micro_f1,
                       'Paths Macro F1': paths_macro_f1,
                       'Second-Level Micro F1': second_level_micro_f1,
                       'Second-Level Macro F1': second_level_macro_f1,
                       'Third-Level Micro F1': third_level_micro_f1,
                       'Third-Level Macro F1': third_level_macro_f1}
        return result_dict
    except IndexError as e:
        raise Exception(f"Incorrect path format: {e}")


def mcnemar_test(gold_standard: list[str], predictions1: list[str], predictions2: list[str], exact: bool = None) \
        -> float:
    """
    Performs a McNemar's test on two given list of predictions. Used to test whether there's a difference in performance between the different approaches

    :param gold_standard: the gold standard, i.e., list of correct categories (or category paths)
    :param predictions1: the first list of category (or category path) predictions
    :param predictions2: the second list of category (or category path) predictions
    :param exact: determines whether an exact binomial distribution (if True) or an approximated chi-squared distribution (if False) is used as the test statistic. If not set, the value for exact is calculated based on a threshold
    :return: the p-value calculated by the McNemar test
    """
    table = [[0, 0], [0, 0]]
    for true, pred1, pred2 in zip(gold_standard, predictions1, predictions2):
        true1 = (true == pred1)
        true2 = (true == pred2)
        if true1 and true2:
            table[0][0] += 1
        elif true1 and not true2:
            table[0][1] += 1
        elif not true1 and true2:
            table[1][0] += 1
        else:
            table[1][1] += 1
    if exact is None:
        exact = True
        if table[0][1] + table[1][0] >= 25:
            exact = False
    result = mcnemar(table, exact=exact)
    return result.pvalue


def cohen_kappa(predictions1: list[str], predictions2: list[str]) -> float:
    """
    Calculates Cohen's Kappa for two lists of classifications

    :param predictions1: the first list of category (or category path) classifications
    :param predictions2: the second list of category (or category path) predictions
    :return: float value of Cohen's Kappa
    """
    return cohen_kappa_score(predictions1, predictions2)
