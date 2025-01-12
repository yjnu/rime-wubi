# rime 配置备份与分享

## 前言

- rime 由于官方文档写的太差, 所以配置起来很难, 实际很简单, 所以这里分享一下我的配置, 让后来的人少踩坑. 
- 只在 windows 平台上使用, 所以只分享 windows 平台的配置, 也就是小狼毫的配置.
- 本配置是**五笔**配置, 所以拼音用户可以参考, 五笔用户直接上手换词库就行.
- 由于词库有个人隐私信息, 所以五笔词库就不分享了. 再说五笔词库随人走, 相信你也有自己的词库

## 简要说明
### 自定义快捷键

所有的功能都在这

- <kbd>zhelp</kbd>                      查看所有快捷键，不用背了
- <kbd>Ctrl</kbd> + <kbd>Space</kbd>           中英文切换 （同微软五笔）
- <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>F4</kbd>   输入方案选择
- <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>F5</kbd>   最近两个方案来回切换
- <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>F6</kbd>   emoji 开关
- <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>F7</kbd>   切换到五笔方案
- <kbd>Ctrl</kbd> + <kbd> . </kbd>              中英标点符号切换 （同微软五笔）
- <kbd>Shift</kbd> + <kbd>Space</kbd>         半角全角切换 （同微软五笔）
- <kbd>Ctrl</kbd> + <kbd> \ </kbd>              简繁切换
- <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd> | </kbd>  常用过滤，默认打开
- <kbd>Ctrl</kbd> + <kbd>Enter</kbd>           回车是清码
- <kbd>zv</kbd>                          数字大写 与 计算器
- <kbd>zu</kbd>                          Unicode 转换成汉字
- <kbd>zi</kbd>                          symbol 符号
- <kbd>zo</kbd>                          多行输出，在 lua 中配置
- <kbd>time</kbd> <kbd>date</kbd> <kbd>dati</kbd> <kbd>week</kbd> <kbd>month</kbd>   输入时间
- <kbd>luna</kbd>                       农历


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

## 词库加词与删词
rime 加词与删词并不方便, 所以用 python 写了一个脚本, 加词与删词就很方便了. 补齐了 rime 唯一的短板.

但通用性很差, 当时写得很随意, 没想过兼容性, 所以需要自改脚本中的路径, 才能使用.(等我有空写的教程 #todo)

**脚本不能上手即用**

使用方法: 将脚本所在路径`aRimeScripts`加入到环境变量中, 打开终端输入相应命令即可使用

- `eeadd 词` 添加词组
- `eesub 词` 删除词组
- `eechange 词` 改变词组顺序
- `eelua 单字` 添加屏蔽字
- `eere 要替换词 被替换词` 替换词库中的词

命令操作的是主词库与英文词库, 用户词库与符号需手动修改
