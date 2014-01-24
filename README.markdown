About
=====

**dnsclass**: open source, reference implementation of the DNS-Class algorithm in Python.

The classifier takes as input ARFF files generated with [the Flowcalc
program](http://mutrics.iitis.pl/flowcalc) (using the `dns` and `lpi` plugins). **dnsclass**
classifies given network traffic flows basing on their DNS context and outputs a classification
report.

The classification process is divided into several steps, into script files named `stepN_*`, e.g.
`step6_predict.py`. There are also scripts named `cvN_*` that support cross-validation.

For scientific works, please cite the following paper:  
> Foremski P., Callegari C., Pagano M., *"DNS-Class: Immediate classification of IP flows using DNS"*

**Author**: Paweł Foremski <pjf@iitis.pl>  
**Copyright (C)** 2012-2013 [IITiS PAN Gliwice](http://www.iitis.pl/)  
**Licensed** under GNU GPL v3

This software package uses [libshorttext](http://www.csie.ntu.edu.tw/~cjlin/libshorttext/), which is
included in the dnsclass repository, but may be licensed differently.

Classifier steps
================

The purpose of the steps:
* `step1_reformat.sh`: reformat input ARFF files into the target text input format; skip all flows
   but those of selected protocols; some corrections may be required to match your ARFF files
* `step2_divide.sh`: divide the dataset into training and testing (may be skipped)
* `step3_convert_train.py`: convert the training dataset into the libsvm format (Vector Space Model (VSM))
* `step4_train.sh`: train the model
* `step5_convert_test.py`: as step 3, but for the testing dataset
* `step6_predict.py`: classify the testing dataset
* `step7_analyze.py`: show the confusion matrix and errors made in step 6

Project information
================
Project realized at [The Institute of Theoretical and Applied Informatics of the Polish Academy of
Sciences](http://www.iitis.pl/), under grant nr 2011/01/N/ST6/07202 of the [Polish National Science
Centre](http://www.ncn.gov.pl/).

Project website: http://mutrics.iitis.pl/
