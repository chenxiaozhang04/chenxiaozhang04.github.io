#!/usr/bin/env python3
"""把 logo 的白色背景抠成透明。

用从图像边缘做 flood fill 的方式：只移除与边框连通的白色背景，
保留 logo 内部的白色区域（不会在图标里戳出透明洞）。

用法：
    python3 make_transparent.py
处理结果会另存为 PNG（带 _t 后缀），不覆盖原图。
"""

from collections import deque

from PIL import Image

# (输入路径, 输出路径)
TASKS = [
    ("images/casia.jpg", "images/casia_t.png"),
    ("images/favicon/115cb2a8573f25e6.jpg", "images/favicon/buaa_t.png"),
]

# 距离纯白的容差：R/G/B 都 >= 255 - THRESH 视为背景白
THRESH = 36

# 裁剪后四周保留的内边距（相对于内容尺寸的比例）
PAD_RATIO = 0.04


def remove_white_bg(in_path, out_path, thresh=THRESH):
    img = Image.open(in_path).convert("RGBA")
    w, h = img.size
    px = img.load()

    def is_bg(x, y):
        r, g, b, _ = px[x, y]
        return r >= 255 - thresh and g >= 255 - thresh and b >= 255 - thresh

    visited = bytearray(w * h)
    q = deque()

    def seed(x, y):
        idx = y * w + x
        if not visited[idx] and is_bg(x, y):
            visited[idx] = 1
            q.append((x, y))

    for x in range(w):
        seed(x, 0)
        seed(x, h - 1)
    for y in range(h):
        seed(0, y)
        seed(w - 1, y)

    while q:
        x, y = q.popleft()
        r, g, b, _ = px[x, y]
        px[x, y] = (r, g, b, 0)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h:
                seed(nx, ny)

    cleared = sum(visited)

    # 按 alpha 通道裁掉四周透明边缘，让 logo 填满画面
    bbox = img.getchannel("A").getbbox()
    if bbox:
        left, top, right, bottom = bbox
        pad = round(max(right - left, bottom - top) * PAD_RATIO)
        left = max(0, left - pad)
        top = max(0, top - pad)
        right = min(w, right + pad)
        bottom = min(h, bottom + pad)
        img = img.crop((left, top, right, bottom))

    img.save(out_path)
    print(f"  {in_path} -> {out_path}  ({cleared} px 透明, 裁剪后 {img.size[0]}x{img.size[1]})")


def main():
    print("抠白底中...")
    for in_path, out_path in TASKS:
        remove_white_bg(in_path, out_path)
    print("完成。")


if __name__ == "__main__":
    main()
