from pathlib import Path
from ..src.Main import main

import unittest

"""
Tests main() with some different tests than the given example.
"""
class MainTest(unittest.TestCase):

	"""
	Adds the parent dir before each test
	"""
	def setUp(self):
		self.parent_dir = Path(__file__).parent.absolute()

	"""
	A helper function which isolates filenames to keep the actual tests 
	readable

	@param test_name - the desired file name before "_input"/"_output"
	"""
	def run_main(self, test_name):
		input_file  = str(self.parent_dir.joinpath(test_name + "_input.txt"))
		output_file = str(self.parent_dir.joinpath(test_name + "_output.txt"))
		main([input_file, output_file])
		return output_file

	"""
	Tests the test1_input.txt file, which tests lots of sentences, punctuation,
	and capital letters.
	"""
	def test1(self):
		output_file = self.run_main("test1")

		concordance  = "a." + "\t" + "all"   + "\t{1:4}\n"
		concordance += "b." + "\t" + "let's" + "\t{1:1}\n"
		concordance += "c." + "\t" + "of"    + "\t{1:5}\n"
		concordance += "d." + "\t" + "test"  + "\t{1:2}\n"
		concordance += "e." + "\t" + "these" + "\t{1:6}\n"
		concordance += "f." + "\t" + "with"  + "\t{1:3}\n"
		
		with open(output_file, "r") as o_f:
			self.assertEqual(concordance, o_f.read())

	"""
	Tests the test2_input file, which tests tab and newline characters.
	"""
	def test2(self):
		output_file = self.run_main("test2")

		concordance  = "a." + "\t" + "and"        + "\t{1:2}\n"
		concordance += "b." + "\t" + "characters" + "\t{1:2}\n"
		concordance += "c." + "\t" + "need"       + "\t{1:1}\n"
		concordance += "d." + "\t" + "newline"    + "\t{1:2}\n"
		concordance += "e." + "\t" + "tab"        + "\t{1:2}\n"
		concordance += "f." + "\t" + "test"       + "\t{1:1}\n"
		concordance += "g." + "\t" + "to"         + "\t{1:1}\n"
		
		with open(output_file, "r") as o_f:
			self.assertEqual(concordance, o_f.read())

	"""
	Tests the test3_input file, which tests acronyms along with many copies
	of the same (or nearly the same) word
	"""
	def test3(self):
		output_file = self.run_main("test3")

		concordance  = "a." + "\t" + "t.e.s.t." + "\t{1:1}\n"
		concordance += "b." + "\t" + "test"     + "\t{8:1,1,1,2,3,4,4,4}\n"
		concordance += "c." + "\t" + "testtest" + "\t{1:1}\n"
		concordance += "d." + "\t" + "testy"    + "\t{1:4}\n"
		
		with open(output_file, "r") as o_f:
			self.assertEqual(concordance, o_f.read())

if __name__ == '__main__':
    unittest.main()