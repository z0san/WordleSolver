#%%
from functools import cache
import json
from time import time
from unittest import result
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

#%%
# tells you if a word has two of the same letter
def hasDoubleLetter(word):
	for index, letter in enumerate(word[0:-1]):
		if letter in word[index+1:]: return True
	return False;

#%%
# load in word lists
with open('list.json') as json_file:
		data = json.load(json_file)
		# print(data["wordOptions"])

wordOptions = data["wordOptions"]
guessOptions = data["guessOptions"]

#%%
# returns the output of wordle for a given secret words and guess
def wordleResult(secret, guess):
	result = ""
	for letter in range(5):
		if secret[letter] == guess[letter]:
			result += 'g' # g represents green
		elif guess[letter] in secret:
			result += 'y' # y represents yellow
		else:
			result += 'b' # b represents black or blanc
	return result

# print(wordleResult("cigar", "later"))

#%%
# nicely prints the wordle result
def prettyPrintResult(guess, result):
	for  index, letter, in enumerate(guess):
		if (result[index] == 'g'): print(f"{Fore.GREEN}{letter}", end="")
		elif (result[index] == 'y'): print(f"{Fore.YELLOW}{letter}", end="")
		else: print(letter, end="")
	print()


#%%
# will return a list of possible words that it could be
def getPossibleWords(results, guesses, possibleWordList = wordOptions):
	confirmed = ['#', '#', '#', '#', '#']
	denied = [[], [], [], [], []]
	nowhere = []
	somwhere = []

	for guessIndex, result in enumerate(results):
		for letterIndex, color in enumerate(result):
			if color == 'g':
				confirmed[letterIndex] = guesses[guessIndex][letterIndex]
			elif color == 'y':
				denied[letterIndex] += [guesses[guessIndex][letterIndex]]
				somwhere += guesses[guessIndex][letterIndex]
			else:
				nowhere += guesses[guessIndex][letterIndex]

	# we can narrow down the word list
	possibleWordList = [x for x in possibleWordList if
                     len([y for y in nowhere if y in x]) == 0 and
                     len([z for z in somwhere if z in x]) == len(somwhere)]

	possibleWords = []

	# check all possible guesses to get the ones that are possible
	for guess in possibleWordList:
		guessPossible = True
		for letter in range(5):
			# check confirmed letters
			if confirmed[letter] != '#' and guess[letter] != confirmed[letter]:
				guessPossible = False;
				break
			# check denied letters in specific locations
			for deniedLetter in denied[letter]:
				if guess[letter] == deniedLetter:
					guessPossible = False;
					break

		# if all tests pass add letter to possible words
		if guessPossible:
			possibleWords += [guess]

	return possibleWords

#%%
def numToChar(num):
	if num == 0: return 'b'
	elif num == 1: return 'y'
	else: return 'g'

def numToResult(num):
	result = [' ', ' ', ' ', ' ', ' ']
	for i in range (5):
		result[4-i] = numToChar(num % 3)
		num = int(num / 3)


	return "".join(result)

def charToNum(char):
	if char == 'b': return 0
	elif char == 'y': return 1
	else: return 2

def resultToNum(result):
	num = 0;
	for i in result:
		num *= 3
		num += charToNum(i)
	return num

    
#%%
# now we check for current results what is the next best word
def bestNextGuess(results, guesses, guessList = guessOptions, wordList = wordOptions):
	# hard code best first word
	if results == []: return "raise", 61

	bestWordSoFar = "";
	minExpectedPossible = len(wordOptions);
	percentageChecked = -1;
	possibleWords = getPossibleWords(results, guesses, wordList)
	# first check if there is only one possible word
	if len(possibleWords) == 1:
		return possibleWords[0], 1


	for count, possibleGuess in enumerate(guessList):
		# calculate all the possible word lengths for all possible results
		resultLengths = []
		for index in range(3 ** 5):
			resultLengths.append(len(getPossibleWords(results + [numToResult(index)], guesses + [possibleGuess], possibleWords)))

		possibleWordCount = 0
		for possibleSecret in possibleWords:
			possibleWordCount += resultLengths[resultToNum(wordleResult(possibleSecret, possibleGuess))]
		
		# check to see if the expected number of possible words is the minimum so far
		if (possibleWordCount / len(possibleWords) < minExpectedPossible or
				(possibleWordCount / len(possibleWords) == minExpectedPossible and
    		possibleGuess in possibleWords)):
			minExpectedPossible = possibleWordCount / len(possibleWords)
			bestWordSoFar = possibleGuess


		# just a nice percentage checked indicator
		newPercentageChecked = int((count / len(guessList)) * 100)
		if newPercentageChecked != percentageChecked:
			percentageChecked = newPercentageChecked
			print(f"{percentageChecked}%")

	return bestWordSoFar, minExpectedPossible


#%%
# easy entering if you are playing the game
def gameHelper():
	results = []
	guesses = []
	solved = False

	while not solved:
		nextGuess, expectedRemainingWords = bestNextGuess(results, guesses, guessList = wordOptions)
		print(f"please guess: {nextGuess} ({expectedRemainingWords})")
		result = input("solved (Y/n): ")
		result = result.lower()
		solved = result == "y" or result == ""
		if solved: break
		guesses += [nextGuess]
		newResult = input("result: ")
		results += [newResult]
		print(guesses)
		print(results)

gameHelper()