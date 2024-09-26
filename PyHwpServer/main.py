from pyhwp import PyHwp
from server.deserializer import to_hwp_model

def main(payload: str):
    data = to_hwp_model(payload)
    filename = data.metadata["filename"]
    pyhwp = PyHwp(filename, True)
 
    pyhwp.openhwp()
    pyhwp.str_to_field(data.text)

    for key, list2d in data.table.items():
        pyhwp.table_maker_list2d(key, list2d)
    pyhwp.save_and_quit("result_"+filename)