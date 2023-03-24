from utils.file import *
from utils.log import getLogger, TqdmLoggingHandler
from math import log
import tqdm

def loadInput(args):
    logger = getLogger(args, "loadInput")
    input = readFile(args.input, encoding="utf8")
    for i in range(len(input)):
        input[i] = input[i].split()
    logger.info("successfully loaded %d input from %s", len(input), args.input)
    return input

def checkFreq(wordFreq, key):
    if key in wordFreq:
        return wordFreq[key]
    return 0

def loss(args, char1, char2, pinyin2, wordDict, wordFreq):
    sumOfPinyin2 = 0
    for item in wordDict[pinyin2]:
        sumOfPinyin2 += checkFreq(wordFreq, item)
    if sumOfPinyin2 == 0:
        Pwi = 1.0 / len(wordDict[pinyin2])
    else:
        Pwi = float(checkFreq(wordFreq, char2)) / sumOfPinyin2
    sumOfChar1 = checkFreq(wordFreq, char1)
    if sumOfChar1 == 0:
        Pwiwi_1 = Pwi
    else:
        Pwiwi_1 = float(checkFreq(wordFreq, char1 + char2)) / sumOfChar1
    p = args.smooth_lambda * Pwiwi_1 + (1 - args.smooth_lambda) * Pwi
    return -log(max(p, args.epsilon))

def tripleLoss(args, words, pinyin, wordDict, wordFreq):
    sumOfPinyin3 = 0
    for item in wordDict[pinyin]:
        sumOfPinyin3 += checkFreq(wordFreq, item)
    if sumOfPinyin3 == 0:
        Pwi = 1.0 / len(wordDict[pinyin])
    else:
        Pwi = float(checkFreq(wordFreq, words[2])) / sumOfPinyin3
    
    sumOfChar2 = checkFreq(wordFreq, words[1])
    if sumOfChar2 == 0:
        Pwiwi_1 = Pwi
    else:
        Pwiwi_1 = float(checkFreq(wordFreq, words[1:])) / sumOfChar2
    
    sumOfChar12 = checkFreq(wordFreq, words[:2])
    if sumOfChar12 == 0:
        Pwiwi_1w_2 = Pwiwi_1
    else:
        Pwiwi_1w_2 = float(checkFreq(wordFreq, words)) / sumOfChar12

    p = args.smooth_lambda1 * Pwiwi_1w_2 + args.smooth_lambda2 * Pwiwi_1 \
        + (1 - args.smooth_lambda1 - args.smooth_lambda2) * Pwi
    return -log(max(p, args.epsilon))

def inferSingle(args, snt, wordDict, wordFreq):
    match args.infer_num:
        case 2:
            dist = [dict()]
            point = [dict()]
            for word in wordDict[snt[0]]:
                dist[0][word] = loss(args, " ", word, snt[0], wordDict, wordFreq)
                point[0][word] = None
            for idx in range(1, len(snt)):
                for char2 in wordDict[snt[idx]]:
                    dist.append(dict())
                    point.append(dict())
                    dist[idx][char2] = args.inf
                    point[idx][char2] = None
                    for char1 in dist[idx - 1]:
                        l = loss(args, char1, char2, snt[idx], wordDict, wordFreq)
                        if dist[idx - 1][char1] + l < dist[idx][char2]:
                            dist[idx][char2] = dist[idx - 1][char1] + l
                            point[idx][char2] = char1
        case 3:
            dist = [dict()]
            point = [dict()]
            for word in wordDict[snt[0]]:
                dist[0][word] = tripleLoss(args, "  " + word, snt[0], wordDict, wordFreq)
                point[0][word] = None
            for word in wordDict[snt[1]]:
                dist.append(dict())
                point.append(dict())
                dist[1][word] = args.inf
                point[1][word] = None
                for char1 in dist[0]:
                    l = tripleLoss(args, " " + char1 + word, snt[1], wordDict, wordFreq)
                    if dist[0][char1] + l < dist[1][word]:
                        dist[1][word] = dist[0][char1] + l
                        point[1][word] = char1
            for idx in range(2, len(snt)):
                for char3 in wordDict[snt[idx]]:
                    dist.append(dict())
                    point.append(dict())
                    dist[idx][char3] = args.inf
                    point[idx][char3] = None
                    for char2 in dist[idx - 1]:
                        l = tripleLoss(args, point[idx - 1][char2] + char2 + char3, snt[idx], wordDict, wordFreq)
                        if dist[idx - 1][char2] + l < dist[idx][char3]:
                            dist[idx][char3] = dist[idx - 1][char2] + l
                            point[idx][char3] = char2
    minDist = args.inf
    idx = len(snt) - 1
    result = ""
    for word in dist[idx]:
        if dist[idx][word] < minDist:
            minDist = dist[idx][word]
            result = word
    while idx > 0:
        result = point[idx][result[0]] + result
        idx -= 1
    return result

def infer(args, wordDict):
    logger = getLogger(args, "infer")
    wordFreq = readJsonFile(args.word_freq, encoding="utf8")
    logger.info("successfully loaded %d word entries from %s", len(wordFreq), args.word_freq)
    input = loadInput(args)
    logger.info("begin inferring")
    output = []
    log = getLogger(args, "inferTqdm", False)
    log.addHandler(TqdmLoggingHandler())
    for i in tqdm.tqdm(range(len(input))):
        snt = input[i]
        result = inferSingle(args, snt, wordDict, wordFreq)
        output.append(result)
    logger.info("successfully inferred %d sentences", len(input))
    writeToFile(args.output, output, encoding="utf8")
    logger.info("succcessfully write results to %s", args.output)