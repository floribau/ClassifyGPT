import classifier
import data
import eval
from util import ExperimentType

# Classification
classifier.set_n_self_consistency(3)
classifier.set_n_choice_shuffling(3)

test_data = data.test_dataset
experiment_type = ExperimentType.SELF_CONSISTENCY
result_data = classifier.classify(experiment_type, test_data)

# Evaluation
# TODO Store eval results
print(eval.eval_f1_scores(result_data['Category Path'], result_data['Predicted Path']))
