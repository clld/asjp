'''
Created on Feb 6, 2012
String distances from the AsjpDist-full program
@author: rarakar
Changed the defaultdict implementation to collections
Implemented the 
'''
#import nltk
from collections import defaultdict
import itertools as it
UNNORM = True

def ldn(a,b):
	m=[];la=len(a)+1;lb=len(b)+1
	for i in range(0,la):
		m.append([])
		for j in range(0,lb):m[i].append(0)
		m[i][0]=i
	for i in range(0,lb):m[0][i]=i
	for i in range(1,la):
		for j in range(1,lb):
			s=m[i-1][j-1]
			if (a[i-1]!=b[j-1]):s=s+1 
			m[i][j]=min(m[i][j-1]+1,m[i-1][j]+1,s)	
	la=la-1;lb=lb-1
#	print a, b, float(m[la][lb])/float(max(la,lb))
	if UNNORM:
		return float(m[la][lb])
	return float(m[la][lb])/float(max(la,lb))

def dice(a, b):
	la = len(a) - 1;lb = len(b) - 1
	overlap = 0
	dicta = defaultdict(int)
	dictb = defaultdict(int)
	for i in range(len(a) - 1):
		tmp = ",".join(map(str, a[i:i + 2]))
		dicta[tmp] += 1
	for j in range(len(b) - 1):
		tmp = ",".join(map(str, b[j:j + 2]))
		dictb[tmp] += 1
	for entry in dicta:
		if(dictb.has_key(entry)):
			  overlap = overlap + min(dicta.get(entry), dictb.get(entry))
	total = la + lb
	if total == 0:
		return 0
	if UNNORM:
#		return float(2.0 * overlap)
		return float(total) - float(2.0*overlap)
	return 1.0 - (float(2.0 * overlap) / float(total))

def lcs(a, b):
	m = [];la = len(a) + 1;lb = len(b) + 1
	for i in range(0, la):
		m.append([])
		for j in range(0, lb):m[i].append(0)
		m[i][0] = 0
	for i in range(0, lb):m[0][i] = 0
	for i in range(1, la):
		for j in range(1, lb):
			if (a[i - 1] == b[j - 1]):m[i][j] = m[i - 1][j - 1] + 1
			else:m[i][j] = max(m[i][j - 1], m[i - 1][j])
	la = la - 1;lb = lb - 1
	#print a, b, m[la][lb]
	if UNNORM:
		return float(max(la, lb)) - float(m[la][lb])
	return 1.0 - (float(m[la][lb]) / float(max(la, lb)))

def jcd(a, b):
	#Only computes the bigram jaccard index. Have to extend it for high order N
	la = len(a) - 1;lb = len(b) - 1
	overlap = 0
	dicta = defaultdict(int)
	dictb = defaultdict(int)
	for i in range(len(a) - 1):
		tmp = ",".join(map(str, a[i:i + 2]))
		dicta[tmp] += 1
	for j in range(len(b) - 1):
		tmp = ",".join(map(str, b[j:j + 2]))
		dictb[tmp] += 1
	for entry in dicta:
		if(dictb.has_key(entry)):
			overlap = overlap + min(dicta.get(entry), dictb.get(entry))
	total = la + lb - overlap
	if total == 0:
		return 0
	if UNNORM:
		return float(total) - float(overlap)
	return 1.0 - (float(overlap) / float(total))

def jcd1(a, b):
	#Computes the higher order jaccard index, upto n=3
	la = len(a) - 1;lb = len(b) - 1
	overlap = 0
	n=3
	pad_symbol = "-"
	s_a = it.chain((pad_symbol,) * (n-1), a) 
	s_a = it.chain(s_a, (pad_symbol,) * (n-1))
	s_a = list(s_a)
	s_b = it.chain((pad_symbol,) * (n-1), b) 
	s_b = it.chain(s_b, (pad_symbol,) * (n-1))
	s_b = list(s_b)
	
	dicta = defaultdict(int)
	dictb = defaultdict(int)
	for i in range(len(s_a) - 1):
		for k in range(1,n+1):
			tmp = ",".join(map(str, s_a[i:i + k]))
			dicta[tmp] += 1
	for j in range(len(s_b) - 1):
		for k in range(1,n+1):
			tmp = ",".join(map(str, s_b[i:i + k]))
			dictb[tmp] += 1		
	for entry in dicta:
		if(dictb.has_key(entry)):
			overlap = overlap + min(dicta.get(entry), dictb.get(entry))
	total = la + lb - overlap
	if total == 0:
		return 0
	if UNNORM:
		return float(total) - float(overlap)
	return 1.0 - (float(overlap) / float(total))

