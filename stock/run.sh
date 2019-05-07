# pip install  -t . --no-deps -U tushare
# pip install --install-option="--prefix=/home/wang/Code/tushare" tushare -i https://pypi.tuna.tsinghua.edu.cn/simple --no-deps
# pip install -t . -U tushare -i https://pypi.tuna.tsinghua.edu.cn/simple --no-deps
#sudo docker run --runtime nvidia --rm -it -v /home/wang/Code/:/root/work nvidia/cuda:dev bash

rm nohup.out
#nohup python main.py &
#nohup python main.py -t &
nohup python main.py -r &
