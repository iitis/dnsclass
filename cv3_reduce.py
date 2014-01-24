#!/usr/bin/env python
# Author: Paweł Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2013 IITiS PAN Gliwice
# Licensed under GNU GPL v3 (see the LICENSE file)

import sys
import argparse

def readcm(path):
	l = open(path).readlines()

	tags = map(rewrite, l[0].split())
	ret = {}
	for tag in tags:
		ret[tag] = dict.fromkeys(tags, 0)

	for k_gt,line in zip(tags, l[1:]):
		vals = line.split()[1:]
		for k_res,v in zip(tags, vals):
			ret[k_gt][k_res] += float(v)

	return ret

def reducecm(cm1, cm2):
	ret = {}
	tags = cm1.keys()

	for t1 in tags:
		ret[t1] = {}
		for t2 in tags:
			ret[t1][t2] = cm1[t1][t2] + cm2[t1][t2]

	return ret

def dometrics(cm):
	ret = {}
	num = {}
	tp = {}
	fp = {}

	tags = cm.keys()
	total = sum([sum(row.values()) for row in cm.values()])

	for t1 in tags:
		ret[t1] = {}
		if t1 not in num: num[t1] = 0
		if t1 not in tp: tp[t1] = 0
		if t1 not in fp: fp[t1] = 0

		num[t1] = sum(cm[t1].values())
		tp[t1] = cm[t1][t1]
		fp[t1] = sum([v[t1] for k,v in cm.iteritems() if k != t1])

		ret[t1]["~1%TP"] = tp[t1] / num[t1] * 100.0
		ret[t1]["~2%FP"] = fp[t1] / (total - num[t1]) * 100.0

#		print "%s: tp=%.2f fp=%.2f" % (t1, ret[t1]["%TP"], ret[t1]["%FP"])

		for t2 in tags:
			ret[t1][t2] = cm[t1][t2] / num[t1] * 100.0

	return ret

def average(m1, m2):
	ret = {}

	for t1 in m1.keys():
		ret[t1] = {}
		for t2 in m1[t1].keys():
			ret[t1][t2] = (m1[t1][t2] + m2[t1][t2]) / 2.0

	return ret

def tostr(pair):
	k, res = pair

	if res == 100.0:
		return "100.0%"
	elif res == 0.0:
		if k == "~2%FP":
			return "0.0%"
		else:
			return " "

	ret = "{:.1f}%".format(res)
	if ret == "100.0%":
		return "99.9%"
	elif ret == "0.0%":
		return "<0.1%"
	else:
		return ret

def rewrite(colname):
	d = {
		"BitTorrent": "Torrent",
		"FlashPlayer": "FPlayer",
		"Kaspersky": "Kasp.",
		"Shoutcast": "Shcast"
	}

	if colname in d:
		return d[colname]
	else:
		return colname

def rewrite2(colname):
	d = {
		"~1%TP": "%TP",
		"~2%FP": "%FP"
	}

	if colname in d:
		return d[colname]
	else:
		return colname

def connect(files):
	cms = map(readcm, files)
	res1 = reduce(reducecm, cms)

	metrics = map(dometrics, cms)
	res2 = reduce(average, metrics)

	### approach 1
	# print labels
	tags = sorted(res1.keys())
	print "\t".join([" "*10] + ["Flows"] + [x[0:7] for x in tags])

	for k in tags:
		vals = [str(int(x[1])) for x in sorted(res1[k].iteritems())]
		vals.insert(0, str(int(sum(res1[k].values()))))
		print "%-10s\t%s" % (k, "\t".join(vals))

	### approach 2
	# print labels
	cols = sorted(res2[res2.keys()[0]].keys())
	print "\t".join([" "*10] + map(rewrite2, cols))

	for p in sorted(res2.keys()):
		vals = map(tostr, sorted(res2[p].iteritems()))
		print "%-10s\t%s" % (p, "\t".join(vals))

	# averages
	num_p = float(len(res2.keys()))
	avg_tp = sum([row["~1%TP"] for p,row in res2.iteritems()]) / num_p
	avg_fp = sum([row["~2%FP"] for p,row in res2.iteritems()]) / num_p
	l = [("~1%TP", avg_tp), ("~2%FP", avg_fp)]
	print "\t".join([" "]*(len(cols)-2) + ["Average:"] + map(tostr, l))

def main():
	p = argparse.ArgumentParser(description='Connect several confusion matrices')
	p.add_argument('files', metavar='FILE', type=str, nargs='+',
		help='path to files with confusion matrices')

	args = p.parse_args()
	connect(args.files)

if __name__ == "__main__": main()
