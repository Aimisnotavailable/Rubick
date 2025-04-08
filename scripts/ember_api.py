#!/usr/bin/env python

import os
from scripts.ember import Ember
from scripts.features import PEFeatureExtractor
from datascripts.handler import Handler

import lightgbm as lgb


class EmberModel:
    def __init__(self, assets):
        self.ember = Ember()
        self.assets = assets

    def get_prediction(self, handler : Handler, binary_path : SystemError):
        try:
            lgbm_model = lgb.Booster(model_file=f'{self.assets.assets_dir["ember_model"]}')
            if not os.path.exists(binary_path):
                print("{} does not exist".format(binary_path))

            file_data = open(binary_path, "rb").read()
            score = self.ember.predict_sample(lgbm_model, file_data, 1)

            handler.set_result(score)
            handler.set_status("done")

        except Exception as e:
            handler.set_result(f'{e}')
            handler.set_status("error")
