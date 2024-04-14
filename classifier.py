import pandas
import pandas as pd
from openai import OpenAI
import data
import util
from util import ExperimentType
import logwriter

N_SELF_CONSISTENCY = 5
N_CHOICE_SHUFFLING = 5

second_level_shuffled_choices = []
third_level_shuffled_choices = []


def chat_completion(title: str, brand: str, second_level_labels: list, third_level_labels: list,
                    temperature: float = 0.5, with_definition: bool = False):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": data.SYSTEM_PROMPT},
            {"role": "user", "content": data.format_user_prompt(title, brand, second_level_labels, third_level_labels,
                                                                with_definition)}
        ],
        temperature=temperature
    )
    return response


def classify_single_row(experiment_type: ExperimentType, row_index: int, result_dataset: pandas.DataFrame,
                        with_description: bool = False):
    """
    Performs single-row classification. The exact execution depends on the experiment type.

    :param experiment_type: The experiment type as specified in util.ExperimentType
    :param row_index: The index of the current row
    :param result_dataset: The resulting dataset. The results will be stored here
    :param with_description: Adds label definitions to the prompt if True, doesn't add label definitions if False
    :return:
    """
    row = result_dataset.iloc[row_index]
    product_name = row['Title']
    product_brand = row['Brand']
    result_paths = []

    if experiment_type == ExperimentType.BASELINE:
        response = chat_completion(product_name, product_brand, data.SECOND_LEVEL_LABELS, data.THIRD_LEVEL_LABELS,
                                   with_description)
        response_string = response.choices[0].message.content.strip()
        majority_path = extract_response_path(response_string)

        while majority_path == -1:
            logwriter.write_to_log(f"Response path format incorrect for response: {response}")
            response = chat_completion(product_name, product_brand, data.SECOND_LEVEL_LABELS, data.THIRD_LEVEL_LABELS,
                                       with_description)
            response_string = response.choices[0].message.content.strip()
            majority_path = extract_response_path(response_string)

        result_dataset.loc[row_index, 'Predicted Path'] = majority_path
        result_dataset.loc[row_index, 'Response'] = response_string

    elif experiment_type == ExperimentType.SELF_CONSISTENCY:
        for i in range(N_SELF_CONSISTENCY):
            if N_SELF_CONSISTENCY > 1:
                temperature = i * 1 / (N_SELF_CONSISTENCY - 1)
            else:
                temperature = 0.5

            response = chat_completion(product_name, product_brand, data.SECOND_LEVEL_LABELS, data.THIRD_LEVEL_LABELS,
                                       temperature, with_description)
            response_string = response.choices[0].message.content.strip()
            predicted_path = extract_response_path(response_string)

            while predicted_path == -1:
                logwriter.write_to_log(f"Response path format incorrect for response: {response}")
                response = chat_completion(product_name, product_brand, data.SECOND_LEVEL_LABELS,
                                           data.THIRD_LEVEL_LABELS, temperature, with_description)
                response_string = response.choices[0].message.content.strip()
                predicted_path = extract_response_path(response_string)

            logwriter.write_to_log(f"-> Round {i} completed: {predicted_path}")
            result_paths.append(predicted_path)
            result_dataset.loc[row_index, f"Path Round {i}"] = predicted_path
            result_dataset.loc[row_index, f"Response Round {i}"] = response_string

        majority_path = util.most_common_string(result_paths)
        result_dataset.loc[row_index, 'Predicted Path'] = majority_path

    elif experiment_type == ExperimentType.CHOICE_SHUFFLING:
        init_choice_shuffling()
        for i in range(N_CHOICE_SHUFFLING):
            response = chat_completion(product_name, product_brand, second_level_shuffled_choices[i],
                                       third_level_shuffled_choices[i], with_description)
            response_string = response.choices[0].message.content.strip()
            predicted_path = extract_response_path(response_string)

            while predicted_path == -1:
                logwriter.write_to_log(f"Response path format incorrect for response: {response}")
                response = chat_completion(product_name, product_brand, second_level_shuffled_choices[i],
                                           third_level_shuffled_choices[i], with_description)
                response_string = response.choices[0].message.content.strip()
                predicted_path = extract_response_path(response_string)

            logwriter.write_to_log(f"-> Round {i} completed: {predicted_path}")
            result_paths.append(predicted_path)
            result_dataset.loc[row_index, f"Path Round {i}"] = predicted_path
            result_dataset.loc[row_index, f"Response Round {i}"] = response_string

        majority_path = util.most_common_string(result_paths)
        result_dataset.loc[row_index, 'Predicted Path'] = majority_path

    elif experiment_type == ExperimentType.COMBINED:
        init_choice_shuffling()
        for i in range(N_SELF_CONSISTENCY):
            if N_SELF_CONSISTENCY > 1:
                temperature = i * 1 / (N_SELF_CONSISTENCY - 1)
            else:
                temperature = 0.5
            for j in range(N_CHOICE_SHUFFLING):
                response = chat_completion(product_name, product_brand, second_level_shuffled_choices[j],
                                           third_level_shuffled_choices[j], temperature, with_description)
                response_string = response.choices[0].message.content.strip()
                predicted_path = extract_response_path(response_string)

                while predicted_path == -1:
                    logwriter.write_to_log(f"Response path format incorrect for response: {response}")
                    response = chat_completion(product_name, product_brand, second_level_shuffled_choices[j],
                                               third_level_shuffled_choices[j], temperature, with_description)
                    response_string = response.choices[0].message.content.strip()
                    predicted_path = extract_response_path(response_string)

                logwriter.write_to_log(f"-> Round {i},{j} completed: {predicted_path}")
                result_paths.append(predicted_path)
                result_dataset.loc[row_index, f"Path Round {i},{j}"] = predicted_path
                result_dataset.loc[row_index, f"Response Round {i},{j}"] = response_string

        majority_path = util.most_common_string(result_paths)
        result_dataset.loc[row_index, 'Predicted Path'] = majority_path

    else:
        raise ValueError(f"Unknown experiment type {experiment_type}")

    logwriter.write_to_log(f"Final Response: {majority_path}\n")
    return result_dataset


