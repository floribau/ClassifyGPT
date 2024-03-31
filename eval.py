from sklearn.metrics import f1_score


def micro_f1_score(y_true, y_pred):
    """
    Calculates the micro f1 score for the given predictions.

    :param y_true: Pandas Series: the correct labels
    :param y_pred: Pandas Series: the predicted labels
    :return: Float: micro f1 score
    """
    return f1_score(y_true, y_pred, average='micro')


def macro_f1_score(y_true, y_pred):
    """
    Calculates the macro f1 score for the given predictions.

    :param y_true: Pandas Series: the correct labels
    :param y_pred: Pandas Series: the predicted labels
    :return: Float: macro f1 score
    """
    return f1_score(y_true, y_pred, average='macro')


def eval_f1_scores(paths_true, paths_pred):
    """
    Calculates micro and macro f1 scores for the category paths, second-level categories, and third-level categories.

    :param paths_true: Pandas Series: the correct paths
    :param paths_pred: Pandas Series: the predicted paths
    :return: dict with all six f1 scores. Keys: Paths Micro F1, Paths Macro F1, Second-Level Micro F1,
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
