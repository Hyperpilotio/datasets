"""
aux functions, etc

"""
import json
import re

prog0 = re.compile('[^a-zA-Z0-9]{2,}') 
prog1 = re.compile('[(){}\[\]".,;:!?]+') 
prog2 = re.compile('[^a-zA-Z_-]+')
META_NUM = '__META_NUM_PUNC__'
meta_num_dict = {}

def compress_num(t):
	m = prog2.match(t)
	if m:
		if t not in meta_num_dict: meta_num_dict[t] = t
		t = META_NUM 
	return t

def cln_tkn(raw_t):
	t = raw_t.lower()
	#if t.endswith((',','.',';',':','!','?')):
	t = t.strip('(){}[]".,;:!?-_')
	return t 

def cln_words(words):
	# \n should be converted to space
	# non-alpha-numeric >2 is compressed to ONE space
	tmp = words.replace('\n', ' ')
	tmp = prog0.sub(' ', tmp)
	tmp = prog1.sub(' ', tmp)
	tkns = []
	for raw_t in tmp.split():
		t = cln_tkn(raw_t)
		## compress chunk of numbers and punctuation, 
		## compress chunk of numbers and only one words
		t = compress_num(t)
		tkns.append(t)	
	return tkns

def carve_data_ngram(data):
	vocab = {}; counter = 0; df = {}; chunked_data = {};
	for k in data.keys():
		counter += 1
		if counter % 1000 == 0:  print counter
		words = data[k]
		tkns = cln_words(words)
		new_tkns = {}
		for t in tkns:
			if t not in vocab: vocab[t] = 0
			if t not in df: df[t] = 0 
			if t not in new_tkns:
				new_tkns[t] = 1
				df[t] += 1
			vocab[t] += 1
		chunked_data[k] = new_tkns
	return vocab, df, chunked_data

def process_test_data(data, vocab):
	chunked_data = {};
	for k in data.keys():
		words = data[k]
		tkns = cln_words(words)
		new_tkns = {}
		for t in tkns:
			if t not in vocab: continue
			if t not in new_tkns:
				new_tkns[t] = 1
		chunked_data[k] = new_tkns
	return chunked_data

def carve_data_bigram_real(data):
	vocab = {}; counter = 0; df = {}; chunked_data = {};
	for k in data.keys():
		counter += 1
		if counter % 1000 == 0:  print counter
		words = data[k]
		tkns = cln_words(words)
		new_tkns = {}
		for i in range(len(tkns)-1):
			t1 = tkns[i]; t2 = tkns[i+1]
			t = t1 + '_' + t2	
			if t not in vocab: vocab[t] = 0
			if t not in df: df[t] = 0 
			if t not in new_tkns:
				new_tkns[t] = 1
				df[t] += 1
			vocab[t] += 1
		chunked_data[k] = new_tkns
	return vocab, df, chunked_data

def process_test_data_bigram(data, vocab):
	chunked_data = {};
	for k in data.keys():
		words = data[k]
		tkns = cln_words(words)
		new_tkns = {}
		for i in range(len(tkns)-1):
			t1 = tkns[i]; t2 = tkns[i+1]
			t = t1 + '_' + t2	
			if t not in vocab: continue
			if t not in new_tkns:
				new_tkns[t] = 1
		chunked_data[k] = new_tkns
	return chunked_data

def read_file(file, attr='text'):
	docs = {}; count = 0
	fh = open(file, 'r')
	for line in fh:
		docid,datam=line.split('\t')
		feats=json.loads(datam)
		if attr not in feats: continue
		content = feats[attr] 
		docs[docid] = content 
		count += 1
		if count % 10000 == 0: print('%d file read' % (count,))
	fh.close()
	return docs
