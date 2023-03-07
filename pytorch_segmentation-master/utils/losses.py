import numpy as np
import torch
import torch.nn.functional as F
import torch.nn as nn
from sklearn.utils import class_weight 
from utils.lovasz_losses import lovasz_softmax
import scipy.ndimage as nd


def make_one_hot(labels, classes):
    one_hot = torch.FloatTensor(labels.size()[0], classes, labels.size()[2], labels.size()[3]).zero_().to(labels.device)
    target = one_hot.scatter_(1, labels.data, 1)
    return target


def get_weights(target):
    t_np = target.view(-1).data.cpu().numpy()
    classes, counts = np.unique(t_np, return_counts=True)
    cls_w = np.median(counts) / counts
    weights = np.ones(7)
    weights[classes] = cls_w
    return torch.from_numpy(weights).float().cuda()


class CrossEntropyLoss2d(nn.Module):
    def __init__(self, weight=None, ignore_index=255, reduction='mean'):
        super(CrossEntropyLoss2d, self).__init__()
        self.CE = nn.CrossEntropyLoss(weight=weight, ignore_index=ignore_index, reduction=reduction)

    def forward(self, output, target):
        loss = self.CE(output, target)
        return loss
# class CrossEntropyLoss2d(nn.Module):
#     def __init__(self, ignore_label=255, thresh=0.7, min_kept=100000, factor=8):
#         super(CrossEntropyLoss2d, self).__init__()
#         self.ignore_label = ignore_label
#         self.thresh = float(thresh)
#         # self.min_kept_ratio = float(min_kept_ratio)
#         self.min_kept = int(min_kept)
#         self.factor = factor
#         self.criterion = torch.nn.CrossEntropyLoss(ignore_index=ignore_label)
#
#     def find_threshold(self, np_predict, np_target):
#         factor = self.factor
#         predict = nd.zoom(np_predict, (1.0, 1.0, 1.0/factor, 1.0/factor), order=1)
#         target = nd.zoom(np_target, (1.0, 1.0/factor, 1.0/factor), order=0)
#
#         n, c, h, w = predict.shape
#         min_kept = self.min_kept // (factor*factor)
#
#         input_label = target.ravel().astype(np.int32)
#         input_prob = np.rollaxis(predict, 1).reshape((c, -1))
#
#         valid_flag = input_label != self.ignore_label
#         valid_inds = np.where(valid_flag)[0]
#         label = input_label[valid_flag]
#         num_valid = valid_flag.sum()
#         if min_kept >= num_valid:
#             threshold = 1.0
#         elif num_valid > 0:
#             prob = input_prob[:,valid_flag]
#             pred = prob[label, np.arange(len(label), dtype=np.int32)]
#             threshold = self.thresh
#             if min_kept > 0:
#                 k_th = min(len(pred), min_kept)-1
#                 new_array = np.partition(pred, k_th)
#                 new_threshold = new_array[k_th]
#                 if new_threshold > self.thresh:
#                     threshold = new_threshold
#         return threshold
#
#
#     def generate_new_target(self, predict, target):
#         np_predict = predict.data(old).cpu().numpy()
#         np_target = target.data(old).cpu().numpy()
#         n, c, h, w = np_predict.shape
#
#         threshold = self.find_threshold(np_predict, np_target)
#
#         input_label = np_target.ravel().astype(np.int32)
#         input_prob = np.rollaxis(np_predict, 1).reshape((c, -1))
#
#         valid_flag = input_label != self.ignore_label
#         valid_inds = np.where(valid_flag)[0]
#         label = input_label[valid_flag]
#         num_valid = valid_flag.sum()
#
#         if num_valid > 0:
#             prob = input_prob[:,valid_flag]
#             pred = prob[label, np.arange(len(label), dtype=np.int32)]
#             kept_flag = pred <= threshold
#             valid_inds = valid_inds[kept_flag]
#             print('Labels: {} {}'.format(len(valid_inds), threshold))
#
#         label = input_label[valid_inds].copy()
#         input_label.fill(self.ignore_label)
#         input_label[valid_inds] = label
#         new_target = torch.from_numpy(input_label.reshape(target.size())).long().cuda(target.get_device())
#
#         return new_target
#
#     def forward(self, predict, target, weight=None):
#         assert not target.requires_grad
#         input_prob = F.softmax(predict, 1)
#         loss = self.generate_new_target(input_prob, target)
#         return loss


class DiceLoss(nn.Module):
    def __init__(self, smooth=1., ignore_index=255):
        super(DiceLoss, self).__init__()
        self.ignore_index = ignore_index
        self.smooth = smooth

    def forward(self, output, target):
        if self.ignore_index not in range(target.min(), target.max()):
            if (target == self.ignore_index).sum() > 0:
                target[target == self.ignore_index] = target.min()
        target = make_one_hot(target.unsqueeze(dim=1), classes=output.size()[1])
        output = F.softmax(output, dim=1)
        output_flat = output.contiguous().view(-1)
        target_flat = target.contiguous().view(-1)
        intersection = (output_flat * target_flat).sum()
        loss = 1 - ((2. * intersection + self.smooth) /
                    (output_flat.sum() + target_flat.sum() + self.smooth))
        return loss


class FocalLoss(nn.Module):
    def __init__(self, gamma=2, alpha=None, ignore_index=255, size_average=True):
        super(FocalLoss, self).__init__()
        self.gamma = gamma
        self.size_average = size_average
        self.CE_loss = nn.CrossEntropyLoss(reduce=False, ignore_index=ignore_index, weight=alpha)

    def forward(self, output, target):
        logpt = self.CE_loss(output, target)
        pt = torch.exp(-logpt)
        loss = ((1-pt)**self.gamma) * logpt
        if self.size_average:
            return loss.mean()
        return loss.sum()


class CE_DiceLoss(nn.Module):
    def __init__(self, smooth=1, reduction='mean', ignore_index=255, weight=None):
        super(CE_DiceLoss, self).__init__()
        self.smooth = smooth
        self.dice = DiceLoss()
        self.cross_entropy = nn.CrossEntropyLoss(weight=weight, reduction=reduction, ignore_index=ignore_index)
    
    def forward(self, output, target):
        CE_loss = self.cross_entropy(output, target)
        dice_loss = self.dice(output, target)
        return CE_loss + dice_loss


class LovaszSoftmax(nn.Module):
    def __init__(self, classes='present', per_image=False, ignore_index=255):
        super(LovaszSoftmax, self).__init__()
        self.smooth = classes
        self.per_image = per_image
        self.ignore_index = ignore_index
    
    def forward(self, output, target):
        logits = F.softmax(output, dim=1)
        loss = lovasz_softmax(logits, target, ignore=self.ignore_index)
        return loss
