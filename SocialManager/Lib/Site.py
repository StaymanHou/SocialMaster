import Mydb

class Site(object):
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

    def create(self):
    	cur = Mydb.MydbExec(("INSERT INTO sites (site_category_id, domain) VALUES (%s, %s)", (self.fields['site_category_id'], self.fields['domain'])))
    	self.id = cur.lastrowid
    	return

    def GetOrCreate(domain):
    	site = Site()
        cur = Mydb.MydbExec(("SELECT * FROM sites WHERE domain = %s LIMIT 1", (domain,)))
        if cur.rowcount:
            row = cur.fetchone()
            site['id'] = row['id']
            site['site_category_id'] = row['site_category_id']
            site['domain'] = row['domain']
        else:
        	site['site_category_id'] = 1
        	site['domain'] = domain
        	site.create()
        return site
    
    GetOrCreate = staticmethod(GetOrCreate)		