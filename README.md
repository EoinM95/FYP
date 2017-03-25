# FYP
Final year project. Automatic summary generator

Compares the efficacy of a multi-layer perceptron neural net and a naive bayesian classifier for summarisation as ML research.
Use the install script to obtain all the required dependecies.
Main program is in main.py.

Users can select either the NN or NB based summariser and then begin summarising documents.

Both models have been trained on a corpus of reference extractive summaries of news articles 
and so these systems will be most effective when summarising other news articles. 

Documents to be summarised are expected to be in XML format and have the following structure:
```xml
<DOC>
<HEAD>Doc title</HEAD> ***HL, H3 or HEADLINE tags also accepted
<TEXT>
  Doc body.
</TEXT>
</DOC>
```
******
***Warning***
Requires a word2vec vector list to run
These can be downloaded from [here](https://code.google.com/archive/p/word2vec/)
******

***Warning***
I cannot include the training and test data used as it is taken from the DUC 2001 corpus.
To request the use of this data check [here](www-nlpir.nist.gov/projects/duc/data.html)
******
***Warning***
Requires 64bit Python
*******
