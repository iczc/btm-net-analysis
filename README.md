# btm-net-analysis

通过多个节点的日志分析区块链分布式网络上交易和区块的传播情况。

## Requirements

* Python3  
* Packages:

To install packages using:
```bash
$ pip install -r requirements.txt
```
## Usage

```bash
$ python main.py
```

Options:

| Option (short) | Options (long) | Explanation |
| :------------- | :------------- |:-------------|
| -h | --help | 查看使用帮助 |
| -b \<block_height\> | --block \<block_height\> | 查看此区块最早收到的节点的时间，最晚收到的节点的时间，交易从出现到完全广播花费的时间 |
| -b all | --block all | 查看所有区块完全广播的最短时间，最长时间，平均值，中位数 |
| -t \<tx_hash\> | --transaction \<tx_hash\> | 查看此交易最早收到的节点的时间，最晚收到的节点的时间，交易从出现到完全广播话费的时间 |
| -t all | --transaction all | 查看所有交易完全广播的最短时间，最长时间，平均值，中位数 |