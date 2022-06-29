# dex2jar_batch

简单的脚本实现批量调用[dex2jar](https://github.com/pxb1988/dex2jar)，用于配合[FRIDA-DEXDump](https://github.com/hluwa/FRIDA-DEXDump)、[jadx](https://github.com/skylot/jadx)进行脱壳逆向

FRIDA-DEXDump -> dex2jar_batch -> jadx

## Usage

1. 安装进度条所需要的库

> pip install rich

2. 使用FRIDA-DEXDump输出dex到target_dir目录

3. 调用dex2jar_batch.py多进程批量把dex转jar，并且压缩为d2j-output.zip

> python dex2jar_batch.py target_dir

4. jadx打开d2j-output.zip开始逆向吧！

## P.S.

1. 将dex2jar的路径加入环境变量，或者修改一下代码中dex2jar的路径d2jpath

2. dex2jar比较占CPU，进程池大小默认为4，可根据需要修改

## Reference

https://github.com/pxb1988/dex2jar

https://github.com/hluwa/FRIDA-DEXDump

https://github.com/skylot/jadx