def prefix(a,b):
	#print a, b
	la = len(a); lb = len(b)
	minl = min(la,lb)
	maxl = max(la,lb)
	pref = 0
	for i in range(minl):
		if a[i] == b[i]:
				pref += 1
	if UNNORM:
		return float(maxl) - float(pref)
	return 1.0 - (float(pref)/float(maxl))

def xdice(a,b):
	la=len(a)-2;lb=len(b)-2
	overlap=0
	#print a, b
	#print la, lb
	dicta=defaultdict(int)
	dictb=defaultdict(int)
	for i in range(len(a)-2):
		tmp = ",".join(map(str,[a[i],a[i+2]]))
		dicta[tmp]+=1
	for j in range(len(b)-2):
		tmp = ",".join(map(str,[b[j],b[j+2]]))
		dictb[tmp]+=1
	for entry in dicta:
		if(dictb.has_key(entry)):
#			 overlap = overlap+ min(sum(map(int,dicta.get(entry))),sum(map(int,dictb.get(entry))))
			  overlap = overlap+ min(dicta.get(entry),dictb.get(entry))
#			   if(a[i:i+2] == b[j:j+2]): overlap=overlap+1
	total = la+lb
	#print overlap
	if total==0 or la < 1 or lb < 1 :
		return 0
	if UNNORM:
		return float(total) - float(2.0*overlap)
	return 1.0 - (float(2*overlap)/float(total))

def trigram(a,b):
	la=len(a)-2;lb=len(b)-2
	overlap=0
   # print a, b
	#print la, lb
	dicta=defaultdict(int)
	dictb=defaultdict(int)
	for i in range(len(a)-2):
		tmp = ",".join(map(str,a[i:i+3]))
		dicta[tmp]+=1
	for j in range(len(b)-2):
		tmp = ",".join(map(str,b[j:j+3]))
		dictb[tmp]+=1
	for entry in dicta:
		if(dictb.has_key(entry)):
#			 overlap = overlap+ min(sum(map(int,dicta.get(entry))),sum(map(int,dictb.get(entry))))
			  overlap = overlap+ min(dicta.get(entry),dictb.get(entry))
#			   if(a[i:i+2] == b[j:j+2]): overlap=overlap+1
	total = la+lb
	#print overlap
	if total==0 or la < 1 or lb < 1 :
		return float(1.0)
	if UNNORM:
		return float(total) - float(2.0*overlap)
	return 1.0 - (float(2*overlap)/float(total))

def ident(a,b):
	#print a, b
	overlap = 0
	if a == b :
		overlap = 1
	else:
		overlap = 0
	return 1.0 - float(overlap)

def xxdice(a,b):
	la = len(a) - 1;lb = len(b) - 1
	overlap = 0
	dicta = defaultdict(list)
	dictb = defaultdict(list)
	for i in range(len(a) - 1):
		tmp = ",".join(map(str, a[i:i + 2]))
		dicta[tmp].append(i)
	for j in range(len(b) - 1):
		tmp = ",".join(map(str, b[j:j + 2]))
		dictb[tmp].append(j)
	for entry in dicta:
		if(dictb.has_key(entry)):
			pos_a = dicta[entry]
			pos_b = dictb[entry]
			for m, n in it.product(pos_a, pos_b):
				overlap += 1.0/(1.0+(m-n)**2)			
	total = la + lb
	if total == 0:
		return 0
	if UNNORM:
		return float(total) - float(2.0 * overlap)
	return 1.0 - (float(2.0 * overlap) / float(total))

metricsMap = {'ldn': ldn,
			'ldn_swap': ldn_swap,
			'dice': dice, 
			'lcs': lcs,
			'jcd': jcd,
			'jcd1': jcd1,
			'prefix': prefix, 
			'xdice': xdice,
			'trigram': trigram, 
			'ident': ident			
			};

#'vc_dist': vc_dist,
def computeDistance(vector1, vector2, similarityMetric='cosine'):
	# compute similarity distances between both vectors
	if metricsMap.has_key(similarityMetric):
		return metricsMap[similarityMetric](vector1, vector2)
