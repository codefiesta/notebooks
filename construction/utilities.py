import csv
import json
import numpy as np

def csv_to_list(filename):
    """
    Reads a csv file into a list.

    Args:
        filename (str): The name of the CSV file to read.
    """
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data

def jsonl_to_list(file_path):
    """
    Reads a jsonl file into a list.

    Args:
        filename (str): The name of the jsonl file to read.
    """
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                json_object = json.loads(line)
                data.append(json_object)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line: {line.strip()} - {e}")
    return data
    
def write_jsonl(data, filename):
    """
    Writes a list of dictionaries to a JSONL file.

    Args:
        data: A list of dictionaries to be written to the file.
        filename: The name of the file to write to.
    """
    with open(filename, 'w') as f:
        for item in data:
            json.dump(item, f)
            f.write('\n')

def split_train_val_test(data, ratio=[0.8, 0.1, 0.1]):
    """
    Splits the list into training, validation, and testing lists.

    Args:
        data: A list of data
        ratio: The ratios to split by
    """
    train_r, val_r, test_r = ratio
    assert(np.sum(ratio) == 1.0)  # makes sure the splits make sense
    # note we only need to give the first 2 indices to split, the last one it returns the rest of the list or empty
    indicies_for_splitting = [int(len(data) * train_r), int(len(data) * (train_r+val_r))]
    train, val, test = np.split(data, indicies_for_splitting)
    return list(train), list(val), list(test)
