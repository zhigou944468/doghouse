# -*- coding: utf-8 -*-
"""生成「狗窝」PWA 图标（狗狗脸）。"""
from PIL import Image, ImageDraw
import os

BG    = (246, 173, 85, 255)      # 焦糖橙背景
EAR   = (150, 100, 62, 255)      # 深棕垂耳
FACE  = (250, 243, 230, 255)     # 奶白脸
EYE   = (46, 32, 24, 255)        # 眼睛
NOSE  = (96, 64, 42, 255)        # 鼻子
BLUSH = (255, 170, 170, 170)     # 腮红（半透明）


def draw_dog(S, scale=1.0):
    """返回透明背景、居中的狗狗脸 RGBA 图。"""
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    u = S * scale            # 狗狗占位边长
    ox = (S - u) / 2.0
    oy = (S - u) / 2.0

    def P(a, b, c, dd):      # 比例坐标 -> 像素 bbox
        return (ox + a * u, oy + b * u, ox + c * u, oy + dd * u)

    # 垂耳（先画，脸会盖住耳根，只露出两侧）
    d.ellipse(P(0.10, 0.18, 0.34, 0.64), fill=EAR)
    d.ellipse(P(0.66, 0.18, 0.90, 0.64), fill=EAR)
    # 脸
    d.ellipse(P(0.26, 0.34, 0.74, 0.86), fill=FACE)
    # 眼睛
    d.ellipse(P(0.40, 0.56, 0.47, 0.65), fill=EYE)
    d.ellipse(P(0.53, 0.56, 0.60, 0.65), fill=EYE)
    # 高光
    d.ellipse(P(0.415, 0.575, 0.445, 0.605), fill=(255, 255, 255, 255))
    d.ellipse(P(0.545, 0.575, 0.575, 0.605), fill=(255, 255, 255, 255))
    # 鼻子
    d.ellipse(P(0.47, 0.68, 0.53, 0.76), fill=NOSE)
    # 嘴（微笑弧）
    d.arc(P(0.42, 0.70, 0.58, 0.88), start=18, end=162, fill=NOSE, width=int(u * 0.03))
    # 腮红
    d.ellipse(P(0.32, 0.66, 0.42, 0.74), fill=BLUSH)
    d.ellipse(P(0.58, 0.66, 0.68, 0.74), fill=BLUSH)
    return img


def make_icon(S, scale, rounded):
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if rounded:
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.22), fill=BG)
    else:
        d.rectangle([0, 0, S - 1, S - 1], fill=BG)
    img.alpha_composite(draw_dog(S, scale))
    return img


def main():
    os.makedirs("icons", exist_ok=True)
    normal = make_icon(1024, 1.00, rounded=True)     # 普通：圆角 + 大狗狗
    mask   = make_icon(1024, 0.72, rounded=False)    # maskable：铺满 + 缩小
    apple  = make_icon(1024, 0.85, rounded=False)    # apple：方形（iOS 自己裁圆角）

    def save(img, sz, name):
        img.resize((sz, sz), Image.LANCZOS).save(os.path.join("icons", name))
        print("saved", name)

    save(normal, 512, "icon-512.png")
    save(normal, 192, "icon-192.png")
    save(normal, 32,  "favicon-32.png")
    save(mask,   512, "icon-maskable-512.png")
    save(apple,  180, "icon-180.png")
    print("done")


if __name__ == "__main__":
    main()
