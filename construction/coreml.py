import coremltools as ct
import torch

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

