#!/usr/bin/env python

import os
from scripts.ember import Ember
from scripts.features import PEFeatureExtractor

import argparse
import lightgbm as lgb


def main(model_file='data\\model.txt', binary_path='bins\\invi.exe'):
    # prog = "classify_binaries"
    # descr = "Use a trained ember model to make predictions on PE files"
    # parser = argparse.ArgumentParser(prog=prog, description=descr)
    # parser.add_argument("-v", "--featureversion", type=int, default=2, help="EMBER feature version")
    # parser.add_argument("-m", "--modelpath", type=str, default=None, required=True, help="Ember model")
    # parser.add_argument("binaries", metavar="BINARIES", type=str, nargs="+", help="PE files to classify")
    # args = parser.parse_args()
    ember = Ember()

    # if not os.path.exists(args.modelpath):
    #     parser.error("ember model {} does not exist".format(args.modelpath))
    lgbm_model = lgb.Booster(model_file=model_file)

    if not os.path.exists(binary_path):
        print("{} does not exist".format(binary_path))

    file_data = open(binary_path, "rb").read()
    print(file_data)
    score = ember.predict_sample(lgbm_model, file_data, 2)
    print(score)

main()