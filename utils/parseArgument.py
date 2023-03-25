import argparse

def parseArg():
    parser = argparse.ArgumentParser()
    addArg(parser=parser)
    args=parser.parse_args()
    return args

def addArg(parser):
    parser.add_argument("--task", choices=["clean", "train", "dictionary", "infer", "evaluate"], required=True, \
                        help="Selected from: [clean, train, dictionary, infer, evaluate]")
    parser.add_argument("--sina-news", required=False, \
                        help="Corpus folder list for sinaNews. Only add this argument when ADDING this corpus into current word frequency")
    parser.add_argument("--smp", required=False, \
                        help="Corpus folder list for SMP. Only add this argument when ADDING this corpus into current word frequency")
    parser.add_argument("--wiki", required=False, \
                        help="Corpus folder list for wiki-zh. Only add this argument when ADDING this corpus into current word frequency")
    parser.add_argument("--baike", required=False, \
                        help="Corpus folder list for baike. Only add this argument when ADDING this corpus into current word frequency")
    parser.add_argument("--verbose", choices=["DEBUG", "INFO", "WARN"], default="INFO", \
                        help="Selected from: [debug, info, warn]")
    parser.add_argument("--pronounciation", required=False, default="../word/pronounceMap.txt", \
                        help="File path to the pronounciation map")
    parser.add_argument("--word-list", required=False, default="../word/includedWord.txt", \
                        help="File path to the word list")
    parser.add_argument("--word-freq", required=False, default="./data/", \
                        help="File path to the word freqency")
    parser.add_argument("--max-batch-size", type=int, default=100000, \
                        help="Maximum number of sentence processed per process")
    parser.add_argument("--max-process", type=int, default=20, \
                        help="Maximum number of processes")
    parser.add_argument("--report-interval", type=int, default=10000, \
                        help="Report interval for processing corpus")
    parser.add_argument("--input", default="../data/input.txt", \
                        help="the pinyin input file")
    parser.add_argument("--std-output", default="../data/std_output.txt", \
                        help="the answer to the input file")
    parser.add_argument("--output", default="../data/output.txt", \
                        help="the Chinese output file")
    parser.add_argument("--smooth-lambda", type=float, default=0.99995, \
                        help="hyper-parameter for smoothing, should lies in [0, 1]")
    parser.add_argument("--smooth-lambda1", type=float, default=0.72, \
                        help="hyper-parameter for smoothing, should lies in [0, 1]")
    parser.add_argument("--smooth-lambda2", type=float, default=0.2795, \
                        help="hyper-parameter for smoothing, should lies in [0, 1]")
    parser.add_argument("--epsilon", type=float, default=0.000000001, \
                        help="the smallest absolute value")
    parser.add_argument("--inf", type=float, default = 1e16, \
                        help="the infinitelt long path")
    parser.add_argument("--infer-num", type=int, choices=[2, 3], default=2, \
                        help="inferring based on word pairs or word triplets ")
    parser.add_argument("--hash-mod", default=20, \
                        help="a factor for hash")
    parser.add_argument("--hash-p", default=7, \
                        help="a factor for hash")
    parser.add_argument("--only-title", default=True, \
                        help="only use title from corpus wiki-zh")
    parser.add_argument("--dictionary", default="../corpus/pinyin.txt", \
                        help="the path to dictionary")
    parser.add_argument("--add-dict", type=bool, default=False, \
                        help="whether to use pinyin frequency from dictionary or not")
    parser.add_argument("--dict-smooth", type=float, default=0.1, \
                        help="to what extent the effect of dictionary is smoothed")