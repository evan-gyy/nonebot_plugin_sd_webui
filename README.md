<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot_plugin_sd_webui

_✨ 基于stable-diffusion-webui的nonebot绘画插件 ✨_

<a href="https://github.com/evan-gyy/nonebot_plugin_sd_webui/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/evan-gyy/nonebot_plugin_sd_webui?color=%09%2300BFFF&style=flat-square">
</a>
<a href="https://github.com/evan-gyy/nonebot_plugin_sd_webui/issues">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/evan-gyy/nonebot_plugin_sd_webui?color=Emerald%20green&style=flat-square">
</a>
<a href="https://github.com/evan-gyy/nonebot_plugin_sd_webui/network">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/evan-gyy/nonebot_plugin_sd_webui?color=%2300BFFF&style=flat-square">
</a>
<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/evan-gyy/nonebot_plugin_sd_webui.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_sd_webui">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_sd_webui.svg" alt="pypi">
</a>
<a href="https://www.python.org">
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</a>

</div>

## 📖 介绍

nonebot绘画插件，基于sd-webui实现，支持指定模型、参数等

## 🔧 开发环境
Nonebot2：2.0.0rc3  
python：3.8.13  
操作系统：Windows 10、Ubuntu 22.04  
编辑器：VS Code  

## 💿 安装  

### 1. nb-cli安装（推荐）

在你bot工程的文件夹下，运行cmd，执行nb命令安装插件，插件配置会自动添加至配置文件  
```
nb plugin install nonebot_plugin_sd_webui
```

### 2. 本地安装

将项目clone到你的机器人插件下的对应插件目录内（一般为机器人文件夹下的`src/plugins`），然后把`nonebot_plugin_sd_webui`文件夹里的内容拷贝至上一级目录即可。  
clone命令参考：

```
git clone https://github.com/evan-gyy/nonebot_plugin_sd_webui.git
```
也可以直接下载压缩包到插件目录解压，然后同样提取`nonebot_plugin_sd_webui`至上一级目录。  
目录结构： ```你的bot/src/plugins/nonebot_plugin_sd_webui/__init__.py```  


### 3. pip安装
```
pip install nonebot_plugin_sd_webui
```
打开 nonebot2 项目的 ```bot.py``` 文件, 在其中写入  
```nonebot.load_plugin('nonebot_plugin_sd_webui')```  
当然，如果是默认nb-cli创建的nonebot2的话，在bot路径```pyproject.toml```的```[tool.nonebot]```的```plugins```中添加```nonebot_plugin_sd_webui```即可  
pyproject.toml配置例如：  
``` 
[tool.nonebot]
plugin_dirs = ["src/plugins"]
plugins = ["nonebot_plugin_sd_webui"]
```

### 更新版本
```
nb plugin update nonebot_plugin_sd_webui
```

## 🔧 配置

### sd-webui配置
启动sd-webui环境，并打开api，具体配置请参考[官方仓库](https://github.com/AUTOMATIC1111/stable-diffusion-webui)

```bash
python launch.py --api --listen
```

## 🎉 功能

基于stable-diffusion的AI绘画


## 👉 命令

```bash
指令：
    ai画 [prompt] | [negative prompt]：使用stable-diffusion绘画
    ai图生图 [prompt] | [negative prompt] [image]：根据输入的图片绘画
    查看sd模型：查看当前的sd模型，以及所有模型列表
    切换sd模型 [model_id]：切换到某个sd模型
    查看lora ?[标签] ?[keyword]：查看可用的lora模型，支持关键词搜索、自动打tag
参数：
    <[width]x[height]>：指定图片大小，如<512x768>
    <s:[steps]>：指定步长，如<s:30>
    <t:[translate]>：翻译成英文，如<t:动人>
示例：
    ai画 miku, ultra detailed | (low quality:1.4), nsfw:1.5
    ai画 <512x768>, <s:30>, <t:动人>, miku, ultra detailed
    切换sd模型 2
```


## ⚙ 拓展


## 📝 更新日志

<details>
<summary>展开/收起</summary>

### 0.0.1

- 插件初次发布  

</details>

## 致谢
- [nonebot-plugin-template](https://github.com/A-kirami/nonebot-plugin-template)
