from .config import config
import asyncio
import re
import os
import sys
import time
import requests
import json
from io import BytesIO
from PIL import Image
import webuiapi
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message, MessageEvent, GroupMessageEvent
from nonebot.log import logger
from nonebot.typing import T_State
from nonebot.params import CommandArg, Arg, ArgStr, Depends
from httpx import AsyncClient, ConnectError

sys.path.append(os.path.abspath(os.path.dirname(__file__)))


__zx_plugin_name__ = "sd"
__plugin_usage__ = """
usage：
    SD_webui
    指令：
        ai画 [prompt] | [negative prompt]：使用stable-diffusion绘画
        ai图生图 [prompt] | [negative prompt] [image]：根据输入的图片绘画
        查看sd模型：查看当前的sd模型，以及所有模型列表
        切换sd模型 [model_id]：切换到某个sd模型
    参数：
        <[width]x[height]>：指定图片大小，如<512x768>
        <s:[steps]>：指定步长，如<s:30>
        <t:[translate]>：翻译成英文，如<t:动人>
    示例：
        ai画 miku, ultra detailed | (low quality:1.4), nsfw:1.5
        ai画 <512x768>, <s:30>, <t:动人>, miku, ultra detailed
        切换sd模型 2
""".strip()
__plugin_des__ = "sd_webui_plugin"
__plugin_cmd__ = ["ai画"]
__plugin_type__ = ("群内小游戏",)
__plugin_version__ = 0.1
__plugin_author__ = "evan-gyy"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": __plugin_cmd__,
}
__plugin_cd_limit__ = {
    "cd": 1,
    "rst": "别急，在画了"
}

api = webuiapi.WebUIApi(host=config.api_host,
                            port=config.api_port,
                            sampler=config.sampler,
                            steps=config.steps
                            )

sd = on_command("ai画", priority=5, block=True)
sd_i2i = on_command("ai图生图", priority=5, block=True)
check_model = on_command("查看sd模型", priority=5, block=True)
change_model = on_command("切换sd模型", priority=5, block=True)


def parse_image(key: str):
    async def _key_parser(
        state: T_State, img: Message = Arg(key)
    ):
        if not get_message_img(img):
            await sd_i2i.reject_arg(key, "请发送要生成的图片")
        state[key] = img
    return _key_parser


@sd.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    global api
    message = args.extract_plain_text()
    if len(message) == 0:
        return

    prompt, negative_prompt, width, height, steps, trans_res = await prompt_wrapper(message)
    if trans_res is not None:
        await sd.send(f"翻译结果：\n{trans_res}")

    start = time.time()
    loop = asyncio.get_event_loop()
    image = await loop.run_in_executor(None, t2i,
                                       api,
                                       prompt,
                                       negative_prompt,
                                       width,
                                       height,
                                       steps)
    delta = round(time.time() - start, 3)
    logger.success(f'成功返回图片，用时{delta} s')

    buffered = BytesIO()
    image.save(buffered, format='png')
    msg = Message(f"用时：{delta} s")
    msg += MessageSegment.image(buffered)
    await sd.send(msg)

    return


@sd_i2i.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State,args: Message = CommandArg()):
    prompt = args.extract_plain_text().strip()
    if prompt:
        state['prompt'] = prompt
    else:
        state['prompt'] = ""
    if get_message_img(event.json()):
        state["img"] = event.message


@sd_i2i.got("img", prompt="图来", parameterless=[Depends(parse_image("img"))])
async def _(bot: Bot,
            event: MessageEvent,
            state: T_State,
            message: str = ArgStr("prompt"),
            img: Message = Arg("img")
):
    url = get_message_img(img)[0]
    temp = BytesIO(requests.get(url).content)
    img = Image.open(temp)
    logger.info(img.size)

    prompt, negative_prompt, width, height, steps, trans_res = await prompt_wrapper(message)
    if trans_res is not None:
        await sd_i2i.send(f"翻译结果：\n{trans_res}")
    
    start = time.time()
    loop = asyncio.get_event_loop()
    image = await loop.run_in_executor(None, i2i,
                                       api,
                                       img,
                                       prompt,
                                       negative_prompt,
                                       width,
                                       height,
                                       steps)
    delta = round(time.time() - start, 3)
    logger.success(f'成功返回图片，用时{delta} s')
    
    buffered = BytesIO()
    image.save(buffered, format='png')
    msg = Message(f"用时：{delta} s")
    msg += MessageSegment.image(buffered)
    await sd_i2i.send(msg)


