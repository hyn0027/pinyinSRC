import argparse

def parseArg():
    parser = argparse.ArgumentParser()
    addArg(parser=parser)
    args=parser.parse_args()
    return args

def addArg(parser):
    parser.add_argument("--task", choices=["clean", "train", "run"], required=True, help="selected from: [clean, train, test]")
    parser.add_argument("--sina-news", required=False, help="corpus folder list")
    parser.add_argument("--verbose", choices=["DEBUG", "INFO", "WARN"], default="INFO", help="selected from: [debug, info, warn]")
    parser.add_argument("--pronounciation", required=False, default="../word/pronounceMap.txt", help="file path to the pronounciation map")
    parser.add_argument("--word-list", required=False, default="../word/includedWord.txt", help="file path to the word list")
    parser.add_argument("--word-freq", required=False, default="../data/wordFreq.txt", help="file path to the word freqency")