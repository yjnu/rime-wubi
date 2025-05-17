# rime 配置备份与分享

## 背景

最好用的五笔输入法是哪个，肯定是极点五笔，但极点五笔停止更新后，几乎不能在 Windows 11 上运行。Rime 通过配置能变成你想要的那个输入法，本配置的目标就是实现极点五笔的大部分功能并加以创新。

## 前言

- rime 由于官方文档写的太差, 所以配置起来很难, 实际很简单, 所以这里分享一下我的配置, 让后来的人少踩坑. 
- 只在 windows 平台上使用, 所以只分享 windows 平台的配置, 也就是小狼毫的配置.
- 本配置是**五笔**配置, 所以拼音用户可以参考, 五笔用户直接上手换词库就行.
- 由于词库有个人隐私信息, 所以词库不分享. 再说词库随人走, 相信你也有自己的词库

## 简要说明

### 自定义快捷键

所有的功能都在这，都是输入法基本功能，不用多说

- <kbd>help</kbd>                        键入 help 候选项显示所有快捷键
- <kbd>Ctrl</kbd> + <kbd>Space</kbd>           中英文切换 （同微软五笔）
- <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>F4</kbd>   输入方案选择
- <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>F5</kbd>   最近两个方案来回切换
- <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>F6</kbd>   emoji 开关
- <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>F7</kbd>   切换到五笔单字方案
- <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>F8</kbd>   动态候选词数量
- <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>F9</kbd>   注释显隐
- <kbd>Ctrl</kbd> + <kbd> . </kbd>                 中英标点符号切换
- <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>Space</kbd>      半角全角切换 
- <kbd>Ctrl</kbd> + <kbd> \ </kbd>                   简繁切换
- <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd> | </kbd>      常用过滤，默认打开
- <kbd>zv</kbd>                             数字大写
- <kbd>zu</kbd>                             Unicode 转换成汉字
- <kbd>info</kbd>                          候选项显示 rime 信息
- <kbd>time</kbd> <kbd>date</kbd> <kbd>dati</kbd> <kbd>week</kbd> <kbd>month</kbd>   输入时间
- <kbd>lunar</kbd>                         农历
- <kbd>Ctrl</kbd> + <kbd> H</kbd>          删除一个编码
- <kbd>Ctrl</kbd> + <kbd> J </kbd>          光标下移
- <kbd>Ctrl</kbd> + <kbd> K </kbd>          光标上移
- <kbd>Ctrl</kbd> + <kbd> L </kbd>          注释上屏
- <kbd>Ctrl</kbd> + <kbd> Enter </kbd>     清码
- <kbd>Tab</kbd>                   向下翻页
- <kbd>Shift</kbd> + <kbd>Tab</kbd>      向上翻页


### 中英文切换设定

通过 ahk v2 实现 <kbd>Ctrl</kbd> + <kbd>Space</kbd> 切换中英文并上屏编码

如果要使用, 需要额外下载 ahk v2, 并写下面代码, 最后设置开机运行 ahk 脚本, 如果不会, 那就不配.

```AHK
; Ctrl + Space  输出 RShift  用来对rime输入法的补充
^Space::
{
  KeyWait "Control"
  Send "{RShift}"
}
```

中英切换其实也可以在 rime 中，通过 lua 实现，但 ahk 可以融合更多功能。

### 四个方案说明

总共有四个方案, 分别是
1. 默认五笔, 只有常用字与词, 用于目常使用
2. 五笔单字, 包含几乎所有汉字, 用于对五笔不能录入时的补充
3. 拼音, 用于反查五笔
4. 英文, 挂载到五笔中, 可实现输入英文单词

### 配置总结
五笔熟练用户上手就能用, 虽然有很多功能, 但都花里胡哨的, 比如: 注释上屏, 农历转换, 

## 词库加词与删词

rime 加词与删词并不方便, 所以用 python 写了一个脚本, 加词与删词就很方便了. 补齐了 rime 唯一的短板.

但通用性很差, 当时写得很随意, 没想过兼容性, 所以需要自改脚本中的路径, 才能使用.(等我有空写的教程 #todo)

**脚本不能上手即用**

使用方法: 将脚本所在路径`aRimeScripts`加入到环境变量中, 安装 python，打开终端输入相应命令即可使用

- `eeadd 词` 添加词组
- `eedel 词` 删除词组
- `eemv 词` 改变词组顺序
- `eelua 单字 <可选：注音>`  添加屏蔽字 或 注音
- `eere 新词 被替换词` 替换词库中的词
- `eehelp` 使用帮助

命令操作的是主词库与英文词库, 用户词库与符号需手动修改

### 图形化界面改词库

命令行加词虽然方便，但依然存在一些问题

- Windows 的终端打开速度慢
- 每次都要输入命令，麻烦

如何能像极点五笔，QQ五笔还有其它输入法一样按 `Ctrl` + `+` 就能迅速打开改词界面。还得是 ahk，简单高效。

如果你按照前面操作，只需将页末的代码加入到 ahk 即可。

用法：

- `Ctrl` + `Alt` + `+` 打开 ahk 窗口，已经预输入 eeadd
- `Ctrl` + `D` 快速输入 eedel
- `Ctrl` + `M` 快速输入 eemv
- `Ctrl` + `H` 快速查看帮助
- 默认 Ctrl+回车 运行命令，Esc 关闭窗口，或者切后台自动关闭窗口

![ahk界面](./sample/ahk_1.jpg)

## 后记

目前逐级显码与加减词不如极点五笔，前者因为 rime 自身原因，后者因为是外挂脚本, 加词需再输入一遍词, 删除词与调整候选位置不能直接用 Ctrl + 数字。要想改进, 只有从小狼毫源码入手改动，分支后有些bug会得不到修复，得不偿失，所以还是得外挂。

Rime 的使用体验，我认为是比极点五笔好的。极点虽是五笔输入法中的一座高峰，但那已是过去式。

极点的很多功能是建立在单词库和一行一码对多词的基础上，词库大杂烩限制了词库的分享，现在五笔传播最广的词库还是二十年前的极爽词库。现在哪还有什么人用五笔啊，哪还需要分享词库啊，不过都是自嗨罢了。

包括 win10 及之后的系统，就五笔输入法而言，能用的就三个，冰凌，rime和微软五笔，冰凌最大的问题是难看。而 rime 比微软五笔的皮肤好看，改词库更方便，还能自定义快捷键，最重要的是自定义词库，所以 Windows 平台，rime 就是目前最好用的输入法。

rime 文档看了数遍，反复折腾了多次，此次更新后不会再大改 rime 配置文件了。