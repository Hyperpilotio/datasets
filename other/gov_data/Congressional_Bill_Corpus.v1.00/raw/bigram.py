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


RARE_WORD_COUNT = 20 #increase the cutoff for bill text #rare_words = 10 0
DF_RARE = 0.0005
DF_FREQ = 0.30

if __name__ == "__main__":

	text_source = sys.argv[2]  ## specify which attribute to use
	fdata = lc_util.read_file(sys.argv[1], text_source) ## input file
	train_file = open(sys.argv[3],'w')  ## write the json file for training 

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
	vocab_bigram,df_bigram,chunked_bigram = lc_util.carve_data_bigram_real(fdata)

	#for i in sorted(df.items(), key=itemgetter(1), reverse=True):
	#	print len(i[1])

	trimed_vocab_bigram = {}
	total_vocab_size = 0
	for i in sorted(vocab_bigram.items(), key=itemgetter(1), reverse=True):
		if i[1] <= RARE_WORD_COUNT:
			#disca.write('RARE: %s\n' % (i[0],));
			continue 
		## freq based trimming. drop words appeared only in one doc
		if df_bigram[i[0]] <= df_rare_words:
			#disca.write('DFRARE: %s %d \n' % (i[0], i[1] ))
			continue
		## freq based trimming. drop words appears everywhere.
		if df_bigram[i[0]] >= df_freq_words:
			#disca.write('DFFREQ: %s %d %d\n' % (i[0],i[1],df_bigram[i[0]]) )
			continue
		## remove some of the left-over html encoding:
		if text_source == 'title' and '<' in i:
			continue
		if text_source == 'title' and '>' in i:
			continue
		if text_source == 'title' and i == 'br':
			continue
		trimed_vocab_bigram[i[0]] = i[1]
		total_vocab_size += 1
	print total_vocab_size  
	
	## clean out the chunked data:
	counter = 0
	for i in chunked_bigram.keys():
		tmp = {}
		for j in chunked_bigram[i].keys():
			if j in trimed_vocab_bigram:
				#tmp[j] = 1
				if text_source == 'title': tmp['titel-word_'+j] = 1
				else: tmp['body-word_'+j] = 1
		train_file.write(i + '\t' + json.dumps(tmp) + '\n')
		counter += 1
		if counter % 1000 == 0: print('%d file written' % (counter,))
	train_file.close()

	## get the test data set
	counter = 0
	chunked_bigram_test = lc_util.process_test_data_bigram(fdata_test, trimed_vocab_bigram)
	for i in chunked_bigram_test.keys():
		tmp = {}
		for j in chunked_bigram_test[i].keys():
			if text_source == 'title': tmp['titel-word_'+j] = 1
			else: tmp['body-word_'+j] = 1
		test_file.write(i + '\t' + json.dumps(tmp) + '\n')
		counter += 1
		if counter % 1000 == 0: print('%d test file written' % (counter,))
	test_file.close()
