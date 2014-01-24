#!/usr/bin/env python
# Author: Paweł Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2013 IITiS PAN Gliwice
# Licensed under GNU GPL v3 (see the LICENSE file)

import re
from libshorttext import converter as lst_conv
import tokenizer
import argparse

# convert text to SVM format
def prepare(outdir, path):
	cdir = outdir + "/converter"
	opath = re.sub('\.[^.]+$', '.svm', path)
	
	print "reading converter from %s..." % cdir
	conv = lst_conv.Text2svmConverter()
	conv.load(cdir)
	conv.text_prep.tokenizer = tokenizer.tokenizer
	
	print "converting %s to %s" % (path, opath)
	lst_conv.convert_text(path, conv, opath)

def main():
	p = argparse.ArgumentParser(description='Convert test samples to VSM format')
	p.add_argument('model', help='dir with model')
	p.add_argument('file', help='file with test samples')
	p.add_argument("--exe", help="exec given Python file")
	args = p.parse_args()

	if args.exe: exec(file.read(open(args.exe)))
	prepare(args.model, args.file)

if __name__ == "__main__": main()

