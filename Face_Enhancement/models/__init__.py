# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import importlib
import torch


def find_model_using_name(model_name):
    # Given the option --model [modelname],
    # the file "models/modelname_model.py"
    # will be imported.
    model_filename = f"models.{model_name}_model"
    modellib = importlib.import_module(model_filename)

    # In the file, the class called ModelNameModel() will
    # be instantiated. It has to be a subclass of torch.nn.Module,
    # and it is case-insensitive.
    model = None
    target_model_name = model_name.replace("_", "") + "model"
    for name, cls in modellib.__dict__.items():
        if name.lower() == target_model_name.lower() and issubclass(cls, torch.nn.Module):
            model = cls

    if model is None:
        print(
            f"In {model_filename}.py, there should be a subclass of torch.nn.Module with class name that matches {target_model_name} in lowercase."
        )
        exit(0)

    return model


def get_option_setter(model_name):
    model_class = find_model_using_name(model_name)
    return model_class.modify_commandline_options


def create_model(opt):
    model = find_model_using_name(opt.model)
    instance = model(opt)
    print(f"model [{type(instance).__name__}] was created")

    return instance