def classify(experiment_type: ExperimentType, test_data: pandas.DataFrame, with_description: bool = False) \
        -> pandas.DataFrame:
    """
    Performs the classification for the whole dataset by calling classify_single_row() for each row.
    The output is saved into a csv file

    :param experiment_type: The experiment type as specified in util.ExperimentType
    :param test_data: The DataFrame containing the test data
    :param with_description: Adds label definitions to the prompt if True, doesn't add label definitions if False
    :returns: result_dataset: The DataFrame containing the classification results
    """
    logwriter.open_log()
    logwriter.write_to_log("Starting Product Classification")
    if with_description:
        description_string = "with category descriptions"
    else:
        description_string = "without category descriptions"
    logwriter.write_to_log(f"Specifications: Experiment Type: {experiment_type}, Descriptions: {description_string}")
    logwriter.write_to_log("-" * 50 + "\n")

    result_dataset = pd.DataFrame(test_data)
    try:
        for i in test_data.index:
            product_name = result_dataset.iloc[i]['Title']
            logwriter.write_to_log(f"--- {product_name} ---")
            result_dataset = classify_single_row(experiment_type, i, result_dataset, with_description)
        data.save_results_as_csv(result_dataset, experiment_type, with_description)
    except Exception as e:
        logwriter.write_to_log(f"Exception caught: {e}")
        data.save_results_as_csv(result_dataset, experiment_type, with_description)

    return result_dataset


def extract_response_path(response_string: str) -> str | int:
    """
    Extracts the predicted category path from the response message given by GPT-3.5.

    :param response_string: String value of the response message
    :return: Extracted category path, or -1 if response_string doesn't contain any valid path
    """
    parts = response_string.split('>')
    modified_parts = [part.strip() for part in parts]
    response_string = ">".join(modified_parts)

    for label_2 in data.SECOND_LEVEL_LABELS:
        for label_3 in data.THIRD_LEVEL_LABELS:
            path = f"Computers & Electronics>{label_2}>{label_3}"
            if path in response_string:
                return path
    return -1


def set_n_self_consistency(n_self_consistency: int):
    """
    Sets the number of self-consistency paths

    :param n_self_consistency: number of self-consistency paths
    """
    global N_SELF_CONSISTENCY
    N_SELF_CONSISTENCY = n_self_consistency


def set_n_choice_shuffling(n_choice_shuffling: int):
    """
    Sets the number of choice shuffling paths

    :param n_choice_shuffling: number of self-consistency paths
    """
    global N_CHOICE_SHUFFLING
    N_CHOICE_SHUFFLING = n_choice_shuffling


def init_choice_shuffling():
    """
    Initializes the arrays with permuted labels for choice shuffling
    """
    global second_level_shuffled_choices
    global third_level_shuffled_choices
    for i in range(N_CHOICE_SHUFFLING):
        second_level_shuffled_choices.append(data.permute_labels(data.SECOND_LEVEL_LABELS))
        third_level_shuffled_choices.append(data.permute_labels(data.THIRD_LEVEL_LABELS))
