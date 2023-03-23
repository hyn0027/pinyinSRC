from utils.parseArgument import parseArg
from utils.log import *
from loadWord import loadWordList
from utils.file import *
from loadCorpus import trainOnCorpus
from infer import infer
from evaluate import computeMetrics

def main():
    args = parseArg()
    logger = getLogger(args=args, name="main")
    logger.info(args)
    match args.task:
        case "clean":
            logger = getLogger(args=args, name="clean")
            if deleteFile(args.word_freq):
                logger.info("successfully removed frequency file %s", args.word_freq)
            else:
                logger.warning("failed to find word freqency file")
        case "train":
            wordSet, _ = loadWordList(args)
            trainOnCorpus(args, wordSet)
        case "infer":
            _, wordDict = loadWordList(args)
            infer(args, wordDict)
        case "evaluate":
            computeMetrics(args)

if __name__ == '__main__':
    main()