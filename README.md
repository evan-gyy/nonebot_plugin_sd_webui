# nonebot_plugin_sd_webui

基于stable-diffusion-webui实现的nonebot绘画插件

# 指令

```
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
# 使用


启动sd-webui环境，并打开api，具体配置请参考[官方仓库](https://github.com/AUTOMATIC1111/stable-diffusion-webui)

```bash
python launch.py --api --listen
```

安装python依赖

```bash
pip install webuiapi
```


# 更新

**2023/5/11**

- 新增查看lora功能，支持关键词搜索、自动打tag

**2023/5/8**

- 新增图生图功能