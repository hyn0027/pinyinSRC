from tools.parseArgument import parseArg
from tools.log import *

def main():
    args = parseArg()
    logger = getLogger(args=args, name="main")
    logger.info(args)

if __name__ == '__main__':
    main()