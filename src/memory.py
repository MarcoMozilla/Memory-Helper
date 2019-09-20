from lzpy import Table,Root
from pprint import pprint

from .detailRecord import DetailRecord
from .sumRecord import SumRecord
from .queryDict import QueryDict
from pynput.keyboard import Key, Listener
from datetime import datetime,timedelta

from .dictMaker import getsubTable,getsubNode,makeDictfromTable,makeDictfromRoot
"""

"""

Table.coding = "GBK"

#read Table from data/ read node from data
#--option: select from table/node

def getcent(part,total):
    result= round(part*100/total,2)
    return result

def prestart(dctn,recordname):
    global totalcount,goodcount,start_time,end_time,currentkey,hint
    sr =  SumRecord()
    dr = DetailRecord(recordname, dctn)
    right = "✔"
    wrong = "✘"
    query = QueryDict(dctn)
    totalcount = 0
    goodcount = 0

    out = "{}                   {}%  #{}\n"

    hintkey = Key.alt_l
    goodkey = Key.shift
    badkey = Key.ctrl_l

    print()
    print(f"answer:  {hintkey}")
    print(f"correct: {goodkey}")
    print(f"wrong:   {badkey}")
        
    print("\n=======================start=======================\n")
    currentkey = query.randkey()
    print(currentkey)

    start_time = datetime.now()
    #print("                                       ","start_time:",start_time)
    hint=True

    def on_press(key):
        global totalcount, goodcount,start_time, end_time,currentkey,Tdelta,acy,hint
        #check good or bad
        #print(hint)
        #print("                                       ",repr(key))
        #Get Value to check

        if hint and key == hintkey:
            hint = False
            # HINT
            pprint(query[currentkey])
            end_time = datetime.now()

            #print("                                       ","end_time:", end_time)
            Tdelta = end_time - start_time
            #print("                                       ","Tdelta:",Tdelta)

        # Respond good or bads
        elif not hint and (key == goodkey or key == badkey):
            hint= True
            outstring=""
            if key == goodkey:
                # GOOD
                totalcount += 1
                goodcount += 1
                acy = getcent(goodcount, totalcount)
                # currentkey, query[currentkey]
                outstring = out.format(right, acy, len(query)-1)

                # track detailrecord
                dr.plusDuration(currentkey, Tdelta)

                # delete & update currentkey
                del query[currentkey]

            elif key == badkey:
                # BAD
                totalcount += 1
                acy = getcent(goodcount, totalcount)
                # currentkey, query[currentkey]
                outstring = out.format(wrong, acy, len(query))

                # track detailrecord
                dr.incTotal(currentkey)
                dr.plusDuration(currentkey, Tdelta)

            print(outstring)

            #new turn
            if len(query) > 0:
                currentkey = query.randkey()
                print(currentkey)
                start_time = datetime.now()
                #print("                                       ","start_time:",start_time)

            else:
                sr.appendnum(recordname, acy)


                #start processing detailrecord

                totalperiod = timedelta()
                maxperiod = timedelta()
                track_table = Table([["key","value","count","period(s)"]])

                for key in dr.body:
                    item = dr.body[key][-1]
                    period = item["p"]
                    totalperiod += period
                    maxperiod  = max(maxperiod,period)
                    row = [key,dctn[key],item["c"],period]
                    track_table.append(row)
                print("\n=================complete=================")

                def d2s(d):
                    return str(round(d.total_seconds(),2))

                print("cost: {} sec".format(d2s(totalperiod)))
                print("ave: {} sec".format(d2s(totalperiod/len(dctn))))
                print("max: {} sec".format(d2s(maxperiod)))
                print()
                track_table = track_table.select(where =lambda row: row["count"] != 0).orderby("count",reverse=True)
                track_table.apply(-1,fparamod="e",f=lambda r:d2s(r))

                print(track_table)
                print()

                sr.save()
                dr.save()
                return False
        else:
            pass

    with Listener(on_press=on_press) as listener:
        listener.join()

#generate dictionary from table
#read sumdata & target detail from record folder
#use dctn start memory, track current to detail_record

#finish the memory, calculate sum_record save, save detail_record
#print the summary info of this memory exercise

def startTable(filename,subpath,kname,vname,**kwargs):
    Table.encoding = "GBK"
    Tori = Table.read(filename,subpath=subpath)
    Tselect = getsubTable(Tori,**kwargs)
    dctn,name = makeDictfromTable(Tselect,kname,vname)
    prestart(dctn,name)

def startNode(filename,subpath,*args):
    Nori = Root.read(filename,subpath=subpath)
    Nselect = getsubNode(Nori,*args)
    dctn,name = makeDictfromRoot(Nselect)
    if len(dctn) > 0:
        prestart(dctn,name)
    else:
        raise Exception("dctn is empty")

if __name__ == "__main__":
    startTable("genki_2_volcab","../nres/","eng","hiragana",lesson=13)
    #Table.read("genki_2_volcab", "../nres/")
    #t = Table.read("genki_2_volcab", subpath="../nres/")
