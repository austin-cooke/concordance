from ..src.Main import Regexer

import unittest

"""
Tests the Regexer class in Main
"""
class TestRegexer(unittest.TestCase):

	"""
	Tests cleaning the count list
	"""
	def test_clean_count_lists(self):
		self.assertEqual(Regexer.clean_count_list([1,2]), "1,2")
		# Should never use anything except positive integers, just showing 
		# behavior.
		self.assertEqual(Regexer.clean_count_list(['a',-1]), "'a',-1")

	"""
	Tests cleaning words, like acronyms, numbers, parentheticals, and words 
	with hyphens.
	"""
	def test_clean_word(self):
		self.assertEqual(Regexer.clean_word("i.e."),      "i.e.")
		self.assertEqual(Regexer.clean_word("yes"),       "yes")
		self.assertEqual(Regexer.clean_word("Yes."),      "yes")
		self.assertEqual(Regexer.clean_word("1."),        "1")
		self.assertEqual(Regexer.clean_word("hi)."),      "hi")
		self.assertEqual(Regexer.clean_word("year-end."), "year-end")

	"""
	Tests grabbing sentences out of the text file. Ensures that acronyms 
	aren't ignored, punctuation is preserved (cleaned later in code), and
	the sentences are padded with a space.
	"""
	def test_get_sentences_from_text(self):
		s1_str =  "This should be two sentences. In total. "
		s1_arr = [" This should be two sentences. ",
				  " In total. "]
		self.assertEqual(Regexer.get_sentences_from_text(s1_str), s1_arr)
		s2_str =  "What if I include an acronym? Like e.g. for example! "
		s2_arr = [" What if I include an acronym? ", 
		          " Like e.g. for example! "]
		self.assertEqual(Regexer.get_sentences_from_text(s2_str), s2_arr)

if __name__ == '__main__':
    unittest.main()