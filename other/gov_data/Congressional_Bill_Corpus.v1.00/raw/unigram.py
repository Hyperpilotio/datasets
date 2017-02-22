"""
Standardized the text
Then prune the rare words and frequent words.

see ./cmnd.sh for the example of running this scripts  

"""

import sys
import json
import getopt
import codecs
from operator import itemgetter 
import lc_util

## chnage here to try out different type of pruning
RARE_WORD_COUNT = 20
DF_RARE = 0.0005
DF_FREQ = 0.30

if __name__ == "__main__":

	text_source = sys.argv[2]  ## specify which attribute to use
	fdata = lc_util.read_file(sys.argv[1], text_source) #input file
	train_file = open(sys.argv[3],'w')  #output: json feature file for trainign 

	stop = [] ## get the stop word list
	fh = open(sys.argv[6], 'r') 
	for line in fh: stop.append(line.strip('\n'))
	fh.close()

	fdata_test = lc_util.read_file(sys.argv[4], text_source) ## input file
	test_file = open(sys.argv[5],'w')  ## write the json file for training 

	total_doc = len(fdata)
	df_rare_words = total_doc * DF_RARE
	df_freq_words = total_doc * DF_FREQ 
	print 'total document %d' % (total_doc,)
	print 'df rare word cut off %f' % (df_rare_words,)
	print 'df freq word cut off %f' % (df_freq_words,)
	print 'general rare word cut off %d' % (RARE_WORD_COUNT,)

	## carve_data() does basic standardization.
	vocab_ngram,df_ngram,chunked_ngram = lc_util.carve_data_ngram(fdata)

	trimed_vocab_ngram = {}
	total_vocab_size = 0
	for i in sorted(vocab_ngram.items(), key=itemgetter(1), reverse=True):

		## freq based trimming 2. stop words
		if i[0] in stop:
			continue
		## skip all digit or punctuation:
		if i[0] == lc_util.META_NUM:
			continue
		if i[1] <= RARE_WORD_COUNT:
			continue 
		## freq based trimming. drop words appeared only in one doc
		if df_ngram[i[0]] <= df_rare_words:
			continue
		## freq based trimming. drop words appears everywhere.
		if df_ngram[i[0]] >= df_freq_words:
			continue
		## remove some of the left-over html encoding:
		if text_source == 'title' and '<' in i:
			continue
		if text_source == 'title' and '>' in i:
			continue
		if text_source == 'title' and i == 'br':
			continue
		trimed_vocab_ngram[i[0]] = i[1]
		total_vocab_size += 1
	print total_vocab_size  
	

	## write the feature for training set:
	counter = 0
	for i in chunked_ngram.keys():
		tmp = {}
		for j in chunked_ngram[i].keys():
			if j in trimed_vocab_ngram:
				if text_source == 'title': tmp['titel-word_'+j] = 1
				else: tmp['body-word_'+j] = 1
		train_file.write(i + '\t' + json.dumps(tmp) + '\n')
		counter += 1
		if counter % 1000 == 0: print('%d file written' % (counter,))
	train_file.close()

	## write the feature for test set 
	counter = 0
	chunked_ngram_test = lc_util.process_test_data(fdata_test, trimed_vocab_ngram)
	for i in chunked_ngram_test.keys():
		tmp = {}
		for j in chunked_ngram_test[i].keys():
			if text_source == 'title': tmp['titel-word_'+j] = 1
			else: tmp['body-word_'+j] = 1
		test_file.write(i + '\t' + json.dumps(tmp) + '\n')
		counter += 1
		if counter % 1000 == 0: print('%d test file written' % (counter,))
	test_file.close()
