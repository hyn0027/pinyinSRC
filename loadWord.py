from utils.file import *
from utils.log import *

def loadPronounciation(args, wordSet, logger):
    pronounciations = readFile(args.pronounciation)
    pronounceDict = dict()
    for pronounciation in pronounciations:
        pronounciation = str.split(pronounciation)
        pronounce = pronounciation[0]
        refWord = set()
        for i in range(1, len(pronounciation)):
            if pronounciation[i] in wordSet:
                refWord.add(pronounciation[i])
        if len(refWord) > 0:
            pronounceDict[pronounce] = refWord
    logger.info("load %d pronounciations in total from %s", len(pronounceDict), args.pronounciation)
    return pronounceDict

def loadWords(args, logger):
    words = readFile(args.word_list)
    wordSet = set()
    for word in words[0]:
        wordSet.add(word)
    logger.info("load %d words in total from %s", len(wordSet), args.word_list)
    return wordSet

def loadWordList(args):
    logger = getLogger(args=args, name="loadWord")
    wordSet = loadWords(args, logger)
    pronounceDict = loadPronounciation(args, wordSet, logger)
    return wordSet, pronounceDict