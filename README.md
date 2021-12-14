# OptimizerUtils
用于处理优化器输入输出格式的小工具。具体的例子见examples文件夹。

## 使用方法
直接```make```即可。

# tri2quad
从标准输入读入三地址代码，将转换后的四元式输出到标准输出。

# quad2tri
从标准输入读入四元式，将转换后的三地址代码输出到标准输出。

# split
从标准输入读入四元式，输出切分后的基本块和基本块的信息。例如：
```
; #BLK 1 （基本块编号
READ	R	-	- 
READ	r	-	- 
SET	T0	3.14	- 
MUL	T1	2	T0 
ADD	T2	R	r 
MUL	A	T1	T2 
SET	B	A	- 
MUL	T3	2	T0 
ADD	T4	R	r 
MUL	T5	T3	T4 
SUB	T6	R	r 
MUL	B	T5	T6 
SET	I	1	- 
; NXT 2 0 （下一个基本块的编号，0无效
; VAR A B I R T0 T1 T2 T3 T4 T5 T6 r （基本块中出现的变量
; DEF A B I R T0 T1 T2 T3 T4 T5 T6 r （基本块中首次出现是以定值形式出现的变量
; USE （基本块中首次出现是以引用形式出现的变量
; OUT A I J （基本块出口处的活跃量，用于基本块内的优化
; IN J（基本块入口处的活跃量
```