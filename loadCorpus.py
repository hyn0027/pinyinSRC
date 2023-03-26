from utils.file import *
from utils.log import *
from multiprocessing import Pool, Manager, cpu_count
from collections import Counter
from utils.hashString import *
import random

def loadSinaCorpus(args, logger):
    import glob
    sinaCorpus = []
    fileList = glob.glob(args.sina_news + "/2016*.txt")
    with Pool(processes=min(args.max_process, cpu_count())) as pool:
        dataList = pool.map(readJsonStrings, fileList)
        for i in range(len(dataList)):
            data = dataList[i]
            if (data != False):
                logger.info("successfully loaded %d sentences from %s", len(data), fileList[i])
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
                logger.info("successfully loaded %d sentences from %s", len(data), fileList[i])
            else:
                logger.error("failed to read valid json from file %s", fileList[i])
                exit(-1)
            smpCorpus += data
    for i in range(len(smpCorpus)):
        smpCorpus[i] = smpCorpus[i]["content"]
    logger.info("loading finished, %d sentences ready from SMP Corpus", len(smpCorpus))
    return smpCorpus

def loadBaikeCorpus(args, logger):
    import glob
    baikeCorpus = []
    fileList = glob.glob(args.baike + "/"+ "*.json") 
    processingArg = []
    for item in fileList:
        processingArg.append((item, "utf8"))
    with Pool(processes=min(args.max_process, cpu_count())) as pool:
        dataList = pool.starmap(readJsonStrings, processingArg)
        for i in range(len(dataList)):
            data = dataList[i]
            if (data != False):
                logger.info("successfully loaded %d sentences from %s", len(data), fileList[i])
            else:
                logger.error("failed to read valid json from file %s", fileList[i])
                exit(-1)
            baikeCorpus += data
    for i in range(len(baikeCorpus)):
        baikeCorpus[i] = baikeCorpus[i]["desc"] + " " + baikeCorpus[i]["answer"]
    logger.info("loading finished, %d sentences ready from baike Corpus", len(baikeCorpus))
    return baikeCorpus

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
                logger.info("successfully loaded %d sentences from %s", len(data), fileList[i])
            else:
                logger.error("failed to read valid json from file %s", fileList[i])
                exit(-1)
            wikiCorpus += data
    
    if args.only_title:
        for i in range(len(wikiCorpus)):
            wikiCorpus[i] = wikiCorpus[i]["title"]
        logger.info("loading finished, %d sentences ready from wiki-zh Corpus", len(wikiCorpus))
        return wikiCorpus
    title = []
    for i in range(len(wikiCorpus)):
        wikiCorpus[i] = wikiCorpus[i]["text"]
        title.append(wikiCorpus[i]["title"])
    logger.info("loading finished, %d sentences ready from wiki-zh Corpus", len(wikiCorpus))
    return wikiCorpus + title

def processList(args, corpus, wordSet, processID, total, processCnt, lock, interval):
    logger = getLogger("INFO", "computing corpus process " + str(processID))
    wordFreq = []
    for i in range(args.hash_mod):
        wordFreq.append(dict())
    cnt = 0
    for snt in corpus:
        for character in snt:
            if character in wordSet:
                hashRes = hashString(args, character)
                if character in wordFreq[hashRes]:
                    wordFreq[hashRes][character] += 1
                else:
                    wordFreq[hashRes][character] = 1
        for i in range(1, len(snt)):
            if snt[i - 1] in wordSet and snt[i] in wordSet:
                hashRes = hashString(args, snt[i - 1: i + 1])
                if snt[i - 1: i + 1] in wordFreq[hashRes]:
                    wordFreq[hashRes][snt[i - 1: i + 1]] += 1
                else:
                    wordFreq[hashRes][snt[i - 1: i + 1]] = 1
        if args.infer_num == 3:
            for i in range(2, len(snt)):
                if snt[i - 2] in wordSet and snt[i - 1] in wordSet and snt[i] in wordSet:
                    hashRes = hashString(args, snt[i - 2: i + 1])
                    if snt[i - 2: i + 1] in wordFreq[hashRes]:
                        wordFreq[hashRes][snt[i - 2: i + 1]] += 1
                    else:
                        wordFreq[hashRes][snt[i - 2: i + 1]] = 1
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

