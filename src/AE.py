# coding: utf-8
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torchvision.datasets import MNIST
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Encoder_AE(nn.Module):
  def __init__(self, z_dim, input_size, array_number):
    super().__init__()
    self.lr = nn.Linear(input_size*input_size, array_number[0])#convolution layer(input image -> 300array)
    self.lr2 = nn.Linear(array_number[0], array_number[-1])#convolution layer(300 -> 100array)
    self.lr3 = nn.Linear(array_number[-1], z_dim)#convolution layer(100 -> 2array)
    self.relu = nn.ReLU()#active function layer

  def forward(self, x):
    x = self.lr(x)#input image -> 300array
    x = self.relu(x)#ReLu
    x = self.lr2(x)#300 -> 100array
    x = self.relu(x)#ReLu
    z = self.lr3(x)#100 -> 2array

    return z

class Decoder_AE(nn.Module):
  def __init__(self, z_dim, input_size, array_number):
    super().__init__()
    self.lr = nn.Linear(z_dim, array_number[-1])#convolution layer(2 -> 100array)
    self.lr2 = nn.Linear(array_number[-1], array_number[0])#convolution layer(100 -> 300array)
    self.lr3 = nn.Linear(array_number[0], input_size*input_size)#convolution layer(300array -> Output image)
    self.relu = nn.ReLU()#actuve function

  def forward(self, z):
    x = self.lr(z)#latent variable -> 100array
    x = self.relu(x)#ReLu
    x = self.lr2(x)#100->300array
    x = self.relu(x)#ReLu
    x = self.lr3(x)#300->output image
    x = torch.sigmoid(x)   #sigmoid
    return x

class AE(nn.Module):
  def __init__(self, z_dim, input_size, array_number):
    """
    #################################################################
    Variables:
      -x_in: input image
      -x_out: output image
      -z: latent variable
    #################################################################
    """
    super().__init__()
    self.encoder = Encoder_AE(z_dim, input_size, array_number)
    self.decoder = Decoder_AE(z_dim, input_size, array_number)

  def forward(self, x_in):
    z = self.encoder(x_in)#encoder
    x_out = self.decoder(z)#decoder
    return x_out, z

# Loss function
def criterion_AE(predict, target):
  """
  #################################################################
  Variables:
    -target:
    -predict:
  #################################################################
  """
  # Cross entropy
  loss = F.binary_cross_entropy(predict, target, reduction='sum')
  return loss
