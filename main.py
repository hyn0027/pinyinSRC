from utils.parseArgument import parseArg
from utils.log import *
from loadWord import loadWordList
from utils.file import *
from loadCorpus import trainOnCorpus

def main():
    args = parseArg()
    logger = getLogger(args=args, name="main")
    logger.info(args)
    match args.task:
        case "clean":
            if deleteFile(args.word_freq):
                logger.info("successfully removed frequency file %s", args.word_freq)
            else:
                logger.warning("failed to find word freqency file")
        case "train":
            wordSet, _ = loadWordList(args)
            wordFreq = trainOnCorpus(args, wordSet)
        case "run":
            wordSet, wordDict = loadWordList(args)

if __name__ == '__main__':
    main()