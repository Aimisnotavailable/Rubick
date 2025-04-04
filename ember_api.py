#!/usr/bin/env python

import os
from scripts.ember import Ember
from scripts.features import PEFeatureExtractor

import lightgbm as lgb


class EmberModel:
    def __init__(self, assets):
        self.ember = Ember()
        self.assets = assets

    def get_prediction(self, binary_path : str, model_file ='\\model.txt'):
        try:
            lgbm_model = lgb.Booster(model_file=f'{self.assets.assets_dir["ember"]}\\{model_file}')
            if not os.path.exists(binary_path):
                print("{} does not exist".format(binary_path))

            file_data = open(binary_path, "rb").read()
            score = self.ember.predict_sample(lgbm_model, file_data, 1)

            print("SCORE: ", score)
        except Exception as e:
            print(e)
