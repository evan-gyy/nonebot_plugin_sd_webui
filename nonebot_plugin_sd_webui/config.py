#!/usr/bin/env python
# -*- coding:utf-8 -*-
from pydantic import BaseModel, Extra
from nonebot import get_driver
from pathlib import Path


class Config(BaseModel, extra=Extra.ignore):
    bot_name = "莲莲"
    # sd api
    api_host = '127.0.0.1'
    api_port = '7860'
    # path
    save_path = Path(__file__).parent / "save_images"
    lora_path = Path("/mnt/kp230/models/stable-diffusion-webui_23-02-17/models/Lora")
    # args
    negative_prompt = 'ugly, nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry'
    sampler = 'DPM++ 2M'
    steps = 20
    max_steps = 50
    max_size = 1024
    default_size = 512


driver = get_driver()
config = Config.parse_obj(driver.config)
