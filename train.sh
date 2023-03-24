python main.py --task clean

python main.py \
    --task train \
    --sina-news ../corpus/sinaNews \
    --smp ../corpus/smp \
    --wiki ../corpus/wiki_zh 

python main.py --task infer

python main.py --task evaluate