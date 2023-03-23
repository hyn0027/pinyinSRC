from utils.file import *
from utils.log import getLogger

def computeMetrics(args):
    logger = getLogger(args, "evaluate")
    test = readFile(args.output, encoding="utf8")
    logger.info("successfully load %d sentences for test from %s", len(test), args.output)
    stdOut = readFile(args.std_output, encoding="utf8")
    logger.info("successfully load %d sentences as standard from %s", len(stdOut), args.std_output)
    assert(len(test) == len(stdOut))
    sntCnt = 0
    wordCnt = 0
    totalWord = 0
    for i in range(len(test)):
        generated = test[i].replace('\n', '')
        std = stdOut[i].replace('\n', '')
        assert(len(generated) == len(std))
        sntCnt += (generated == std)
        for j in range(len(generated)):
            totalWord += 1
            wordCnt += (generated[j] == std[j])
    logger.info("sentence accuracy = %f%s", sntCnt / len(test) * 100, "%")
    logger.info("word accuracy = %f%s", wordCnt / totalWord * 100, "%")