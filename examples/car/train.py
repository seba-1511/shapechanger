#!/usr/bin/env python

import os
import csv
import torch as th
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor as T
from torch.autograd import Variable as V
from torch.optim import Adam, SGD

from torchvision.datasets.folder import default_loader
from torchvision import transforms
from torchvision import models

from random import Random


class Partition(object):

    def __init__(self, data, index):
        self.data = data
        self.index = index

    def __len__(self):
        return len(self.index)

    def __getitem__(self, index):
        data_idx = self.index[index]
        return self.data[data_idx]


class DataPartitioner(object):

    def __init__(self, data, sizes=[0.7, 0.2, 0.1], seed=1234):
        self.data = data
        self.partitions = []
        rng = Random()
        rng.seed(seed)
        data_len = len(data)
        indexes = [x for x in range(0, data_len)]
        rng.shuffle(indexes)

        for frac in sizes:
            part_len = int(frac * data_len)
            self.partitions.append(indexes[0:part_len])
            indexes = indexes[part_len:]

    def use(self, partition):
        return Partition(self.data, self.partitions[partition])


class DrivingDataset(object):

    def __init__(self, path='./driving_data/', cuda=False, transform=None):
        self.path = path
        csv_path = os.path.join(path, 'labels.csv')
        reader = csv.reader(open(csv_path, 'r'))
        data = []
        self.transform = transform
        self.cuda = cuda
        for row in reader:
            label = T([float(a) for a in row[1:]])
            img_path = os.path.join(path, row[0])
            img = default_loader(img_path)
            # if transform is not None:
                # img = transform(img)
            # t = transforms.ToPILImage()(img)
            # t.show()
            # quit()
            if cuda:
                label = label.cuda()
                # img = img.cuda()
            data.append([img, label])
        self.data = data
            
    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        # return self.data[index]
        img, label = self.data[index]
        if self.transform is not None:
            img = self.transform(img)
        if self.cuda:
            img = img.cuda()
        return img, label



class DrivingNet(nn.Module):

    def __init__(self):
        super(DrivingNet, self).__init__()
        self.bn1 = nn.BatchNorm2d(32)
        self.conv1 = nn.Conv2d(3, 32, kernel_size=5, stride=2)
        self.bn2 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=5, stride=2)
        self.bn3 = nn.BatchNorm2d(32)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=5, stride=2)
        self.bn4 = nn.BatchNorm2d(32)
        self.conv4 = nn.Conv2d(64, 64, kernel_size=3, stride=2)
        self.bn5 = nn.BatchNorm2d(32)
        self.conv5 = nn.Conv2d(64, 32, kernel_size=3, stride=2)
        self.fc1 = nn.Linear(128, 128)
        self.fc2 = nn.Linear(128, 4)

    def forward(self, x):
        x = self.conv1(x)
        x = F.elu(x)
        # x = self.bn1(x)
        x = self.conv2(x)
        x = F.elu(x)
        # x = self.bn2(x)
        x = self.conv3(x)
        x = F.elu(x)
        # x = self.bn3(x)
        # x = F.dropout(x, p=0.4, training=self.training)
        x = self.conv4(x)
        x = F.elu(x)
        # x = self.bn4(x)
        # x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv5(x)
        x = F.elu(x)
        # x = self.bn5(x)
        x = x.view(x.size(0), -1)
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.fc1(x)
        x = F.elu(x)
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x)
        # return F.softmax(x)


def accuracy(preds, targets):
    return th.sum(preds.max(1)[1] == targets.max(1)[1]).data[0]


if __name__ == '__main__':
    model = DrivingNet().cuda()
    lr = 0.0007
    # opt = Adam(model.parameters(), lr=lr)
    opt = SGD(model.parameters(), lr=lr, momentum=0.9)
    bw = transforms.Lambda(lambda x: (th.sum(x, 0) / 3).expand_as(x))
    luminosity = transforms.Lambda(lambda x: ((0.21 * x[0] + 0.72 * x[1] + 0.01 * x[2]) / 3).expand_as(x))
    data = DrivingDataset(cuda=True, transform=transforms.Compose([
            transforms.RandomSizedCrop(128),
            transforms.ToTensor(),
            luminosity,
            transforms.Normalize([0.0, 0.0, 0.0], [0.1, 0.1, 0.1]),
        ]))
    partitioner = DataPartitioner(data, [0.9, 0.1])
    train_set = partitioner.use(0)
    valid_set = partitioner.use(1)
    bsz = 4
    dataset = th.utils.data.DataLoader(train_set, batch_size=bsz, shuffle=True)
    validation = th.utils.data.DataLoader(valid_set, batch_size=bsz, shuffle=True)
    loss = nn.NLLLoss()
    loss = loss.cuda()

    print('Dataset length: ', len(dataset))
    for epoch in range(200):
        print('*'*20, 'Epoch ', epoch, '*'*20)
        epoch_error = 0.0
        epoch_acc = 0.0
        valid_error = 0.0
        valid_acc = 0.0
        model.train()
        if epoch in [30, 80]:
            lr /= 3.0
            for pg in opt.param_groups:
                pg['lr'] = lr
        for X, y in dataset:
            X, y = V(X), V(y)
            outputs = model(X)
            epoch_acc += accuracy(outputs, y)
            y = y.max(1)[1].view(-1).long()
            error = loss(outputs, y)
            epoch_error += error.data[0]
            opt.zero_grad()
            error.backward()
            opt.step()
        print('Train loss', epoch_error / len(dataset))
        print('Train accuracy', epoch_acc / (bsz * len(dataset)))
        model.eval()
        for X, y in validation:
            X, y = V(X, volatile=True), V(y, volatile=True)
            outputs = model(X)
            valid_acc += accuracy(outputs, y)
            y = y.max(1)[1].view(-1).long()
            error = loss(outputs, y)
            valid_error += error.data[0]
        print('Valid loss', valid_error / len(validation))
        print('Valid accuracy', valid_acc / (bsz * len(validation)))
        print('')


    # Save model weights
    th.save(model.cpu().state_dict(), './model.pth')