@check_model.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    old_model = api.util_get_current_model().split('.')[0]
    models = api.util_get_model_names()
    models = '\n'.join([f"{i}. {m.split('.')[0]}" for i, m in enumerate(models)])
    text = f"当前模型：\n{old_model}\n\n模型列表：\n{models}"
    await check_model.send(text)


@change_model.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    global api
    message = args.extract_plain_text()
    models = api.util_get_model_names()
    if len(message) == 0:
        await change_model.finish('请输入要切换的模型')
    try:
        index = int(message)
        if index >= 0 and index < len(models):
            await change_model.send('模型载入中...')
            start = time.time()
            loop = asyncio.get_event_loop()
            ret = await loop.run_in_executor(None, set_model, models[index])
            delta = round(time.time() - start, 3)
            logger.info('切换模型：', ret)
            if ret == 'success':
                curr = api.util_get_current_model().split('.')[0]
                await change_model.send(f'切换完成：{curr}\n用时：{delta} s')
            else:
                await change_model.send(f'发生错误：{ret}')
        else:
            await change_model.send('请输入正确的序号')

    except Exception as e:
        logger.error(str(e))
        change_model.send('请输入模型序号')


async def prompt_wrapper(message):
    trans = re.search('<t[:：]([^>]+)>', message)
    if trans:
        message, trans_res = await translator(message, trans)
    else:
        trans_res = None

    if '|' in message:
        prompt = message.split('|')[0]
        negative_prompt = ''.join(message.split('|')[1:]) + ',' + config.negative_prompt
    else:
        prompt = message
        negative_prompt = config.negative_prompt
    
    logger.info('prompt: %s' % prompt)
    logger.info('negative prompt: %s' % negative_prompt)
    
    max_size = config.max_size
    size = re.search('<(\d+)[x×](\d+)>', prompt)
    step = re.search('<s[:：](\d+)>', prompt)

    if size:
        width = min(abs(int(size.group(1))), max_size)
        height = min(abs(int(size.group(2))), max_size)
        prompt = prompt.replace(size.group(), '')
    else:
        width = config.default_size
        height = config.default_size

    if step:
        steps = min(abs(int(step.group(1))), config.max_steps)
        prompt = prompt.replace(step.group(), '')
    else:
        steps = config.steps

    if size or step:
        logger.info(f'final prompt: {prompt}')
    
    return prompt, negative_prompt, width, height, steps, trans_res


async def translator(message, trans):
    async with AsyncClient(verify=False, follow_redirects=True) as c:
        resp = ''
        for i in range(5):
            try:
                resp = await c.post(
                    "https://hf.space/embed/mikeee/gradio-gtr/+/api/predict", 
                    json={"data": [trans.group(1), "auto", "en"]}
                )
                if resp.status_code != 200:
                    return False
                break
            except ConnectError as e:
                logger.error(f'{e}: retry {i+1}')
                time.sleep(0.5)

        if resp:
            result = resp.json()
            result = result["data"][0]
            message = message.replace(trans.group(), result)
        else:
            result = '翻译失败'

        return message, result


def t2i(api, prompt, n, width, height, steps):
    r = api.txt2img(
        prompt=prompt,
        negative_prompt=n,
        width=width,
        height=height, 
        steps=steps,
    )
    return r.image


def i2i(api, image, prompt, n, width, height, steps):
    r = api.img2img(
        images=[image],
        prompt=prompt,
        negative_prompt=n,
        width=width,
        height=height, 
        steps=steps,
    )
    return r.image


def set_model(model):
    try:
        api.util_set_model(model)
        return 'success'
    except Exception as e:
        return str(e)
    

def img2bytes(img):
    img_bytes = BytesIO()
    img.save(img_bytes, format="png")
    img_bytes = img_bytes.getvalue()
    return img_bytes


def get_message_img(data):
    img_list = []
    if isinstance(data, str):
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "image":
                img_list.append(msg["data"]["url"])
    else:
        for seg in data["image"]:
            img_list.append(seg.data["url"])
    return img_list
