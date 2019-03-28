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
| -t \<tx_hash\> | --transaction \<tx_hash\> | 查看此交易最早收到的节点的时间，最晚收到的节点的时间，交易从出现到完全广播话费的时间 |
| -t all | --transaction all | 查看所有交易完全广播的最短时间，最长时间，平均值，中位数 |
| -b \<block_height\> | --block \<block_height\> | 查看此区块最早收到的节点的时间，最晚收到的节点的时间，交易从出现到完全广播花费的时间 |
| -b all | --block all | 查看所有区块完全广播的最短时间，最长时间，平均值，中位数 |



## 日志参数说明

* time: Mar 17 00:00:00.486 (月 日 时:分:秒.毫秒)
* level: info（日志等级）
* msg: receive message from peer
* message: tx_size tx_hash （交易大小和交易id）/ height hash（区块高度和区块Hash）/ 
* peer: 115.54.192.9:52618 （节点ip和端口）
* type:  *netsync.TransactionMessage （交易日志） / *netsync.MineBlockMessage （区块日志）