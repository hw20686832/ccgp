# coding:utf-8
# The verification code recognition
# author: David Wong
import os
import math
from StringIO import StringIO
from PIL import Image

import requests


class VectorCompare:
    def magnitude(self, concordance):
        total = 0
        for word, count in concordance.iteritems():
            total += count ** 2
        return math.sqrt(total)

    def relation(self, concordance1, concordance2):
        topvalue = 0
        for word, count in concordance1.iteritems():
            if word in concordance2:
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))


def iter_letters(im):
    im2 = Image.new("P", im.size, 255)

    for x in range(im.size[1]):
        for y in range(im.size[0]):
            pix = im.getpixel((y, x))
            if pix < 100:
                # these are the numbers to get
                im2.putpixel((y, x), 0)

    inletter = False
    foundletter = False
    start = 0
    end = 0

    for y in range(im2.size[0]):
        for x in range(im2.size[1]):
            pix = im2.getpixel((y, x))
            if pix != 255:
                inletter = True

        if not foundletter and inletter:
            foundletter = True
            start = y

        if foundletter and not inletter:
            foundletter = False
            end = y
            yield start, end
        inletter = False


def buildvector(im):
    d1 = {}

    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1

    return d1


def analyze(imgobj):
    v = VectorCompare()
    iconset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    imageset = []
    for letter in iconset:
        vct = buildvector(Image.open(os.path.join(os.path.dirname(__file__), "letters/%s.gif" % letter)))
        imageset.append({letter: vct})

    im = Image.open(imgobj)
    im = im.convert("P")

    codes = []
    for c in iter_letters(im):
        im3 = im.crop((c[0], 0, c[1], im.size[1]))
        #im3.save("%s.gif" % str(time.time()*1000))
        guess = []
        for image in imageset:
            for x, y in image.iteritems():
                guess.append((v.relation(y, buildvector(im3)), x))

        guess.sort(reverse=True)
        codes.append(guess[0][1])

    return ''.join(codes)


def main():
    pic_url = "http://www.cqgp.gov.cn/commons/image.jsp"
    response = requests.get(pic_url)
    with open('x.jpg', 'wb') as img:
        img.write(response.content)
    imgio = StringIO(response.content)
    code = analyze(imgio)
    print code
    imgio.close()


if __name__ == '__main__':
    main()
