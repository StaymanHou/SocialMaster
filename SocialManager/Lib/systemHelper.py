import platform
from dateutil import parser as dateutilparser
from datetime import datetime

def specialize_path(gene_path):
	if platform.system() is 'Windows':
		return gene_path.replace('/','\\')
	return gene_path

def parseTime(t):
	if platform.system() is 'Windows':
		return dateutilparser.parse(t)
	return datetime.strptime(t, '%a, %d %b %Y %H:%M:%S %Z')

