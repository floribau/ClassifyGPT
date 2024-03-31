from sklearn.metrics import f1_score


def micro_f1_score(y_true, y_pred):
    return f1_score(y_true, y_pred, average='micro')


def macro_f1_score(y_true, y_pred):
    return f1_score(y_true, y_pred, average='macro')


def eval_f1_scores(paths_true, paths_pred):
    paths_micro_f1 = micro_f1_score(paths_true, paths_pred)
    paths_macro_f1 = macro_f1_score(paths_true, paths_pred)

    try:
        second_level_true = paths_true.apply(lambda x: x.split('>')[1])
        second_level_pred = paths_pred.apply(lambda x: x.split('>')[1])
        second_level_micro_f1 = micro_f1_score(second_level_true, second_level_pred)
        second_level_macro_f1 = macro_f1_score(second_level_true, second_level_pred)

        third_level_true = paths_true.apply(lambda x: x.split('>')[2])
        third_level_pred = paths_pred.apply(lambda x: x.split('>')[2])
        third_level_micro_f1 = micro_f1_score(third_level_true, third_level_pred)
        third_level_macro_f1 = macro_f1_score(third_level_true, third_level_pred)

        return paths_micro_f1, paths_macro_f1, second_level_micro_f1, second_level_macro_f1, third_level_micro_f1, third_level_macro_f1
    except IndexError as e:
        raise Exception("Incorrect path format")
