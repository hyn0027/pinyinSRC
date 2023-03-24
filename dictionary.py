from utils.file import *
from utils.log import *
import tqdm

YUAN_YIN = {"ā": "a", "á": "a", "ǎ": "a", "à": "a", 
            "ē": "e", "é": "e", "ě": "e", "è": "e",
            "ī": "i", "í": "i", "ǐ": "i", "ì": "i",
            "ō": "o", "ó": "o", "ǒ": "o", "ò": "o",
            "ū": "u", "ú": "u", "ǔ": "u", "ù": "u",
            "ǖ": "v", "ǘ": "v", "ǚ": "v", "ǜ": "v", "ü": "v"}

def transfer(pinyin):
    for i in range(len(pinyin)):
        for key in YUAN_YIN:
            pinyin[i] = pinyin[i].replace(key, YUAN_YIN[key])
        pinyin[i] = pinyin[i].replace("ve", "ue")
    return pinyin

def loadDictionary(args, logger):
    data = readFile(args.dictionary, encoding="utf8")
    while data[0].find("#") != -1:
        data = data[1:]
    for i in range(len(data)):
        data[i] = data[i].replace(":", "").split()
        data[i] = {"word": data[i][0], "pronounciation": transfer(data[i][1:])}
    logger.info("successfully load %d entries from dictionary %s", len(data), args.dictionary)
    return data


def addDictionary(args, wordSet, wordDict):
    logger = getLogger(args, "dictionary")
    dictionary = loadDictionary(args, logger)
    frequency = dict()
    for pronounce in wordDict:
        frequency[pronounce] = dict()
        for word in wordDict[pronounce]:
            frequency[pronounce][word] = 0
    logger.info("begin computing frequency...")
    log = getLogger(args, "dictionaryTqdm", False)
    log.addHandler(TqdmLoggingHandler())
    for idx in tqdm.tqdm(range(len(dictionary))):
        item = dictionary[idx]
        for i in range(len(item["word"])):
            character = item["word"][i]
            pronounce = item["pronounciation"][i]
            if character in wordDict[pronounce]:
                frequency[pronounce][character] += 1
    logger.info("begin writing to file")
    writeJsonFile(args.word_freq + "/pronounce.txt", frequency, encoding="utf8")
    logger.info("successfully write frequency to file %s", args.word_freq + "/pronounce.txt")
