import argparse

def parseArg():
    parser = argparse.ArgumentParser()
    addArg(parser=parser)
    args=parser.parse_args()
    return args

def addArg(parser):
    parser.add_argument("--task", choices=["clean", "train", "run", "test"], required=True, help="Selected from: [clean, train, test]")
    parser.add_argument("--sina-news", required=False, help="Corpus folder list for sinaNews. Only add this argument when ADDING this corpus into current word frequency")
    parser.add_argument("--verbose", choices=["DEBUG", "INFO", "WARN"], default="INFO", help="Selected from: [debug, info, warn]")
    parser.add_argument("--pronounciation", required=False, default="../word/pronounceMap.txt", help="File path to the pronounciation map")
    parser.add_argument("--word-list", required=False, default="../word/includedWord.txt", help="File path to the word list")
    parser.add_argument("--word-freq", required=False, default="./data/wordFreq.json", help="File path to the word freqency")
    parser.add_argument("--max-batch-size", type=int, default=100000, help="Maximum number of sentence processed in a process")
    parser.add_argument("--max-process", type=int, default=14, help="Maximum number of process")
    parser.add_argument("--report-interval", type=int, default=10000, help="Report interval for processing corpus")