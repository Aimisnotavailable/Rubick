import os
import json

class Assets(object):

    def __init__(self):
        with open(f"{os.getcwd()}\\path_resources\\path_resources.json") as fp:
            assets_path = json.load(fp)

        self.assets_dir = {"gui_resources" : f'{os.getcwd() + assets_path["gui_resources"]}',
                           "ember_model" : f'{os.getcwd() + assets_path["ember_model"]}'}
    