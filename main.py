import classifier
import data
import eval
from util import ExperimentType

# Classification
classifier.set_n_self_consistency(5)
classifier.set_n_choice_shuffling(5)

test_data = data.test_dataset
experiment_type = ExperimentType.BASELINE
result_data = classifier.classify(experiment_type, test_data)

# Evaluation
# TODO Store eval results
print(eval.eval_f1_scores(result_data['Category Path'], result_data['Category Path']))
