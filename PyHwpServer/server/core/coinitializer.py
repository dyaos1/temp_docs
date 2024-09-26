from threading import Thread
from main import main
import pythoncom

class CoInitializer(Thread):
    def __init__(self, data):
        self.data = data
        super().__init__()

    def run(self):
        pythoncom.CoInitialize()
        
        main(self.data)

        pythoncom.CoUninitialize()