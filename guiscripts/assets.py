import os

class Assets(object):

    def __init__(self):    
        self.assets_dir = {"gui_resources" : f'{os.getcwd()}\\gui_resources',
                           "ember" : f'{os.getcwd()}\\data'}
    