# nonebot_plugin_sd_webui

基于stable-diffusion-webui实现的nonebot绘画插件

# 指令

```
指令：
    ai画 [prompt] | [negative prompt]：使用stable-diffusion绘画
    查看sd模型：查看当前的sd模型，以及所有模型列表
    切换sd模型 [model_id]：切换到某个sd模型
示例：
    ai画 miku, ultra detailed | (low quality:1.4), nsfw:1.5
    切换sd模型 2
```
# 使用


启动sd-webui环境，并打开api，具体配置请参考[官方仓库](https://github.com/AUTOMATIC1111/stable-diffusion-webui)

```bash
python launch.py --api
```

安装python依赖

```bash
pip install webuiapi
```


# 更新

**2023/5/5**

新增切换/查看sd模型功能