import MySQLdb
import Mydb

class MainConf(object):
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
    
    def StaticGet():
	mc = MainConf()
        cur = Mydb.MydbExec(("SELECT PK, TITLE, CACHING_TIME, IMAGE_FILE_DIR, LOAD_ITERATION, PULLER_ITERATION, POSTER_ITERATION FROM main_conf WHERE PK = 1",))
        if cur.rowcount:
            row = cur.fetchone()
            mc['PK'] = row['PK']
            mc['TITLE'] = row['TITLE']
            mc['CACHING_TIME'] = row['CACHING_TIME']
            mc['IMAGE_FILE_DIR'] = row['IMAGE_FILE_DIR']
            if mc['IMAGE_FILE_DIR'][-1]!='/': mc['IMAGE_FILE_DIR']+='/'
            mc['LOAD_ITERATION'] = row['LOAD_ITERATION']
            mc['PULLER_ITERATION'] = row['PULLER_ITERATION']
            mc['POSTER_ITERATION'] = row['POSTER_ITERATION']
        return mc

    Get = staticmethod(StaticGet)


