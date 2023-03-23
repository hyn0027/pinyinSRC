from utils.file import *
from utils.log import *
from multiprocessing import Pool, Manager

def loadSinaCorpus(args, logger):
    import glob
    sinaCorpus = []
    fileList = glob.glob(args.sina_news + "/2016*.txt")
    with Pool(processes=args.max_process) as pool:
        dataList = pool.map(readJsonStrings, fileList)
        for i in range(len(dataList)):
            data = dataList[i]
            if (data != False):
                logger.info("successfully load %d sentences from %s", len(data), fileList[i])
            else:
                logger.error("failed to read valid json from file %s", fileList[i])
                exit(-1)
            sinaCorpus += data
    for i in range(len(sinaCorpus)):
        sinaCorpus[i] = sinaCorpus[i]["html"]
    logger.info("loading finished, %d sentences ready from Sina News Corpus", len(sinaCorpus))
    return sinaCorpus

def processList(corpus, wordSet, processID, total, processCnt, lock, interval):
    logger = getLogger("INFO", "computing corpus process " + str(processID))
    wordFreq = dict()
    cnt = 0
    for snt in corpus:
        for i in range(1, len(snt)):
            if snt[i - 1] in wordSet and snt[i] in wordSet:
                if snt[i - 1: i + 1] in wordFreq:
                    wordFreq[snt[i - 1: i + 1]] += 1
                else:
                    wordFreq[snt[i - 1: i + 1]] = 1
        cnt += 1
        if cnt % interval == 0:
            with lock:
                processCnt.value += cnt
                logger.info("processed %d / %d sentences", processCnt.value, total)
                cnt = 0
    if cnt != 0:
        with lock:
            processCnt.value += cnt
            logger.info("processed %d / %d sentences", processCnt.value, total)
            cnt = 0
    return wordFreq

def process(args, corpus, wordSet, logger, corpusName):
    processingArg = []
    segment = []
    manager = Manager()
    processCnt = manager.Value('d', 0)
    lock = manager.Lock()
    batchSize = min(args.max_batch_size, int(len(corpus) / args.max_process) + 1)
    for i in range(int(len(corpus) / batchSize) + 1):
        l = i * batchSize
        r = min(len(corpus), l + batchSize)
        processingArg.append((corpus[l:r], wordSet, i, len(corpus), processCnt, lock, args.report_interval))
        segment.append([l, r])
    wordFreq = dict()
    with Pool(processes=args.max_process) as pool:
        dataList = pool.starmap(processList, processingArg)
        logger.info("All %d sentences in %s successfully processed", len(corpus), corpusName)
        for i in range(len(dataList)):
            data = dataList[i]
            for key in data:
                if key in wordFreq:
                    wordFreq[key] += data[key]
                else:
                    wordFreq[key] = data[key]
        logger.info("All data from %s cleaned", corpusName)
    return wordFreq

def trainOnCorpus(args, wordSet):
    logger = getLogger(args, "corpus")
    wordFreq = readJsonFile(args.word_freq, encoding="utf8")
    if (args.sina_news):
        sinaCorpus = loadSinaCorpus(args, logger)
        corpusName = "sinaNews"
        deltaFreq = process(args, sinaCorpus, wordSet, logger, corpusName)
        for key in deltaFreq:
            if key in wordFreq:
                wordFreq[key] += deltaFreq[key]
            else:
                wordFreq[key] = deltaFreq[key]
        logger.info("All data from %s integrated with loaded frequency", corpusName)
    return wordFreq
        