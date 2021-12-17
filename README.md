# OptimizerUtils
用于处理优化器输入输出格式的小工具。具体的例子见examples文件夹。

## 使用方法
直接```python xxx.py```即可。(Python版本高于3.7)

# tri2json.py
运行```python tri2json.py examples/vm_src02.txt```即可生成```examples/vm_src02.json```。

读入文件必须为```*.txt```格式。

生成的json文件中，各变量初始值为0，数组初始大小为0，需自行赋值。

# optvm.py
运行```python optvm.py examples/vm_src02.json > examples/vm_src02_vmlog.txt```即可生成```vm_src02_vmout.json```和```vm_src02_vmlog.txt```。

```vm_src02_vmout.json```输出文件记录了虚拟机运行的全过程。而```vm_src02_vmlog.txt```则易于（？）人类阅读。

读入文件必须为合规的```*.json```格式，参见样例。

# 一个样例

下面是虚拟机执行某魔改版本的```CGD(X,Y)```的过程。

```
=======RUNNING=======

  1   0:  R = X % Y
  2   1:  ? R == 0 : 7
FALSE R == 0 ( 2 == 0 )
  3   2:  X = Y
  4   3:  Y = R
  5   4:  !: 0
GOTO 0
  6   0:  R = X % Y
  7   1:  ? R == 0 : 7
FALSE R == 0 ( 1 == 0 )
  8   2:  X = Y
  9   3:  Y = R
 10   4:  !: 0
GOTO 0
 11   0:  R = X % Y
 12   1:  ? R == 0 : 7
TRUE R == 0 ( 0 == 0 )
GOTO 7
 13   7:  HALT
=======DONE=======


=======IN VAR=======
R : 0
X : 233
Y : 7

=======OUT VAR=======
R : 0
X : 2
Y : 1

Saving output to: examples/vm_src01_vmout.json

```

# split.py

基本块切分。运行```python split.py examples/vm_src02.json > examples/vm_src02_blklog.txt```，生成```vm_src02_blk.json```和```vm_src02_blklog.txt```。

```vm_src02_blk.json```输出文件记录了基本块的信息。而```vm_src02_blklog.txt```则易于（？）人类阅读。

一个基本块的json实例如下：
```

  "summary": {
    "total_blocks": 6
  },
  "blocks": {
    "0": {
      "line_num": [
        0,
        3
      ],
      "next": [
        1,
        null
      ],
      "code": [
        "I = M - 1",
        "J = N",
        "T_1 = N",
        "V = A [ T_1 ]"
      ]
    },
    "1": {
      "line_num": [
        4,
        7
      ],
      "next": [
        2,
        1
      ],
      "code": [
        "I = I + 1",
        "T_2 = I",
```
其中，```"line_num"```指示基本块在原文件中开始和结束的行号，```"next"```的第一个元素指示下一个基本块（或不跳转时执行的基本块），第二个元素指示跳转后的下一个基本块。

# 变量

## 支持的变量类型

- 整型 int
- 整型数组 int_array

数组支持负索引，与python中的负索引语义相同，但需要预先定义数组长度。

常数也是整型。

## 变量名

支持的变量名为```[A-Za-z_][A-Za-z0-9_]*```。常数也是整型，但其变量名为其本身的字符串，无需遵守变量名规则。

我们约定，名为```[T_][0-9]+```的变量为临时变量。

# 语句

## 支持的语句类型

- 赋值与四则运算
```
a = T_1
A [ i ] = T_1
T_1 = A [ i ]
T_1 = T_2 + T_3
T_1 = T_2 - T_3
T_1 = T_2 * T_3
T_1 = T_2 / T_3
T_1 = T_2 % T_3
```
- 控制语句
```
!: 101 强制跳转至行号
? T_1 > a : 101 条件跳转至行号
? T_1 < a : 101 
? T_1 == a : 101 
? T_1 >= a : 101 
? T_1 <= a : 101 
? T_1 != a : 101 
HALT 停机
```

注意，语句中的空格是必须严格遵守的格式。

## 存储方式
字符串列表，例如：

```
code = ["R = X % Y",
        "? R == 0 : 7",
        "X = Y",
        "Y = R",
        "!: 0",
        "X = Y + 1",
        "Y = X + 1",
        "HALT"]
```

具体格式见```notebooks/```里的说明。