#!/usr/bin/env python

import os
import csv
import torch as th
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor as T
from torch.autograd import Variable as V
from torch.optim import Adam

from torchvision.datasets.folder import default_loader
from torchvision import transforms
from torchvision import models


class DrivingDataset(object):

    def __init__(self, path='./driving_data/', cuda=False, transform=None):
        self.path = path
        csv_path = os.path.join(path, 'labels.csv')
        reader = csv.reader(open(csv_path, 'r'))
        data = []
        for row in reader:
            label = T([float(a) for a in row[1:]])
            # label = T([i for i, a in enumerate(row[1:]) if a == 1.0])
            img_path = os.path.join(path, row[0])
            img = default_loader(img_path)
            if transform is not None:
                img = transform(img)
            if cuda:
                label = label.cuda()
                img = img.cuda()
            data.append([img, label])
        self.data = data
            
    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]


class DrivingNet(nn.Module):

    def __init__(self):
        super(DrivingNet, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=5, stride=2)
        self.conv2 = nn.Conv2d(32, 32, kernel_size=5, stride=2)
        self.conv3 = nn.Conv2d(32, 32, kernel_size=5, stride=2)
        self.conv4 = nn.Conv2d(32, 16, kernel_size=3, stride=1)
        self.conv5 = nn.Conv2d(16, 16, kernel_size=3, stride=1)
        self.fc1 = nn.Linear(1296, 128)
        self.fc2 = nn.Linear(128, 4)

    def forward(self, x):
        x = self.conv1(x)
        x = F.elu(x)
        x = self.conv2(x)
        x = F.elu(x)
        x = self.conv3(x)
        x = F.elu(x)
        x = self.conv4(x)
        x = F.elu(x)
        x = self.conv5(x)
        x = F.elu(x)
        x = x.view(x.size(0), -1)
        x = F.dropout(x, p=0.6, training=True)
        x = self.fc1(x)
        x = F.elu(x)
        x = F.dropout(x, p=0.7, training=True)
        x = self.fc2(x)
        return F.softmax(x)


def accuracy(preds, targets):
    return th.sum(preds.max(1)[1] == targets.max(1)[1]).data[0]


if __name__ == '__main__':
    model = DrivingNet().cuda()
    opt = Adam(model.parameters(), lr=0.001)
    data = DrivingDataset(cuda=True, transform=transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.25, 0.25, 0.25]),
        ]))
    bsz = 64
    dataset = th.utils.data.DataLoader(data, batch_size=bsz, shuffle=True)
    # loss = nn.CrossEntropyLoss()
    loss = nn.MSELoss().cuda()

    for epoch in range(200):
        print('*'*20, 'Epoch ', epoch, '*'*20)
        epoch_error = 0.0
        epoch_acc = 0.0
        for X, y in dataset:
            X, y = V(X), V(y)
            outputs = model(X)
            epoch_acc += accuracy(outputs, y)
            error = loss(outputs, y)
            epoch_error += error.data[0]
            opt.zero_grad()
            error.backward()
            opt.step()
        print('Epoch loss', epoch_error / len(data) * bsz)
        print('Epoch accuracy', epoch_acc / len(data))


    # Save model weights
    th.save(model.cpu().state_dict(), './model.pth')
