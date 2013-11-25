import MySQLdb
import Mydb

class Module(object):
    def __init__(self):
        self.pk=None
        self.fields={}

    def __getitem__(self,field):
        if field == 'PK':
            return self.pk
        else:
            if field in self.fields:
                return self.fields[field]

    def __setitem__(self,field,value):
        if field == 'PK':
            self.pk = value
        else:
            self.fields[field] = value
    
    def StaticGetActiveList():
        cur = Mydb.MydbExec(("SELECT PK, NAME FROM module",))
        modlst = cur.fetchall()
        return modlst

    GetActiveList = staticmethod(StaticGetActiveList)

