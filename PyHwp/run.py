from py_hwp import PyHwp
from threading import Thread
import pythoncom

class SubThreading(Thread):
    def __init__(self,):
        super().__init__()

    def run(self):
        pythoncom.CoInitialize()
        
        # 여기에 코드 작성

        pythoncom.CoUninitialize()

sub_thread = SubThreading()
sub_thread.start()
sub_thread.join()