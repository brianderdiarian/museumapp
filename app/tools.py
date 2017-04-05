import re
from datetime import date, timedelta
import unicodedata
from app.models import Artwork#, Artist
import collections



#strip parenthesis, double parenthesis, brackets, and double brackets from strings
def strip_parenthesis(test_str):
	ret = ''
	skip1c = 0
	skip2c = 0
	for i in test_str:
		if i == '[':
			skip1c += 1
		elif i == '(':
			skip2c += 1
		elif i == ']':
			skip1c -= 1
		elif i == ')':
			skip2c -= 1
		elif skip1c == 0 and skip2c == 0:
			ret += i
	return ret

#strip html tags
def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext

#show most recent results - yesterday to be safe that all indexes are complete
today = date.today()
yesterday = (date.today() - timedelta(1))
skipcatch = (date.today() - timedelta(15))

current = date.today()

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])