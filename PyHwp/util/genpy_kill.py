import os, shutil

def genpy_kill(directory: str| os.PathLike):
    file_list = os.listdir(directory)
    for i in file_list:
        try:
            shutil.rmtree(os.path.join(directory, i))
        except:
            print(f"genpy kill pass {i}")