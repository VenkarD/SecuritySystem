from abc import ABCMeta, abstractmethod

class IFrameAnalyzer:
	__metaclass__ = ABCMeta

	def __init__(self):
		pass

	# на вход принимает numpy.ndarray
	# помимо прочего должен вернуть массив кортежей с координатами областей
	@abstractmethod
	def process(self, frame):
		raise NotImplementedError("You have to implement this method!")
