import argparse

def parseArg():
    parser = argparse.ArgumentParser()
    addArg(parser=parser)
    args=parser.parse_args()
    return args

def addArg(parser):
    parser.add_argument("--task", choices=["clean", "train", "infer", "evaluate"], required=True, help="Selected from: [clean, train, infer, evaluate]")
    parser.add_argument("--sina-news", required=False, help="Corpus folder list for sinaNews. Only add this argument when ADDING this corpus into current word frequency")
    parser.add_argument("--smp", required=False, help="Corpus folder list for SMP. Only add this argument when ADDING this corpus into current word frequency")
    parser.add_argument("--wiki", required=False, help="Corpus folder list for wiki-zh. Only add this argument when ADDING this corpus into current word frequency")
    parser.add_argument("--verbose", choices=["DEBUG", "INFO", "WARN"], default="INFO", help="Selected from: [debug, info, warn]")
    parser.add_argument("--pronounciation", required=False, default="../word/pronounceMap.txt", help="File path to the pronounciation map")
    parser.add_argument("--word-list", required=False, default="../word/includedWord.txt", help="File path to the word list")
    parser.add_argument("--word-freq", required=False, default="./data/wordFreq.json", help="File path to the word freqency")
    parser.add_argument("--max-batch-size", type=int, default=100000, help="Maximum number of sentence processed per process")
    parser.add_argument("--max-process", type=int, default=20, help="Maximum number of processes")
    parser.add_argument("--report-interval", type=int, default=10000, help="Report interval for processing corpus")
    parser.add_argument("--input", default="../testCase/input.txt", help="the pinyin input file")
    parser.add_argument("--std-output", default="../testCase/std_output.txt", help="the answer to the input file")
    parser.add_argument("--output", default="../testCase/output.txt", help="the Chinese output file")
    parser.add_argument("--smooth-lambda", type=float, default=0.99995, help="hyper-parameter for smoothing, should lies in [0, 1]")
    parser.add_argument("--smooth-lambda1", type=float, default=0.73, help="hyper-parameter for smoothing, should lies in [0, 1]")
    parser.add_argument("--smooth-lambda2", type=float, default=0.26995, help="hyper-parameter for smoothing, should lies in [0, 1]")
    parser.add_argument("--epsilon", type=float, default=0.000000001, help="the smallest absolute value")
    parser.add_argument("--inf", type=float, default = 1e16, help="the infinitelt long path")
    parser.add_argument("--infer-num", choices=[2, 3], default=3, help="inferring based on word pairs or word triplets ")