from fileManager import ExcelFileManager #导入自定义的Excel读写文件
import urllib3
import json
import datetime

global appId
appId = '414478124'
global pages
#每页50个评论
pages = 10

def searchIOSReview(appId,pageNo):
    url = "https://itunes.apple.com/cn/rss/customerreviews/page="+pageNo+"/id="+appId+"/sortby=mostrecent/json"
    httpManager = urllib3.PoolManager()
    urllib3.disable_warnings()
    req = httpManager.request('GET', url)
    # print(req.data)
    jsonData = json.loads(req.data)
    # print(jsonData)
    array = jsonData['feed']['entry']
    reviewList = []
    for each in array:
        dic = each['author']
        name = dic['name']['label']
        uri = dic['uri']['label']
        version = each['im:version']['label']
        rating = each['im:rating']['label']
        idStr = each['id']['label']
        title = each['title']['label']
        content = each['content']['label']
        i = [uri,name,version,rating,idStr,title,content]
        reviewList.append(i)
    print('第'+pageNo+'页')
    return reviewList

def saveProductData(fileName,SheetName,productList):
    #创建列表
    headRowList = ['uri','name','version','rating','id','title','content']
    ExcelFileManager.creatExcelFile(fileName,SheetName,headRowList)
    print("创建文件成功")
    #保存数据
    ExcelFileManager.addDataToExcelFile(fileName,SheetName,productList)
    print("保存数据成功")

if __name__ == '__main__':
    allPList = []
    for i in range(0,pages):
        plist = searchIOSReview(appId,str(i+1))
        allPList += plist

    fileName = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    saveProductData(fileName,'iOS',allPList)

