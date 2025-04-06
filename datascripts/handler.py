class Handler:
    
    def __init__(self):
        self.results : float = 0
        self.status = "waiting"
    
    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def set_result(self, results):
        self.results = results
        
    def get_result(self):
        return self.results