import os
import win32com.client as win32
from time import sleep
from util import genpy_kill, abs_path, none_check
from config.configurer import load_config, ConfigPydanticModel

CONFIG: ConfigPydanticModel = load_config()

class PyHwp():
    def __init__(
            self,
            filename: str,
            visible: bool=False
        ):
        genpy_kill(CONFIG.system.genpy)

        self.directory = abs_path(CONFIG.file.directory)
        self.output_directory = abs_path(CONFIG.file.output_directory)
        print(self.directory)
        print(self.output_directory)

        self.filename = filename
        self.visible = visible
        self.filepath = os.path.join(self.directory, self.filename)
        self.filepath_checker_module = CONFIG.system.filepath_checker_module


    def openhwp(self):
        self.hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
        self.hwp.XHwpWindows.Item(0).Visible = self.visible
        self.hwp.RegisterModule("FilePathCheckDLL", self.filepath_checker_module)

        self.hwp.Open(self.filepath, "HWP", "forceopen:true")


    def save_and_quit(self, fileName:str|None=None):
        if fileName == None:
            fileName = self.filename
        if not fileName.endswith(".hwp"):
            fileName += ".hwp"
        
        self.hwp.SaveAs(os.path.join(self.output_directory, fileName))
        self.hwp.Quit()


    def quit_without_save(self):
        self.hwp.Clear(option=1)
        self.hwp.Quit()


    def str_to_field(self, dict: dict):
        """key value 형태의 딕셔너리를 입력한다.
        key가 누름틀이 되고 value가 그 누름틀에 들어갈 값이다"""
        fieldList = self.hwp.GetFieldList().split("\x02")
        keyList = dict.keys()
        for i in fieldList:
            if i in keyList:
                self.hwp.PutFieldText(i, dict[i])
        return self.hwp   


    def image_to_field(
            self, 
            fieldname: str, 
            img_full_path: str| os.PathLike, 
            width=CONFIG.image.default_width, 
            height=CONFIG.image.default_width
        ):
        self.hwp.MoveToField(fieldname, True, False, False)
        self.hwp.InsertPicture(img_full_path, Embedded=True)
        sleep(0.5)
        self.hwp.FindCtrl()

        # 크기 변경
        self.hwp.HAction.GetDefault("ShapeObjDialog", self.hwp.HParameterSet.HShapeObject.HSet)
        self.hwp.HParameterSet.HShapeObject.TreatAsChar = True
        self.hwp.HParameterSet.HShapeObject.TextWrap = 3
        self.hwp.HParameterSet.HShapeObject.Width = self.hwp.MiliToHwpUnit(width)
        self.hwp.HParameterSet.HShapeObject.Height = self.hwp.MiliToHwpUnit(height)
        self.hwp.HAction.Execute("ShapeObjDialog", self.hwp.HParameterSet.HShapeObject.HSet)


    def table_maker_list2d(self, start_field: str, list2d, new_row = True, pass_first_col = False):
        """2차원 배열을 받아 테이블을 만든다. 
        start_field: 시작점이 되는 누름틀
        new_row: False 로 하면 새 행을 추가하지 않고 값을 입력한다. 
                입력한 2차원 배열과 같은 크기의 테이블 빈 칸이 있을 경우 False로 하면 된다.        
        
        pass_first_col: True로 하게 되면 첫번째 열은 패스"""
        row = len(list2d)
        col = len(list2d[0])

        self.hwp.MoveToField(start_field, False, False, False)

        if (row > 1) and (new_row):
            self.hwp.HAction.GetDefault("TableInsertRowColumn", self.hwp.HParameterSet.HTableInsertLine.HSet)
            self.hwp.HParameterSet.HTableInsertLine.Side = self.hwp.SideType("Bottom")
            self.hwp.HParameterSet.HTableInsertLine.Count = row-1
            self.hwp.HAction.Execute("TableInsertRowColumn", self.hwp.HParameterSet.HTableInsertLine.HSet)

        for i in range(row):
            for j in range(col):
                text = list2d[i][j]
                self.hwp.HAction.GetDefault("InsertText", self.hwp.HParameterSet.HInsertText.HSet)
                self.hwp.HParameterSet.HInsertText.Text = text
                self.hwp.HAction.Execute("InsertText", self.hwp.HParameterSet.HInsertText.HSet)

                if (j<col-1):
                    self.hwp.HAction.Run("MoveRight")
                sleep(0.02)

            if (i<row-1) :
                self.hwp.HAction.Run("MoveDown")
                sleep(0.05)
                self.hwp.HAction.Run("TableColBegin")

                if pass_first_col:
                    self.hwp.HAction.Run("TableCellBlock")
                    self.hwp.HAction.Run("TableRightCell")
                    self.hwp.HAction.Run("Cancel")
                sleep(0.05)


    def cursor_to_field(self, cursor: str):
        """cursor=누름틀명
        해당 위치로 커서를 이동시킨다"""
        self.hwp.MoveToField(cursor, False, False, False)


    def get_text_from_cell(self):
        self.hwp.InitScan(Range=0xff)
        text = ""

        checker = 2
        while 1 < checker :
            checker, newText = self.hwp.GetText()
            text += newText.replace('\r\n', '\n')

        self.hwp.ReleaseScan()
        
        return text


    # 이하 세가지는 hwp.HAction 명령어를 쓰기 위한 함수
    def return_hwp(self):
        """HAction을 클래스 외부에서 쓰기 위해서 인스턴스가 hwp를 반환한다."""
        return self.hwp


    def get_hwp(self, hwp):
        """HAction을 사용하고 나서 다시 인스턴스에 hwp를 업데이트 한다."""
        self.hwp = hwp


    def HAction(self, command: str):
        """HAction를 직접 사용하기 위한 방법"""
        self.hwp.HAction.Run(command)
    # 이상 hwp.HAction 관련 함수
