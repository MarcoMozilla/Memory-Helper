from lzpy import Root, Table
from pprint import pprint
from datetime import datetime,timedelta

import time

class DetailRecord:
    """
    def nkv2str(name,qkey,qvalue):
        return "{}:{}-{}".format(name, qkey, qvalue)
    """

    subpath = "rec/"
    timeout = timedelta(minutes=5)

    def __init__(self,recordname,keys):
        self.recordname = recordname
        self.keys = keys
        # initialize record
        encoding_save = Root.encoding
        try:
            self.record = Root.read(recordname,subpath = DetailRecord.subpath)
        except:
            self.record = Root({}, name=recordname,subpath = DetailRecord.subpath)
            for key in keys:
                self.record.body[key] = []
        Root.encoding = encoding_save

        # initialize current value
        self.body =self.record.body
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for key in self.body:
            sub = {"dt": dt,
                     "c": 0,
                    "p": timedelta()}
            self.body[key].append(sub)

    def incTotal(self,key):
        self.body[key][-1]["c"]+=1

    def plusDuration(self,key,amount):
        if not isinstance(amount,timedelta):
            raise Exception("amount should be 'timedelta' object")

        if amount < DetailRecord.timeout:
            self.body[key][-1]["p"] += amount
        else:
            print("timeout {}".format(DetailRecord.timeout))

    def save(self):
        for key in self.record.body:
            for item in self.record.body[key]:
                item["p"] = str(item["p"])

        self.record.save()
        #del self.record

if __name__ == "__main__":
    name= "testrecordname"
    kv = {"A":{"a":"","aa":"","aaa":""},
          "C":{"c":""},
          "D":{"d":"","dd":"","ddd":""},
          "G":{"g":""}}
    dr = DetailRecord(name,kv)
    dr.incTotal("A")
    dr.plusDuration("C",timedelta(minutes=2))

    dr.save()




