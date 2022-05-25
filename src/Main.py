import platform
import re
import sys

from pathlib import Path

"""
main() has all functionality. It first pulls arguments from the system and 
reads the input files. Then, using regexes, it pulls the sentences from the 
text and loops through them. The second loop runs through a list(set()) of
the words in each sentence, finds all instances in each sentence, and adds
them to a concordance object. Finally, the concordance is written to a file.

@param argv - The system arguments as an array
"""
def main(argv):
	(input_file, output_file) = handle_arguments(argv)

	with open(input_file, "r") as f:
		text_all = f.read()

	sentences   = Regexer.get_sentences_from_text(text_all)
	concordance = ConcordanceObj()
	for i in range(0, len(sentences)):
		# list(set()) removes duplicates
		for word in list(set(sentences[i].split())):
			# Pads words and sentences so regexes complete properly
			count = len(re.findall(' ' + word + ' ', sentences[i]))
			if count > 0:
				concordance.add_word(Regexer.clean_word(word), [i+1] * count)

	with open(output_file, "w+") as f:
		f.write(str(concordance))

	print("Success!")

"""
Handles input and output file arguments. If an input and output file are both
specified, they are used. If not, default files are used. Otherwise, it is
considered an error and the system exits.

@param argv - an array of input files
@returns input and output files
"""
def handle_arguments(argv):
	# Put this here in case versioning creates issues
	print("Python version: " + platform.python_version())
	parent_dir  = Path(__file__).parent.absolute()
	input_file  = str(parent_dir.joinpath('input.txt'))
	output_file = str(parent_dir.joinpath('output.txt'))
	if len(argv) == 2:
		input_file  = argv[0]
		output_file = argv[1]
	elif len(argv) == 0:
		print("Using default input file: '"  + input_file  + "'")
		print("Using default output file: '" + output_file + "'")
	else:
		print("Invalid Input: accepted arguments below")
		cmd = "python -m arista.src.Main"
		print("To use custom files: "  + cmd + " $INPUT_FILE $OUTPUT_FILE")
		print("To use default files: " + cmd)
		sys.exit(1)
	return (input_file, output_file)

"""
The Regexer class performs all regex operations. It isn't used as an object,
but is instead called statically whenever needed.
"""
class Regexer():

	"""
	Cleans count lists for concordance. Very simple regex for list types

	@param list_to_clean - list which needs only positive integers for 
						   expected behavior.
	@returns the list as a string
	"""
	def clean_count_list(list_to_clean):
		cleaned = re.sub(r'[\[|\]| ]', r'', str(list_to_clean))
		return cleaned

	"""
	Cleans words which are passed. Only used when adding to the concordance
	so that words don't contain punctuation. However, not to be used when 
	searching sentences (or else more pre-processing would be necessary). 
	Removes end punctuation *unless* an acronym is passed. 

	@param word_to_clean - a word which may have punctuation
	@returns a word with punctuation removed (except acronyms)
	"""
	def clean_word(word_to_clean):
		word_to_clean = str.lower(word_to_clean)
		# Captures acronyms. Non-capturing group "?:" is used so that the 
		# acronym isn't split. Quantifier uses 2 so that "a.a." will be captured
		# but not "a." (which would be poor grammar but not an acronym)
		match = re.fullmatch(r'(?:[a-zA-Z]\.){2,}', word_to_clean)
		if (match is not None):
			return word_to_clean
		else:
			# Grabs punctuation at end of word, and any amount of it like ")."
			return re.sub(r'\W+\Z', r'', word_to_clean)

	"""
	Pulls individual sentences from the passed text string. Crawls to first
	instance of punctuation not including acronyms. That sentence is added
	to an array, and the next loops begins, finally returning an array of
	sentences padded with spaces.

	@param text_to_clean - Full text as a string
	@returns an array of sentences padded with spaces
	"""
	def get_sentences_from_text(text_to_clean):
		# pads text and replaces special characters with spaces
		new_text = ' ' + text_to_clean + ' '
		new_text = re.sub(r'\n+|\t+', r' ', new_text)
		# matches space, letter(s), optional apostrophe, letter(s),
		# end punctuation (can be multiple), space (the end of a sentence)
		sentence_regex = r' [a-zA-Z]+[\']?[a-z]*[.?!]+ '
		match = re.search(sentence_regex, new_text)
		sentences = []
		while (match):
			# pulls first sentence, add to array. Removes from new_text
			sentences +=      [new_text[0:match.end()]]
			# pads beginning of new_text just like above padding
			new_text   = ' ' + new_text  [match.end():]
			match = re.search(sentence_regex, new_text)
		return sentences

"""
The ConcordanceObj is a class which holds all of the cleaned information after
each word has been grabbed individually. Makes writing to file very easy.
"""
class ConcordanceObj():

	"""
	Initializes values such as the word dictionary and useful constants
	"""
	def __init__(self):
		self.word_dict = {}
		# added these for readability
		self.ALPH_LENGTH   = 26
		self.UNICODE_START = 97

	"""
	Adds a word to the dictionary with associated position list

	@param new_word - word to be added
	@param pos_list - list of integers denoting sentence positions
	"""
	def add_word(self, new_word, pos_list):
		if new_word not in self.word_dict:
			self.word_dict[new_word] = []
		self.word_dict[new_word] += pos_list

	"""
	Creates individual lines in the concordance. Usually only called inside the
	class by the str() function.

	@param concordance_pos - the number in order to be printed
	@param word - the word itself
	@returns the word in the entry format shown in the concordance
	"""
	def word_as_entry(self, concordance_pos, word):
		pfix = self.prefix(concordance_pos)
		count_list = self.word_dict[word]
		count_str = str(len(self.word_dict[word]))
		label = Regexer.clean_count_list(count_list)
		# Won't render the same everywhere, but not in requirements
		return pfix + "\t" + word + "\t" + '{' + count_str + ':' + label + '}'

	"""
	Creates the prefix, or the "a."/"aa." part of the concordance. Uses unicode
	to find letters

	@param count - the order or number in the concordance
	@returns a short string, such as "aa."
	"""
	def prefix(self, count):
		# modulus on letters in alphabet, get lowercase unicode letter
		alphabet_position = (count %  self.ALPH_LENGTH) + self.UNICODE_START
		# // in Python 3 skips remainder
		alphabet_repeat   = (count // self.ALPH_LENGTH) + 1
		return chr(alphabet_position) * alphabet_repeat + "."

	"""
	Returns this object as a string. Overrides built-in str() method. First
	it sorts the dictionary keys, then calls word_as_entry in a loop and 
	returns.

	@returns the concordance in its final format
	"""
	def __str__(self):
		# sorts on lowercase letters
		sorted_keys = sorted(self.word_dict.keys(), key=str.lower)
		ret = ""
		for i in range(0, len(sorted_keys)):
			ret += self.word_as_entry(i, sorted_keys[i]) + "\n"
		return ret

if __name__ == "__main__":
	main(sys.argv[1:])