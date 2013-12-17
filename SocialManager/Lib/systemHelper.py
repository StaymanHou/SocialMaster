import platform
from dateutil import parser as dateutilparser
from datetime import datetime
import pytz

def specialize_path(gene_path):
	if platform.system() is 'Windows':
		return gene_path.replace('/','\\')
	return gene_path

def parseTime(t):
	if platform.system() is 'Windows':
		d = dateutilparser.parse(t)
		if d.tzinfo:
			est = pytz.timezone('US/Eastern')
			return d.astimezone(est).replace(tzinfo=None)
		return d
	return datetime.strptime(t, '%a, %d %b %Y %H:%M:%S %Z')

