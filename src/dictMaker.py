from pprint import pprint
from lzpy import Table,Root

#help functions
def check_repeat_key(t,keyname,detail=False):
    #use to check where have repeated key
    catch = {}
    for i in range(1,len(t)+1):
        key = t[i][keyname]
        if key in catch:
            catch[key].append(i)
        else:
            catch[key] = [i]
    res = {}
    if detail:
        for key in catch:
            if len(catch[key])>1:
                res[key]=[]
                for  i in catch[key]:
                    res[key].append([i]+list(t[i]))
    else:
        for key in catch:
            if len(catch[key])>1:
                res[key]=catch[key]
    pprint(res)


def check_repeat_key_value(t,keyname,valuename,detail=False):
    # use to check whether have repeated (key,value) pair
    catch = {}
    for i in range(1,len(t)+1):
        key = t[i][keyname]
        value=  t[i][valuename]
        pair = (key,value)
        if pair in catch:
            catch[pair].append(i)
        else:
            catch[pair] = [i]

    res = {}
    if detail:
        for key in catch:
            if len(catch[key])>1:
                res[key]=[]
                for  i in catch[key]:
                    res[key].append([i]+list(t[i]))
    else:
        for key in catch:
            if len(catch[key]) > 1:
                res[key] = catch[key]
    pprint(res)


def getsubTable(t,**kwargs):
    def check(row):
        for key in kwargs:
            if row[key] != kwargs[key]:
                return False
        return True
    Tres = t.select(where=check)
    Tres.name = t.name +"~" +",".join(["{}={}".format(key,kwargs[key]) for key in kwargs])
    return Tres

def getsubNode(r,*args):
    Nrest = r.select(args)
    Nrest.name = r.name+ "~" + "-".join([str(a) for a in args])
    return Nrest


def makeDictfromTable(t,keyname,valuename):
    res= {}
    for i in range(1,len(t) + 1):
        key = t[i][keyname]
        value = t[i][valuename]
        if key in res:
            if isinstance(res[key],list):
                res[key].append(value)
            else:
                res[key]=[res[key],value]
        else:
            res[key]=value
    name = t.name+"-({},{})".format(str(keyname),str(valuename))
    return res,name


def makeDictfromRoot(r):

    def hasdict(target):
        if isinstance(target, dict):
            return True
        elif isinstance(target,list):
            for v in target:
                if hasdict(v):
                    return True
            return False
        else:
            return False


    def toStr(target):
        if isinstance(target,set):
            return "{{{}}}".format(",".join([toStr(v) for v in target]))
        if isinstance(target,list):
            return "[{}]".format(",".join([toStr(v) for v in target]))
        else:
            return str(target)

    def merged(target, adder):
        for key in adder:
            if not key in target:
                target[key]=adder[key]
            else:
                raise Exception("KEY {} in target:{} and adder:{}".format(key, target[key],adder[key]))
        return target

    def Tlist(target, keychain=[]):
        resd = {}
        values = []
        nkey = "-".join(keychain)
        for i in range(len(target)):
            ii =i+1
            value = target[i]
            if value:
                if isinstance(value, dict):
                    Vset = set(value.keys())
                    if len(Vset) > 1:
                        nkeychain = keychain.copy() +[str(ii)]+ [toStr(Vset)]
                        merged(resd, Tdict(value, nkeychain,addkey=False))
                        values.append(Vset)
                    else:
                        subkey = list(Vset)[0]
                        nkeychain = keychain.copy() + [str(ii)] + [str(subkey)]
                        merged(resd, Tnode(value[subkey], nkeychain))
                        values.append(subkey)
                elif isinstance(value, list):
                    if hasdict(value):
                        merged(resd, Tlist(value, nkeychain))
                    else:
                        values.append(value)
                else:
                    values.append(value)
        resd[nkey] = values
        return resd

    def Tdict(target,keychain=[],addkey = True):
        resd = {}
        nkey = "-".join(keychain)
        if addkey:
            resd[nkey] = set(target.keys())
        for k in target:
            nkeychain = keychain.copy()+[k]
            nkey = "-".join(nkeychain)
            value = target[k]
            if value:
                if isinstance(value,dict):
                    merged(resd,Tdict(value,nkeychain))
                elif isinstance(value,list):
                    if hasdict(value):
                        merged(resd, Tlist(value, nkeychain))
                    else:
                        resd[nkey]=value
                else:
                    resd[nkey] = value
        return resd

    def Tnode(target,keychain=[]):
        if isinstance(target,dict):
            return Tdict(target,keychain)
        elif isinstance(target,list):
            return Tlist(target,keychain)
        elif target:
            key = "-".join(keychain)
            return {key:target}
        else:
            return {}

    res = Tnode(r.body,keychain=[])
    for key in res:
        res[key] = toStr(res[key])

    rtv = res[""]
    del res[""]
    rtname = "<MAIN>"
    res[rtname] =rtv
    name= r.name
    return res,name

if __name__ == "__main__":
    """
    Table.encoding="GBK"
    t = Table.read("kanji")
    #check_repeat_key_value(t,"hiragana","kanji")
    d = makeDictfromTable(t,"hiragana","kanji")
    pprint(d)
    """
    """
    r = Root.read("test")
    d = makeDictfromRoot(r)
    pprint(d)
    """
    """
    t =Table([["A","B","C"],
              [1,2,1],
              [1,2,0],
              [1,1,1],
              [0,2,1]])
    t.name ="test"
    res = getsubTable(t,A=1,B=2)
    res.fsee()
    """

    r = Root([{"A":{"B":1,"C":2}},{"D":2}])
    r.name = "test"
    res = getsubNode(r, 0,"A")
    res.fsee()