import logging

def getLogger(args, name):
    logger = logging.getLogger(name)
    logger.setLevel(eval("logging." + args.verbose))
    fmt = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    datefmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(fmt, datefmt)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger