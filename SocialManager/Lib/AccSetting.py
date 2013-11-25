import MySQLdb
import Mydb
from datetime import datetime, timedelta
import json

class AccSetting(object):
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
    
    def StaticGetByAccAndMod(acc, mod):
        cur = Mydb.MydbExec(("SELECT PK, ACCOUNT, MODULE, USERNAME, DES_DECRYPT(`PSWD`,%s) AS PSWD, OTHER_SETTING, EXTRA_CONTENT, ACTIVE, AUTO_MODE, TIME_START, TIME_END, NUM_PER_DAY, MIN_POST_INTERVAL, QUEUE_SIZE FROM acc_setting WHERE ACCOUNT = %s AND MODULE = %s",(Mydb.Mydb_key, acc, mod)))
        accsetting = cur.fetchone()
        now = datetime.now()
        if accsetting['OTHER_SETTING'] is not None and accsetting['OTHER_SETTING']!='':
            accsetting['OTHER_SETTING'] = json.loads(accsetting['OTHER_SETTING'])
        else:
            accsetting['OTHER_SETTING'] = {}
        accsetting['TIME_START'] = (now.replace(hour=0,minute=0,second=0,microsecond=0)+accsetting['TIME_START']).time()
        accsetting['TIME_END'] = (now.replace(hour=0,minute=0,second=0,microsecond=0)+accsetting['TIME_END']).time()
        return accsetting

    GetByAccAndMod = staticmethod(StaticGetByAccAndMod)

