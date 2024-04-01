import classifier
import data
from util import ExperimentType

test_data = data.test_dataset
experiment_type = ExperimentType.BASELINE
classifier.classify(experiment_type, test_data)
