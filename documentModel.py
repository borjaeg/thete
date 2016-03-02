# -*- coding: utf-8 -*-
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
import numpy as np
from annotation import Annotation


class DocumentModel:
	""" """	

	def proportion(self,prop, train_y):
		if len(np.array(train_y)[np.array(train_y) == 'f']) / (len(np.array(train_y)[np.array(train_y) == 'p']) * 1.0) < prop:
			return False
		else:
			return True

	def oversample(self,sentence, annotation, prop):
		train = sentence[:]
		train_y = annotation[:]
		while not self.proportion(prop, train_y):
			for i in range(1, len(sentence)):
				if annotation[i] == 'f':
					train.append(sentence[i])
					train_y.append('f')

		return train, train_y

	def undersample(self,sentence, annotation, prop):
		train = sentence[:]
		train_y = annotation[:]
		while not self.proportion(prop, train_y):
			removed = False
			for i in range(1, len(train_y)-1):
				if train_y[i] == 'p' and removed == False:
					train.pop(i)
					train_y.pop(i)
					removed = True

		return train, train_y


	def get_sentences(self, cs):
		""" """
		sentence, annotation = \
			Annotation().getcondicionamientosGeneralesAnotadosVectors()

		self.X_train = sentence	

		y = []
		for target in annotation:
			if target=='o':
				y.append(0)
			elif target == 'f':
				y.append(1)
			elif target == 'p':
				y.append(0)
			elif target == 'pr':
				y.append(0)
			else:
				print('Unknown target value')
				raise # Unkown

		result = {}
		result["data"] = self.X_train
		result["target"] = np.array(y)

		return result

	def balancedDatasetTest(target): # Modify
		""" """
		
		target = np.array(target)
		print((target == 0).sum(), (target == 1).sum())
