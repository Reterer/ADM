%%writefile going_modular/model_builder.py
"""
Contains PyTorch model code to instantiate a TinyVGG model.
"""
import torch
from torch import nn 

class NN(nn.Module):
  """Creates some NN model
  Args:
    input_shape: An integer indicating number of input channels.
    hidden_units: An integer indicating number of hidden units between layers.
    output_shape: An integer indicating number of output units.
  """
    def __init__(self, input_shape: int, hidden_units: int, output_shape: int) -> None:
        pass

    def forward(self, x: torch.Tensor):
        pass