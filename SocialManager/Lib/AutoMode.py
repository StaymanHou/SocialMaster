import MySQLdb
import Mydb
import json

class AutoMode(object):
    def __init__(self):
        self.pk=None
        self.fields={}
        self.fields['MODULE'] = None
        self.fields['CODE'] = None
        self.fields['TITLE'] = None
        self.fields['OTHER_SETTING'] = None
	
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
    
    def StaticGetByPk(pk):
        am = AutoMode()
        cur = Mydb.MydbExec(("SELECT PK, MODULE, CODE, TITLE, OTHER_SETTING FROM auto_mode WHERE PK = %s",(pk)))
        if cur.rowcount:
            row = cur.fetchone()
            am['PK'] = row['PK']
            am['MODULE'] = row['MODULE']
            am['CODE'] = row['CODE']
            am['TITLE'] = row['TITLE']
            if row['OTHER_SETTING'] is not None and row['OTHER_SETTING']!='':
                am['OTHER_SETTING'] = json.loads(row['OTHER_SETTING'])
            else:
                am['OTHER_SETTING'] = {}
        return am
    
    GetByPk = staticmethod(StaticGetByPk)
    
