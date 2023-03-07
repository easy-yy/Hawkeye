import os
import json
import argparse
import torch
import dataloaders
import models
from utils import losses
from utils import Logger
from trainer import Trainer


def get_instance(module, name, config, *args):
    # GET THE CORRESPONDING CLASS / FCT
    return getattr(module, config[name]['type'])(*args, **config[name]['args'])


def main(resume):
    config = json.load(open('saved/PSPNet/config.json'))
    train_logger = Logger()

    # DATA LOADERS
    train_loader = get_instance(dataloaders, 'train_loader', config)
    val_loader = get_instance(dataloaders, 'val_loader', config)

    # MODEL
    model = get_instance(models, 'arch', config, train_loader.dataset.num_classes)
    print(f'\n{model}\n')

    # LOSS
    loss = getattr(losses, config['loss'])(ignore_index=config['ignore_index'])

    # TRAINING
    trainer = Trainer(
        model=model,
        loss=loss,
        resume=resume,
        config=config,
        train_loader=train_loader,
        val_loader=val_loader,
        train_logger=train_logger)

    trainer.train()


if __name__ == '__main__':
    # PARSE THE ARGS
    parser = argparse.ArgumentParser(description='PyTorch Training')
    parser.add_argument('-c', '--config', default='saved/DeepLab/04-16_19-42/config.json', type=str,
                        help='Path to the config file (default: config.json)')
    parser.add_argument('-r', '--resume', default='saved/DeepLab/04-16_19-42/best_model.pth', type=str,
                        help='Path to the .pth model checkpoint to resume training')
    # parser.add_argument('-d', '--device', default=None, type=str,
    #                     help='indices of GPUs to enable (default: all)')
    args = parser.parse_args()

    config = json.load(open(args.config))
    if args.resume:
        config = torch.load(args.resume)['config']
    if args.device:
        os.environ["CUDA_VISIBLE_DEVICES"] = args.device

    main(args.resume)