#How to run:
#>> python bigram.py input_json [title|text] output_json input_test_json output_json
#>> python unigram.py input_json [title|text] output_json input_test_json output_json stop_words.txt 
#
# NOTE: YOU need to split the row input file (included) into the training and test set.

# local examples. do not copy -----------------------|
#python unigram.py ../../congresses/train_103_110.json title ./train_103_110_title_bigram.json ../../congresses/congress111.json ./congress111_title_bigram.json stop_words.txt |tee test.log
#python unigram.py ../../congresses/train_103_110.json text ./train_103_110_text_bigram.json ../../congresses/congress111.json ./congress111_text_bigram.json stop_words.txt |tee test.log
#python bigram.py ../../congresses/train_103_110.json title ./train_103_110_title_bigram.json ../../congresses/congress111.json ./congress111_title_bigram.json  |tee test.log
