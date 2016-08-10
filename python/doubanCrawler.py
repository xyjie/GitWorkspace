import requests
import lxml.html
import csv

doubanUrl = 'https://movie.douban.com/top250?start={}&filter='

def getSource(url):
    # head = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"}
    # content = requests.get(url, headers=head)
    content = requests.get(url)
    content.encoding = 'utf-8'
    return content.content

def geteveryItem(source):
    movieList = []
    selector = lxml.html.document_fromstring(source)
    # movieItemList获取到25个元素
    movieItemList = selector.xpath('//div[@class="item"]')
    for each in movieItemList:
        movieDict = {}
        content = each.xpath('div[@class="info"]/div[@class="hd"]/a/span[@class="title"]/text()')
        othertitle = each.xpath('div[@class="info"]/div[@class="hd"]/a/span[@class="other"]/text()')
        contentlink = each.xpath('div[@class="info"]/div[@class="hd"]/a/@href')
        actor = each.xpath('div[@class="info"]/div[@class="bd"]/p[@class=""]/text()')
        grade = each.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')
        peoplenum = each.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[4]/text()')
        instruct = each.xpath('div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span[@class="inq"]/text()')
        picture = each.xpath('div[@class="pic"]/a/img/@src')

        movieDict['content'] = ''.join(content + othertitle)
        movieDict['contentlink'] = contentlink
        movieDict['actor'] = ''.join(actor).replace('\n','').replace(' ','')
        movieDict['grade'] = grade
        movieDict['peoplenum'] = peoplenum
        if instruct:
            movieDict['instruct'] = instruct
        else:
            movieDict['instruct'] = '没有简介'
        movieDict['picture'] = picture


        movieList.append(movieDict)
    return movieList


def writeData(movieList):
    with open('doubanmovie.csv','w',encoding = 'utf-8',newline='') as f:
        writer = csv.DictWriter(f,fieldnames=['content','contentlink','actor','grade','peoplenum','instruct','picture'])
        writer.writeheader()
        for each in movieList:
            writer.writerow(each)

if __name__ == '__main__':
    movieList2 = []
    for i in range(10):
        pageLink = doubanUrl.format(i * 25)
        source = getSource(pageLink)
        movieList2 += geteveryItem(source)
    print(len(movieList2))
    movieList = sorted(movieList2, key = lambda k:k['grade'],reverse=True)
    writeData(movieList)









