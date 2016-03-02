import xml.etree.ElementTree as ET
import os


class Annotation:

	def __init__(self):
		""" """
		files = os.listdir('/Users/b3j90/Downloads/MAE_v0.9.6/rulesAnnotated')
		self.condicionamientosGeneralesAnotados = []
		for f in files:
			if (f.startswith('1') or f.startswith('2')):
				print("Processing %s" % f.split(".")[0])
				self.loadDeontic(f)

	def loadDeontic(self, f):
		""" """

		tree = ET.parse('/Users/b3j90/Downloads/MAE_v0.9.6/rulesAnnotated/' + f)
		root = tree.getroot()
		cache = []
		name = f.split(".")[0]

		obligations = root.findall('./TAGS/obligation')
		for obligation in obligations:
			if obligation.attrib["text"] not in cache:
				self.condicionamientosGeneralesAnotados.\
					append((obligation.attrib["text"], "p", name))
				cache.append(obligation.attrib["text"])

		permissions = root.findall('./TAGS/permission')
		for permission in permissions:
			if permission.attrib["text"] not in cache:
				self.condicionamientosGeneralesAnotados.\
					append((permission.attrib["text"], "p", name))
				cache.append(permission.attrib["text"])

		prohibitions = root.findall('./TAGS/prohibition')
		for prohibition in prohibitions:
			if prohibition.attrib["text"] not in cache:
				self.condicionamientosGeneralesAnotados.\
					append((prohibition.attrib["text"], "f", name))
				cache.append(prohibition.attrib["text"])

		propositions = root.findall('./TAGS/proposition')
		for proposition in propositions:
			if proposition.attrib["text"] not in cache:
				self.condicionamientosGeneralesAnotados.\
					append((proposition.attrib["text"], "p", name))
				cache.append(proposition.attrib["text"])


	def getcondicionamientosGeneralesAnotados(self):
		""" """
		return self.condicionamientosGeneralesAnotados

	def getcondicionamientosGeneralesAnotadosVectors(self):
		""" """
		sentences = []
		deonticTags = []

		for annotation in self.condicionamientosGeneralesAnotados:
			sentences.append(annotation[0])
			deonticTags.append(annotation[1])

		return sentences, deonticTags



