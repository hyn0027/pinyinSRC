from utils.file import *
from utils.log import *
from utils.multiProcess import threadWithReturnValue

def loadSinaCorpus(args, logger):
    import glob
    sinaCorpus = []
    loadingThread = []
    for file in glob.glob(args.sina_news + "/2016*.txt"):
        thread = threadWithReturnValue(target=readJsonStrings, args=(file,))
        thread.start()
        loadingThread.append({"thread": thread, "file": file})
    for thread in loadingThread:
        data = thread["thread"].join()
        if (data != False):
            logger.info("successfully load %d sentences from %s", len(data), thread["file"])
        else:
            logger.error("failed to read valid json from file %s", thread["file"])
            exit(-1)
        sinaCorpus += data
    logger.info("loading finished, %d sentences in total from Sina News Corpus", len(sinaCorpus))
    for i in range(len(sinaCorpus)):
        sinaCorpus[i] = sinaCorpus[i]["html"]
    logger.info("preprocessing finished, %d sentences ready from Sina News Corpus", len(sinaCorpus))
    return sinaCorpus

def processList(corpus, wordSet):
    wordFreq = dict()
    for snt in corpus:
        for i in range(1, len(snt)):
            if snt[i - 1] in wordSet and snt[i] in wordSet:
                if snt[i - 1: i + 1] in wordFreq:
                    wordFreq[snt[i - 1: i + 1]] += 1
                else:
                    wordFreq[snt[i - 1: i + 1]] = 1
    return wordFreq

def trainOnCorpus(args, wordSet):
    logger = getLogger(args, "corpus")
    wordFreq = readJsonFile(args.word_freq, encoding="utf8")
    if (args.sina_news):
        sinaCorpus = loadSinaCorpus(args, logger)
        