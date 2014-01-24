#!/usr/bin/env python
# Author: Paweł Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2013 IITiS PAN Gliwice
# Licensed under GNU GPL v3 (see the LICENSE file)

from libshorttext import converter as lst_conv
import tokenizer
import argparse
import params as P

# convert text to SVM format
def prepare(outdir):
	cpath = outdir+"/converter"
	path = outdir+"/train.txt"
	opath = outdir+"/train.svm"

	print "creating new converter..."
	conv = lst_conv.Text2svmConverter()
	conv.class_map.toIdx("Unknown")
	conv.text_prep.tokenizer = tokenizer.tokenizer

	print "converting %s to %s" % (path, opath)
	lst_conv.convert_text(path, conv, opath)
	
	print "saving converter to %s" % cpath
	conv.save(cpath)

def main():
	p = argparse.ArgumentParser(description='Convert training samples to VSM format')
	p.add_argument("--exe", help="exec given Python file")
	p.add_argument('model', help='dir with model and train.txt')
	args = p.parse_args()

	if args.exe: exec(file.read(open(args.exe)))
	prepare(args.model)

if __name__ == "__main__": main()
