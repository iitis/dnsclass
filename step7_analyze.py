#!/usr/bin/env python
# Author: Paweł Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2013 IITiS PAN Gliwice
# Licensed under GNU GPL v3 (see the LICENSE file)

import re
from libshorttext import classifier as lst_class
from libshorttext import analyzer as lst_anl
import tokenizer
import argparse

class Buf():
	def __init__(self): self.buf = ""
	def write(self, s): self.buf += s
	def close(self): return
	def clear(self): self.buf = ""
	def __str__(self): return self.buf
	def __repr__(self): return repr(self.buf)
	def sub(self, p, t): self.buf = re.sub(p, t, self.buf)
	def save(self, path):
		f = open(path, "w")
		f.write(self.buf)
		f.close()

# based on libshorttext code
def analyze(outdir, path):
	mpath = outdir + "/model"
	pref = re.sub('\.[^.]+$', '', path)
	respath = pref + ".res"
	cmpath  = pref + ".matrix"
	errpath = pref + ".errors"

	print "loading model from %s" % mpath
	m = lst_class.TextModel(mpath)
	m.text_converter.text_prep.tokenizer = tokenizer.tokenizer

	print "loading results from %s" % respath
	insts = lst_anl.InstanceSet(respath)
	an = lst_anl.Analyzer(m)
	buf = Buf()

	print "saving confusion matrix to %s" % cmpath
	an.gen_confusion_table(insts, buf)
	buf.sub('[ ]+', '\t')
	print buf
	buf.save(cmpath)
	buf.clear()
		
	print "writing detailed error analysis to %s" % errpath
	wr = insts.select(lst_anl.wrong)
	wr.load_text()
	
	err = 0
	for w in wr:
		err += 1

		buf.write(w.true_y + "\t" + w.text + "\t" + w.predicted_y + "\n")

		w.true_y = None # libshorttext hack
		try:
			an.analyze_single(w, 3, buf)
			buf.write("\n")
		except Exception as e:
			buf.write("libshorttext error: " + e.message + "\n")
	buf.save(errpath)
	
	print "total %d errors" % err

def main():
	p = argparse.ArgumentParser(description='Analyze predict results')
	p.add_argument('model', help='dir with model')
	p.add_argument('file', help='file with test samples')
	p.add_argument("--exe", help="exec given Python file")
	args = p.parse_args()
	
	if args.exe: exec(file.read(open(args.exe)))
	analyze(args.model, args.file)

if __name__ == "__main__": main()

