import classifier
import data
import util

test_data = data.test_dataset
experiment_type = util.ExperimentType.BASELINE
classifier.classify(experiment_type, test_data)
