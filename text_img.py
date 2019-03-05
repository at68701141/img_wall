from PIL import Image
import os,sys
import random
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mw', default=100, help='照片的长宽', type=int)
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    mw = args.mw
    raw_img = Image.open('./_raw.png')
    raw_img_1 = raw_img.convert('1')
    raw_img_1.save("./_deal.jpg")
    out_width = raw_img_1.size[0]
    out_height = raw_img_1.size[1]

    text_img = Image.open("./_deal.jpg")
    rows = text_img.size[0] + 1
    columns = text_img.size[1] + 1
    imgs = 0
    for y in range(1,columns):
        for x in range(1,rows):
            if 0 == text_img.getpixel((x-1,y-1)):
                imgs += 1
    print('need imgs:',imgs)

    #搜索路径下所有图片
    dir_list = os.listdir("./")
    list_fromImage = []
    for i in dir_list:
        if -1 == i.find('.py'):
            if -1 == i.find('_raw') and -1 == i.find('_deal') and -1 == i.find('_out'):
                fromImagetmp = Image.open("./"+i)
                list_fromImage.append(fromImagetmp)
    print('total imgs:',len(list_fromImage))

    #选一张画布，关键确定画布的大小
    toImage = Image.new('RGBA',(out_width*mw,out_height*mw))
    for y in range(1,columns):
        for x in range(1,rows):
            try:
                if 255 == text_img.getpixel((x-1,y-1)):
                    pass
                elif 0 == text_img.getpixel((x-1,y-1)):
                    #选取照片，按照自己想要的样式，依次选取
                    fromImage = list_fromImage[random.randint(0, len(list_fromImage)-1)].copy()
                    # fromImage = fromImage.rotate(random.randint(0, 360))
                    #粘贴照片，将照片粘贴到设计的位置上 
                    fromImage = fromImage.resize((mw,mw),Image.ANTIALIAS) 
                    toImage.paste(fromImage,((x-1)*mw,(y-1)*mw))
            except IOError:
                pass
    toImage.save('./_out.png')

if __name__ == '__main__':
    main()