import re

def isAccepableSentence(sentence):
	#print "UTILS"
	if len(sentence) < 15:
		return False

	if sentence[0] == '(':
		return False

	if "030314" in sentence:
		return False

	if not re.match("[A-Z]",sentence[0]):
		return False

	if "Condicionamientos preventivos de riesgos" in sentence:
		return False

	return True

def preCleanSentence(sentence):
	""" """
	sentence = re.sub("P.S.", "PS", re.sub("g.s.a.", "gsa ", re.sub(", \([0-9]+[ -][0-9a-zA-Z/\. ]+.\)[ ]?,", " [cantidad]",re.sub("[Hh][Aa]\.", "Ha", re.sub("R.D.", "RD", re.sub("[Hh][Aa]\.", "Ha", re.sub("[0-9\.]+ semillas", "semillas", sentence)))))))
	sentence = re.sub("# ","", re.sub("#.-","",sentence))

	return sentence

def postCleanSentence(sentence):
	""" """
	if re.match(".*\n\n030314\n\n.*", sentence):
		print "CATCHED"
		if sentence.split('.')[0] == sentence:
			return sentence.split('\n')[0]
		else:
			return sentence.split('.')[0]
	else:
		return sentence


def removeStopWords(sentence):
	sentence = re.sub(",","", re.sub("\n","",re.sub("\.", "",sentence)))
	return sentence
