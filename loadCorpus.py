from utils.file import *
from utils.log import *
from multiprocessing import Pool, Manager, cpu_count
from collections import Counter

def loadSinaCorpus(args, logger):
    import glob
    sinaCorpus = []
    fileList = glob.glob(args.sina_news + "/2016*.txt")
    with Pool(processes=min(args.max_process, cpu_count())) as pool:
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

def loadSmpCorpus(args, logger):
    import glob
    smpCorpus = []
    fileList = glob.glob(args.smp + "/"+ "*.txt")
    with Pool(processes=min(args.max_process, cpu_count())) as pool:
        dataList = pool.map(readJsonStrings, fileList)
        for i in range(len(dataList)):
            data = dataList[i]
            if (data != False):
                logger.info("successfully load %d sentences from %s", len(data), fileList[i])
            else:
                logger.error("failed to read valid json from file %s", fileList[i])
                exit(-1)
            smpCorpus += data
    for i in range(len(smpCorpus)):
        smpCorpus[i] = smpCorpus[i]["content"]
    logger.info("loading finished, %d sentences ready from SMP Corpus", len(smpCorpus))
    return smpCorpus

def loadWikiCorpus(args, logger):
    import glob
    wikiCorpus = []
    fileList = glob.glob(args.wiki + "/"+ "*" + "/wiki*")
    processingArg = []
    for item in fileList:
        processingArg.append((item, "utf8"))
    with Pool(processes=min(args.max_process, cpu_count())) as pool:
        dataList = pool.starmap(readJsonStrings, processingArg)
        for i in range(len(dataList)):
            data = dataList[i]
            if (data != False):
                logger.info("successfully load %d sentences from %s", len(data), fileList[i])
            else:
                logger.error("failed to read valid json from file %s", fileList[i])
                exit(-1)
            wikiCorpus += data
    for i in range(len(wikiCorpus)):
        wikiCorpus[i] = wikiCorpus[i]["text"]
    logger.info("loading finished, %d sentences ready from wiki-zh Corpus", len(wikiCorpus))
    return wikiCorpus

def processList(args, corpus, wordSet, processID, total, processCnt, lock, interval):
    logger = getLogger("INFO", "computing corpus process " + str(processID))
    wordFreq = dict()
    cnt = 0
    for snt in corpus:
        for character in snt:
            if character in wordSet:
                if character in wordFreq:
                    wordFreq[character] += 1
                else:
                    wordFreq[character] = 1
        for i in range(1, len(snt)):
            if snt[i - 1] in wordSet and snt[i] in wordSet:
                if snt[i - 1: i + 1] in wordFreq:
                    wordFreq[snt[i - 1: i + 1]] += 1
                else:
                    wordFreq[snt[i - 1: i + 1]] = 1
        if args.infer_num == 3:
            for i in range(2, len(snt)):
                if snt[i - 2] in wordSet and snt[i - 1] in wordSet and snt[i] in wordSet:
                    if snt[i - 2: i + 1] in wordFreq:
                        wordFreq[snt[i - 2: i + 1]] += 1
                    else:
                        wordFreq[snt[i - 2: i + 1]] = 1
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

def process(args, corpus, wordSet, logger):
    processingArg = []
    segment = []
    manager = Manager()
    processCnt = manager.Value('d', 0)
    lock = manager.Lock()
    batchSize = min(args.max_batch_size, int(len(corpus) / args.max_process) + 1)
    for i in range(int(len(corpus) / batchSize) + 1):
        l = i * batchSize
        r = min(len(corpus), l + batchSize)
        processingArg.append((args, corpus[l:r], wordSet, i, len(corpus), processCnt, lock, args.report_interval))
        segment.append([l, r])
    wordFreq = dict()
    with Pool(processes=min(args.max_process, cpu_count())) as pool:
        dataList = pool.starmap(processList, processingArg)
        logger.info("All %d sentences successfully processed", len(corpus))
        logger.info("Start integrating processes...")
        for i in range(len(dataList)):
            data = Counter(dataList[i])
            wordFreq = dict(Counter(wordFreq) + data)
            logger.info("process %d integrated", i)
        logger.info("All data cleaned")
    return wordFreq

def trainOnCorpus(args, wordSet):
    logger = getLogger(args, "corpus")
    wordFreq = readJsonFile(args.word_freq, encoding="utf8")
    logger.info("successfully loaded %d entries from %s", len(wordFreq), args.word_freq)
    corpus = []
    if args.sina_news:
        corpus += loadSinaCorpus(args, logger)
    if args.smp:
        corpus += loadSmpCorpus(args, logger)
    if args.wiki:
        corpus += loadWikiCorpus(args, logger)
    if len(corpus) > 0:
        logger.info("%d sentences in total", len(corpus))
        deltaFreq = process(args, corpus, wordSet, logger)
        if len(wordFreq) == 0:
            wordFreq = deltaFreq
        else:
            logger.info("start integrating")
            log = getLogger(args, "integrateTqdm", False)
            log.addHandler(TqdmLoggingHandler())
            for key, i in zip(deltaFreq, tqdm.tqdm(range(len(deltaFreq)))):
                if key in wordFreq:
                    wordFreq[key] += deltaFreq[key]
                else:
                    wordFreq[key] = deltaFreq[key]
        logger.info("All data integrated with loaded frequency")
    writeJsonFile(args.word_freq, wordFreq, encoding="utf8")
    logger.info("successfully writed %d entries to word frequency file", len(wordFreq))