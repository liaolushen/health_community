#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import Image
import ImageDraw
import ImageFont

fonts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/fonts')
mask_img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/image')
width, height = 500, 500

user_map = [{'name':'姓名'},
                    {'sex':'性别'},
                    {'birth_date':'出生日期'},
                    {'birth_locate':'出生地'},
                    {'job':'职业'},
                    {'education':'文化程度'},
                    {'blood':'血型'},
                    {'RH':'RH阴性'}, 
                    {'marry':'婚姻状况'},
                    {'history':'既往史&家族史'}]

def createImg(user_info):
    """
        Args:
            user_info

        Return:
            a Image object
        """
    im = Image.new('RGB', (width, height), 0XFFFFFF)
    draw = ImageDraw.Draw(im)

    # 画第一横作为标题， 50px
    draw.line(((10, 50),(width-10, 50)) , fill=(225,225,225))
    titlefont = ImageFont.truetype(os.path.join(fonts_path, 'msyh.ttf'), 26)
    titlecolor= (225, 225, 225)
    draw.rectangle(((10, 0),(width-10, 50)),fill=(105, 105, 105));
    draw.text((160, 10),unicode('基本信息记录','utf-8'), fill=titlecolor, font=titlefont)

    # 画行横线，每行30像素，第一行多10像素
    for i in range(1,15):
                y=i*30+60;
                draw.line(((10, y),(width-10, y)) , fill=(225,225,225))

    # 边线
    draw.line(((10, 1),(10,height-20)) , fill=(225,225,225))
    draw.line(((width-10, 1),(width-10,height-20)) , fill=(225,225,225))


    # 表头背景
    draw.rectangle(((10,50),(width-10,90)),fill=(223,223,223));

    headfont = ImageFont.truetype(os.path.join(fonts_path, 'msyh.ttf'), 24)
    headcolor = (14,77,157)

    itemfont = ImageFont.truetype(os.path.join(fonts_path, 'msyh.ttf'), 20)
    itemcolor= (0, 0, 0)

    # 标题
    draw.text((20, 55),unicode('项目','utf-8'), fill=headcolor, font=headfont)
    draw.text((250, 55),unicode('内容','utf-8'), fill=headcolor, font=headfont)

    for x in xrange(0, 10):
        draw.text((25, 90+x*30),unicode(user_map[x].values()[0],'utf-8'), fill=itemcolor, font=itemfont)
        draw.text((255, 90+x*30),user_info[user_map[x].keys()[0]], fill=itemcolor, font=itemfont)

    mask_im = Image.open(os.path.join(mask_img_path, 'mask.jpg'))
    im = Image.blend(im, mask_im, 0.2)
    return im
