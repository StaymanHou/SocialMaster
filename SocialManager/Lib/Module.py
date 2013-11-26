import Mydb

class Module(object):
    def __init__(self):
        self.id=None
        self.fields={}

    def __getitem__(self,field):
        if field == 'id':
            return self.id
        else:
            if field in self.fields:
                return self.fields[field]

    def __setitem__(self,field,value):
        if field == 'id':
            self.id = value
        else:
            self.fields[field] = value
    
    def StaticGetActiveList():
        cur = Mydb.MydbExec(("SELECT id, name FROM smodules",))
        modlst = cur.fetchall()
        return modlst

    GetActiveList = staticmethod(StaticGetActiveList)

