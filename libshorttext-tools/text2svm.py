#!/usr/bin/env python

from sys import argv, stderr
from libshorttext.converter import *

def exit_with_help():
	print("""\
Usage: text2svm.py [options] text_src [output]
This script generates a directory containing needed information for converting
short texts to LIBSVM format. An output file in LIBSVM format is also generated.

options:
    -P {0|1|2|3|4|5|6|7}
        Preprocessor options. The options include stopwrod removal, 
        stemming, and bigram. (default 1)
        0   no stopword removal, no stemming, unigram
        1   no stopword removal, no stemming, bigram
        2   no stopword removal, stemming, unigram
        3   no stopword removal, stemming, bigram
        4   stopword removal, no stemming, unigram
        5   stopword removal, no stemming, bigram
        6   stopword removal, stemming, unigram
        7   stopword removal, stemming, bigram
Default output will be a file "text_src.svm" and a directory "text_src.text_converter." 
If "output" is specified, the output will be "output.svm" and "output.text_converter."
""")
	exit(1)

if __name__ == '__main__':
	if len(argv) < 2:
		exit_with_help()
	text_src = None 
	output = None
	converter_arguments = '-stopword 0 -stemming 0 -feature 1'

	i = 1
	while(True):
		if i >= len(argv): break

		if not argv[i].startswith('-'):
			if text_src is None:
				text_src = argv[i]
			elif output is None:
				output = argv[i]
			else:
				exit_with_help()
			i += 1
			continue

		value = argv[i+1]
		if argv[i] == '-P':
			if value.startswith('-'):
				stderr.write("Warning: no preprocessor argument {0}. Directly passed to libshorttext.converter.\n".format(value))
				converter_arguments = value
			else:
				if len(value) != 1: 
					exit_with_help()
				opt = int(value)
				stopword = (opt & 4) >> 2
				stemming = (opt & 2) >> 1
				feature = opt & 1
				converter_arguments = '-stopword {0} -stemming {1} -feature {2}'.format(stopword, stemming, feature)
		else:
			stderr.write('Error: No option ' + argv[i] + '\n')
			exit_with_help()

		i += 2

	if not text_src:
		stderr.write('Error: Text data path is not given.\n')
		exit_with_help()

	if output is None:
		output = text_src
	text_converter_dir = output + '.text_converter'
	text_converter = Text2svmConverter(converter_arguments)
	convert_text(text_src, text_converter, output + '.svm')
	text_converter.save(text_converter_dir)
