import MySQLdb
import Mydb

class Account(object):
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
        cur = Mydb.MydbExec(("SELECT PK, NAME, RSS_URL, ACTIVE, TAG_LIMIT, LAST_UPDATE, DELETED FROM account WHERE ACTIVE = True AND DELETED = False",))
        acclst = cur.fetchall()
        return acclst

    GetActiveList = staticmethod(StaticGetActiveList)

    def StaticSetLastUpdate(PK, last_update):
        cur = Mydb.MydbExec(("UPDATE account SET LAST_UPDATE = %s WHERE PK = %s",(last_update, PK)))
        return

    SetLastUpdate = staticmethod(StaticSetLastUpdate)

