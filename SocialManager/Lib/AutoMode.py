import Mydb

class AutoMode(object):
    def __init__(self):
        self.id=None
        self.fields={}
        self.fields['title'] = None
	
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
    
    def StaticGetByPk(id):
        am = AutoMode()
        cur = Mydb.MydbExec(("SELECT id, title FROM auto_modes WHERE id = %s",(id)))
        if cur.rowcount:
            row = cur.fetchone()
            am['id'] = row['id']
            am['title'] = row['title']
        return am
    
    GetByPk = staticmethod(StaticGetByPk)
    