def integrateWordFreq(args, freqList, num):
    logger = getLogger(args, "integrating" + str(num))
    wordFreq = dict()
    cnt = total = 0
    for data in freqList:
        total += len(data)
    for data in freqList:
        for key in data:
            if key in wordFreq:
                wordFreq[key] += data[key]
            else:
                wordFreq[key] = data[key]
            cnt += 1
            if cnt % (args.report_interval * 100) == 0:
                logger.info("integrated %d / %d entries", cnt, total)
    logger.info("integrated %d / %d entries", cnt, total)
    return wordFreq

def process(args, corpus, wordSet, logger):
    processingArg = []
    segment = []
    manager = Manager()
    processCnt = manager.Value('d', 0)
    lock = manager.Lock()
    batchSize = min(args.max_batch_size, int(len(corpus) / min(args.max_process, cpu_count())) + 1)
    for i in range(int(len(corpus) / batchSize) + 1):
        l = i * batchSize
        r = min(len(corpus), l + batchSize)
        processingArg.append((args, corpus[l:r], wordSet, i, len(corpus), processCnt, lock, args.report_interval))
        segment.append([l, r])
    with Pool(processes=min(args.max_process, cpu_count())) as pool:
        dataList = pool.starmap(processList, processingArg)
        logger.info("All %d sentences successfully processed", len(corpus))
    processingArg = []
    for i in range(args.hash_mod):
        dictList = []
        for j in range(len(dataList)):
            dictList.append(dataList[j][i])
        processingArg.append((args, dictList, i))
    logger.info("Start integrating processes...")

    with Pool(processes=min(args.max_process, cpu_count())) as pool1:
        dataList = pool1.starmap(integrateWordFreq, processingArg)
        logger.info("All data cleaned")
    return dataList

def trainOnCorpus(args, wordSet):
    logger = getLogger(args, "corpus")
    processingArg = []
    totalWordFreq = 0
    for i in range(args.hash_mod):
        processingArg.append((args.word_freq + "wordFreq" + str(i) + ".txt", "utf8"))
    with Pool(processes=min(args.max_process, cpu_count())) as pool:
        wordFreq = pool.starmap(readJsonFile, processingArg)
        for item in wordFreq:
            totalWordFreq += len(item)
    logger.info("successfully loaded %d entries from %s", totalWordFreq, args.word_freq)
    corpus = []
    if args.sina_news:
        corpus += loadSinaCorpus(args, logger)
    if args.smp:
        corpus += loadSmpCorpus(args, logger)
    if args.wiki:
        corpus += loadWikiCorpus(args, logger)
    if args.baike:
        corpus += loadBaikeCorpus(args, logger)
    if len(corpus) > 0:
        random.shuffle(corpus)
        logger.info("%d sentences in total", len(corpus))
        deltaFreq = process(args, corpus, wordSet, logger)
        if totalWordFreq == 0:
            wordFreq = deltaFreq
        else:
            logger.info("start integrating")
            log = getLogger(args, "integrateTqdm", False)
            log.addHandler(TqdmLoggingHandler())
            for j in range(args.hash_mod):
                for key, _ in zip(deltaFreq[j], tqdm.tqdm(range(len(deltaFreq[j])))):
                    if key in wordFreq[j]:
                        wordFreq[j][key] += deltaFreq[j][key]
                    else:
                        wordFreq[j][key] = deltaFreq[j][key]
        logger.info("All data integrated with loaded frequency")
    logger.info("start writing entries to %s", args.word_freq)
    processingArg = []
    totalWordFreq = 0
    for i in range(args.hash_mod):
        processingArg.append((args.word_freq + "/wordFreq" + str(i) + ".txt", wordFreq[i], "utf8"))
        totalWordFreq += len(wordFreq[i])
    with Pool(processes=min(args.max_process, cpu_count())) as p:
        wordFreq = p.starmap(writeJsonFile, processingArg)
    logger.info("successfully writed loaded %d entries to word frequency files", totalWordFreq)