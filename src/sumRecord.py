from lzpy import Root,Table
from pprint import pprint
from datetime import datetime,timedelta
import time

class SumRecord:

    """
    def nkv2str(name,qkey,qvalue):
        return "{}:{}-{}".format(name, qkey, qvalue)
    """
    subpath = "rec/"
    recordname = "summary"
    def __init__(self):
        try:
            self.record = Root.read(SumRecord.recordname,subpath=SumRecord.subpath)
        except:
            self.record = Root({}, name=SumRecord.recordname,subpath=SumRecord.subpath)
        self.body =self.record.body

    def appendnum(self, recordkey, num):
        if not recordkey in self.body:
            self.body[recordkey] = []
        self.body[recordkey].append(num)

    def save(self):
        self.record.save()

if __name__ == "__main__":
    keyname= "epoch1"
    sr = SumRecord()
    sr.appendnum(keyname,89)
    sr.save()




