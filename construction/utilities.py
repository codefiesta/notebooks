import coremltools as ct
import csv
import json
import numpy as np
import os
import torch

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

def safe_make_dir(dir):
    # Create nested directories
    try:
        os.makedirs(dir)
        print("Directory {} created".format(dir))
    except FileExistsError:
        print("Ignoring: Directory {} already exists".format(dir))

def trace_model(model, example_input):
    """
    Tracing works by running an example input through the model and recording the operations that are executed. 
    This method is suitable for models with a fixed control flow.
    
    Example usage
    traced_model = trace_model(my_pytorch_model, torch.rand(1, 3, 224, 224))
    """
    return torch.jit.trace(model, example_input)

def script_model(model):
    """
    Scripting analyzes the Python code of the model and converts it to TorchScript. 
    This method is more flexible and can handle models with dynamic control flow.

    Example usage:
    scripted_model = script_model(my_pytorch_model)
    """
    return torch.jit.script(model)

def convert_to_coreml(torchscript_model, input_shape):
    """
    Converts a TorchScript model into the CoreML format using CoreML Tools.
    
    Example usage:
    coreml_model = convert_to_coreml(traced_model, (1, 3, 224, 224))
    coreml_model.save("my_model.mlmodel")
    """
    mlmodel = ct.convert(
        torchscript_model,
        inputs=[ct.TensorType(shape=input_shape)]
    )
    return mlmodel

