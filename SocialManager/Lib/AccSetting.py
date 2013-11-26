import Mydb
from datetime import datetime
import json

class AccSetting(object):
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
    
    def StaticGetByAccAndMod(acc, mod):
        cur = Mydb.MydbExec(("SELECT id, account_id, smodule_id, username, password, other_setting, extra_content, active, auto_mode_id, time_start, time_end, num_per_day, min_post_interval, queue_size FROM acc_settings WHERE account_id = %s AND smodule_id = %s",(acc, mod)))
        accsetting = cur.fetchone()
        now = datetime.now()
        if accsetting['other_setting'] is not None and accsetting['other_setting']!='':
            accsetting['other_setting'] = json.loads(accsetting['other_setting'])
        else:
            accsetting['other_setting'] = {}
        accsetting['time_start'] = (now.replace(hour=0,minute=0,second=0,microsecond=0)+accsetting['time_start']).time()
        accsetting['time_end'] = (now.replace(hour=0,minute=0,second=0,microsecond=0)+accsetting['time_end']).time()
        return accsetting

    GetByAccAndMod = staticmethod(StaticGetByAccAndMod)

