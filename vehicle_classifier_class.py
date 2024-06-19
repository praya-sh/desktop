import torch
from torch import nn
from torchvision import models

import cv2
from PIL import Image
import os


class VehicleClassifier:
    def __init__(self, model_path):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        torch.manual_seed(42)
        torch.cuda.manual_seed(42)
        _, ext = os.path.splitext(model_path)
        if ext.lower() not in [".pth", ".pt"]:
            raise ValueError(
                "Invalid model file extension. Only '.pth' and '.pt' files are supported."
            )

        # Instantiate model and transform parameters
        weightsv3 = models.MobileNet_V3_Large_Weights.DEFAULT
        self.modelv3 = models.mobilenet_v3_large(weights=weightsv3).to(self.device)
        self.auto_transform = weightsv3.transforms()
        # self.class_names = ["0_no wheeler", "1_two wheeler", "2_four wheeler"]

        # Freezing the final classifier layer
        for param in self.modelv3.features.parameters():
            param.requires_grad = False
        output_shape = 3

        # Recreate the classifier layer and seed it to the target device
        self.modelv3.classifier = nn.Sequential(
            nn.Linear(
                in_features=960,
                out_features=1280,
                bias=True,
            ),
            nn.Hardswish(),
            nn.Dropout(p=0.2, inplace=True),
            nn.Linear(
                in_features=1280,
                out_features=output_shape,  # same number of output units as our number of classes
                bias=True,
            ),
        ).to(self.device)

        self.modelv3.load_state_dict(torch.load(model_path, map_location=self.device))

    def load_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = self.auto_transform(image)
        image = torch.Tensor(image)
        return image.to(self.device).unsqueeze(0)

    def predict(self, image: cv2.imread):
        self.modelv3.eval()
        image = self.load_image(image)
        with torch.inference_mode():
            output = self.modelv3(image)
            _, predicted = torch.max(output, 1)
       
        return predicted.item()

    def get_auto_transform(self):
        return self.auto_transform
