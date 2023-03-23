import torch.nn as nn
import torch
import numpy as np

classes = ['airplane',
           'apple',
           'bee',
           'car',
           'dragon',
           'mosquito',
           'moustache',
           'mouth',
           'pear',
           'piano',
           'pineapple',
           'smiley face',
           'train',
           'umbrella',
           'wine bottle']


def get_model():
    model = nn.Sequential(
        nn.Conv2d(1, 16, 3, padding='same'),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(16, 32, 3, padding='same'),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(32, 32, 3, padding='same'),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Flatten(),
        nn.Linear(288, 128),
        nn.ReLU(),
        nn.Linear(128, len(classes)),
    )

    checkpoint = torch.load('./model_lessCapacity.pth', map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint)

    model.eval()
    return model


def get_grad_cam_model():
    grad_model = GradCamModel()
    checkpoint = torch.load('./model_lessCapacity.pth', map_location=torch.device('cpu'))
    grad_model.model.load_state_dict(checkpoint)

    grad_model.model.eval()
    return grad_model


class GradCamModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding='same'),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding='same'),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 32, 3, padding='same'),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(288, 128),
            nn.ReLU(),
            nn.Linear(128, len(classes)),
        )

        self.gradients = None

    # hook for the gradients of the activations
    def activations_hook(self, grad):
        self.gradients = grad

    def forward(self, x):
        # apply all layers up to last conv layer
        x = self.model[:7](x)

        # register the hook
        h = x.register_hook(self.activations_hook)

        # apply the remaining layers
        x = self.model[7:](x)
        return x

    # method for the gradient extraction
    def get_activations_gradient(self):
        return self.gradients

    # method for the activation exctraction
    def get_activations(self, x):
        return self.model[:7](x)
