def hashString(args, snt):
    hash = 0
    for ch in snt:
        hash += ord(ch) * args.hash_p
        hash %= args.hash_mod
    return hash