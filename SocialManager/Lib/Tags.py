import Mydb
import string
import re

def addhashtag(text, tag_string, mode=0):
    if tag_string is None or len(tag_string.strip())==0:
        return text
    tag_list = tag_string.split(',')
    tag_list = [tag.strip().lower() for tag in tag_list]
    tokens = text.split()
    for i in xrange(len(tokens)-2):
        for j in xrange(3,0,-1):
            try: merged_token = ' '.join(tokens[i:i+j]).strip().lower().translate(None, string.punctuation)
            except: continue
            if merged_token in tag_list:
                try: replace_text = ''.join(tokens[i:i+j]).translate(None, string.punctuation)
                except: continue
                text = re.sub('(^| )%s'%re.escape(' '.join(tokens[i:i+j])), '\\1#%s'%replace_text, text)
                if mode == 1:
                    return text
    return text

def ngrams(text, n):
    try: text = text.strip().translate(None, string.punctuation)
    except: return []
    text = text.lower().split()
    output = []
    for i in range(len(text)-n+1):
        output.append(' '.join(text[i:i+n]))
    output = set(output)
    return output

class Tags(object):
    def __init__(self):
        self.id=None
        self.fields={}
        self.fields['str'] = None
	
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
    
    def StaticParseTags(text):
        gram_limit = 3
        tags = []
        for i in range(gram_limit):
            gram_n = i+1
            tokens = ngrams(text, gram_n)
            if len(tokens)==0: continue
            fmtstr = ','.join(['%s']*len(tokens))
            cur = Mydb.MydbExec(("SELECT str FROM tags WHERE str IN (%s)"%fmtstr, tuple(tokens)))
            if cur.rowcount:
                rows = cur.fetchall()
                tags.extend([row['str'] for row in rows if 'str' in row])
        return tags
    
    ParseTags = staticmethod(StaticParseTags)
    
    def StaticSaveTags(tag_list):
        tag_list = set([tag.strip().lower() for tag in tag_list])
        if len(tag_list)==0: return
        fmtstr = ','.join(['%s']*len(tag_list))
        cur = Mydb.MydbExec(("SELECT str FROM tags WHERE str IN (%s)"%fmtstr, tuple(tag_list)))
        if cur.rowcount:
            rows = cur.fetchall()
            for row in rows:
                tag_list.remove(row['str'])
        if len(tag_list)==0: return
        fmtstr = ','.join(['(%s)']*len(tag_list))
        cur = Mydb.MydbExec(("INSERT INTO tags (str) VALUES %s"%fmtstr, tuple(tag_list)))
        return
        
    SaveTags = staticmethod(StaticSaveTags)
    
