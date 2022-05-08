'''
电脑壁纸嵌入式便笺 v1.2
作者：z.yf@pku.edu.cn
GitHub: https://github.com/pku-zyf/wallpaper_note
最后更新：2022-05-08
致谢：jxr
'''

import os
from os.path import join
from PIL import Image, ImageDraw, ImageFont
import win32api, win32con, win32gui
import time

PATH = os.getcwd()
FONT_PATH = "C:\Windows\Fonts"
NOTE_PATH = join(PATH, "notes")

def search_txt_files(path):
    num = 20200001    # 0001号便笺需要提前新建好
    while True:
        new_txt = "notes_{}.txt".format(num)
        if not os.path.exists(join(path, new_txt)):
            old_txt = "notes_{}.txt".format(num - 1)
            return [old_txt, new_txt]
        else:
            num += 1

def get_lines(txt):
    with open(join(NOTE_PATH, txt), 'r', encoding="utf-8") as f:
        lines = f.readlines()
    return lines

def renew_notes(old_txt, new_txt, prefix):
    lines = get_lines(old_txt)
    while True:
        print("当前的便笺内容为：")
        for num in range(len(lines)):    # 逐行输出便笺内容，前面加上行号
            print("\t[{}] {}".format(num + 1, lines[num]))
        renew = input("您接下来是否要更新便笺？[Y/N] ")
        if str.lower(renew) == 'y':
            operation = input("您是要删除一行还是要添加一行？[D/A] ")
            if str.lower(operation) == 'd':
                if len(lines) == 1:
                    print("您必须先新增一行再进行删除操作！")
                else:
                    del_num = input("请输入您要删除第几行？")
                    if del_num.isdigit():
                        if 1 <= int(del_num) <= len(lines):
                            del lines[int(del_num) - 1]
                        else:
                            print("您的输入有误，请检查！")
                    else:
                        print("您的输入有误，请检查！")
            elif str.lower(operation) == 'a':
                add_num = input("您要在第几行后新增一行？如果添加在便笺最后，请直接回车。")
                if add_num.isdigit() or add_num == "":
                    location = len(lines) if add_num == "" else int(add_num)
                    if 0 <= location <= len(lines):
                        add_line = input("请输入您要新增的内容：")
                        lines.insert(location, "{}{}\n".format(prefix, add_line))
                    else:
                        print("您的输入有误，请检查！")
                else:
                    print("您的输入有误，请检查！")
            else:
                print("您的输入有误，请检查！")
        elif str.lower(renew) == 'n':
            break
        else:
            print("您的输入有误，请检查！")
    with open(join(NOTE_PATH, new_txt), 'w+', encoding="utf-8") as f:
        f.writelines(lines)

def add_notes_to_pic(pic, lines, wallpaper):

    img = Image.open(join(PATH, pic))
    width, height = img.width, img.height    # 最好是1920, 1080
    size = 26    # 字号（好像是像素？）
    spacing = 13    # 行距
    main_font = ImageFont.truetype(join(FONT_PATH, "FZCKJW.TTF"), size)
        # 方正硬笔楷书简体："FZYBKSJW.TTF"
        # 方正粗楷简体："FZCKJW.TTF"
    main_color = (242, 236, 222)
        # 缟色：(242, 236, 222)
    total_columns = 3    # 把屏幕分3列
    # start_y = (1 - 1 / 2) * height    # 设置打印文字的高度
    start_y = (1 - 17 / 20) * height    # 偏上的布局
    max_line = int((height - start_y - 50) / (size + spacing))    # Win10底部状态栏高度约50
    columns = len(lines) // max_line + 1 if len(lines) % max_line else len(lines) // max_line    # 算一共需要几列，不能超过3列
    for col in range(columns):
        notes = ''.join(lines[max_line * col : len(lines)]) if col == columns - 1 else ''.join(lines[max_line * col : max_line * col + max_line])    # 便笺切片
        # start_x = (total_columns - columns + col) / total_columns * width    # 起始的横坐标，默认居右
        start_x = 1 / 6 * width    # 偏左的起始横坐标
        starting_point = (start_x, start_y)
        draw = ImageDraw.Draw(img)
        draw.text(
            starting_point,    # 起始点
            notes,    # 文字
            font = main_font,    # 字体
            fill = main_color,    # 颜色
            spacing = spacing    # 行距
        )
    img.save(join(PATH, wallpaper))

def set_wall_paper(wallpaper):
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)        # 打开注册表
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "2")    # 0=居中，1=平铺，2=拉伸
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")    # 0=关闭瓷砖平铺，1=开启瓷砖平铺
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, join(PATH, wallpaper), win32con.SPIF_SENDWININICHANGE)    # 设置桌面

def exit_app():
    print("桌面便笺更新成功，程序稍后将自动退出！")
    time.sleep(5)

def main():
    old_txt, new_txt = search_txt_files(NOTE_PATH)
    renew_notes(old_txt, new_txt, "▲ ")
    note_lines = get_lines(new_txt)
    add_notes_to_pic("background.bmp", note_lines, "wallpaper.bmp")
    set_wall_paper("wallpaper.bmp")
    exit_app()
    
if __name__ == '__main__':
    main()
    