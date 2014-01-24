#!/usr/bin/env python
# Author: Paweł Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2013 IITiS PAN Gliwice
# Licensed under GNU GPL v3 (see the LICENSE file)

import re
from libshorttext.classifier import learner as lst_learner
from libshorttext import classifier as lst_class
import tokenizer
import argparse
import params as P

# based on libshorttext code
def predict(outdir, path, store):
	mpath = outdir + "/model"
	pref = re.sub('\.[^.]+$', '', path)
	svmpath = pref + ".svm"
	respath = pref + ".res"

	print "loading model from %s" % mpath
	m = lst_class.TextModel(mpath)
	m.text_converter.text_prep.tokenizer = tokenizer.tokenizer

	print "predicting labels in %s" % svmpath
	res, acc, dvs, gt, fcs = lst_learner.predict(svmpath, m.svm_model, '')
	
	# NOTE: values in "decision values" (dvs) are simply the sum of weights
	#       for the features found in given instance BUT feature values are
	#       normalized, e.g. 1.0 -> 0.447214, so the decision value will be
	#       a scaled sum of the weights

	if P.pre.F > 0:
		print "unknown filtering (F=%g, T=%g)" % (P.pre.F, P.pre.T)

		above, above_ok = 0.0, 0.0
		below, below_was_ok, below_ok = 0.0, 0.0, 0.0

		for i in xrange(len(res)):
			dv = max(dvs[i])
			fc = fcs[i]
			if fc >= P.pre.F and dv >= P.pre.T:
				above += 1.0
				if res[i] == gt[i]: above_ok += 1.0
			else: # make it "Unknown"
				below += 1.0
				if res[i] == gt[i]: below_was_ok += 1.0
				res[i] = 0
				if gt[i] == 0: below_ok += 1.0

		total = above + below
		total_ok = above_ok + below_ok
		
		print "above T: %d (%.2f%%), in which accuracy is %.2f%%" % \
			(above, above/total*100.0, above_ok/above*100.0)
		if below > 0:
			print "below T: %d (%.2f%%), in which accuracy was %.2f%% and now is %.2f%%" % \
				(below, below/total*100.0, below_was_ok/below*100.0, below_ok/below*100.0)
	else:
		total = float(len(res))
		total_ok = sum([i == j for i,j in zip(res,gt)])

	print "overall accuracy: %g%%" % (total_ok/total*100.0)
	print "total errors: %d" % (total - total_ok)

	if store:
		print "translating..."
		i2c = m.text_converter.class_map.idx2class
		res = [i2c[int(y)] for y in res]
		gt  = [i2c[int(y)] for y in gt]
		pr = lst_class.PredictionResult(
			path, m._hashcode, gt, res, dvs, svmpath, m.get_labels())

		print "saving to %s" % respath
		pr.save(respath, True)

def main():
	p = argparse.ArgumentParser(description='Predict test samples')
	p.add_argument('model', help='dir with model')
	p.add_argument('file', help='file with test samples')
	p.add_argument('-s','--store', help='store results', action='store_true')
	p.add_argument("--exe", help="exec given Python file")
	args = p.parse_args()
	
	if args.exe: exec(file.read(open(args.exe)))
	predict(args.model, args.file, args.store)

if __name__ == "__main__": main()

