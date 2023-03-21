import argparse

def parseArg():
    parser = argparse.ArgumentParser()
    addArg(parser=parser)
    args=parser.parse_args()
    return args

def addArg(parser):
    parser.add_argument("--task", choices=["clean", "train", "run"], required=True, help="selected from: [clean, train, test]")
    parser.add_argument("--corpus-list", nargs="*", default=[], help="corpus folder list")
    parser.add_argument("--verbose-level", choices=["DEBUG", "INFO", "WARN"], default="INFO", help="selected from: [debug, info, warn]")