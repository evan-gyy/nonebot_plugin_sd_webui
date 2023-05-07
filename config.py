#!/usr/bin/env python
# -*- coding:utf-8 -*-
from pydantic import BaseModel, Extra
from nonebot import get_driver
from pathlib import Path


class Config(BaseModel, extra=Extra.ignore):
    # sd
    api_host = '127.0.0.1'
    api_port = '7860'
    save_path = Path(__file__).parent / "save_images"
    negative_prompt = 'ugly, nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry'
    sampler = 'DPM++ 2M'
    steps = 20
    max_steps = 50
    max_size = 1024
    default_size = 512


driver = get_driver()
config = Config.parse_obj(driver.config)
