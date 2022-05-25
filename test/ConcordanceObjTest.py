from ..src.Main import ConcordanceObj

import unittest

"""
Tests the ConcordanceObj in Main.
"""
class TestConcordanceObj(unittest.TestCase):

	"""
	Initializes an empty ConcordanceObj() before each test
	"""
	def setUp(self):
		self.concordance = ConcordanceObj()

	"""
	Tests the add_word functionality. First adds a word multiple times to test
	how it would look in a concordance, then adds an acronym, and finally a
	very long word.
	"""
	def test_add_word(self):
		self.concordance.add_word("words", [1])
		self.concordance.add_word("words", [3, 3])
		result = "a.\twords\t{3:1,3,3}"
		self.assertEqual(self.concordance.word_as_entry(0, "words"), result)
		result = "aa.\twords\t{3:1,3,3}"
		self.assertEqual(self.concordance.word_as_entry(26, "words"), result)
		# Adding 2 later means numbers are out of order. The sentences are
		# looped in order, so this shouldn't matter. But this is the behavior.
		self.concordance.add_word("words", [2])
		result = "b.\twords\t{4:1,3,3,2}"
		self.assertEqual(self.concordance.word_as_entry(1, "words"), result)
		self.concordance.add_word("e.g.", [1])
		result = "a.\te.g.\t{1:1}"
		self.assertEqual(self.concordance.word_as_entry(0, "e.g."), result)
		long_word = "antidisestablishmentarianism"
		self.concordance.add_word(long_word, [4])
		result = "a.\t" + long_word + "\t{1:4}"
		self.assertEqual(self.concordance.word_as_entry(0, long_word), result)
		result  = "a.\t" + long_word + "\t" + "{1:4}"       + "\n"
		result += "b.\t" + "e.g."    + "\t" + "{1:1}"       + "\n"
		result += "c.\t" + "words"   + "\t" + "{4:1,3,3,2}" + "\n"
		self.assertEqual(str(self.concordance), result)

	"""
	Tests the prefix() function to ensure it works as desired.
	"""
	def test_prefix(self):
		self.assertEqual(self.concordance.prefix(0), "a.")
		self.assertEqual(self.concordance.prefix(26), "aa.")
		# Should never take negative numbers, but noting the behavior
		self.assertEqual(self.concordance.prefix(-1), ".")
		self.assertEqual(self.concordance.prefix(75), "xxx.")

if __name__ == '__main__':
    unittest.main()