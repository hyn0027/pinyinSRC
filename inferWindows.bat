@REM python main.py --task clean

@REM python main.py ^
@REM     --task train ^
@REM     --sina-news ../corpus/sinaNews ^
@REM     --smp ../corpus/smp ^
@REM     --wiki ../corpus/wiki_zh 

python main.py --task infer

python main.py --task evaluate

pause