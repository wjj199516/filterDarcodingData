from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager， process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open
from bs4 import BeautifulSoup
import re

def readPDF（pdfLink）:
    pdfFile = urlopen（pdfLink）
    rsrcmgr = PDFResourceManager（）
    retstr = StringIO（）
    laparams = LAParams（）
    device = TextConverter（rsrcmgr， retstr， laparams=laparams）
    process_pdf（rsrcmgr， device， pdfFile）
    device.close（）
    content = retstr.getvalue（）
    retstr.close（）
    pdfFile.close（）
    return content
def getFileName（pdfLink）:
    fileName = pdfLink.split（'/'）[-1].split（"."）[0]
    return fileName
def getNames（content，fileName）:
    pattern1 = re.compile（'（\n[0-9]+\. [A-Z][a-zë\-]+ [a-z\-]+ ）（[A-Z]|\（）'）
    pattern2 = re.compile（'（\n[0-9]+[a-z]\. [A-Z][a-zë\-]+ [a-z\-]+ （var.|f.|subsp.） [a-z]+）'）
    results1 = re.findall（pattern1， content）
    results2 = re.findall（pattern2， content）
    file = open（'20160929/' + fileName ， "w"）
    for result in results1:
        print（" ".join（result[0].split（' '）[1:3]））
        file.write（" ".join（result[0].split（' '）[1:3]） + '\n'）
    for result in results2:
        print（" ".join（result[0].split（' '）[1:5]））
        file.write（" ".join（result[0].split（' '）[1:5]） + '\n'）
def getVols（url）:
    html = urlopen（"http://foc.eflora.cn/" + url）
    bsObj = BeautifulSoup（html， "lxml"）
    linksObj = bsObj.findAll（"a"， {"href": re.compile（"^（volume\.aspx\?num=）[0-9]+"）}）
    links = [link["href"] for link in linksObj]
    return links
def getFamilyLinks（volUrl）:
    familyUrls = []
    for url in volUrls:
        html = urlopen（"http://foc.eflora.cn/" + url）
        bsObj = BeautifulSoup（html， "lxml"）
        linksObj = bsObj.findAll（"a"， {"href": re.compile（"^（content\.aspx\?TaxonId=）[0-9]+$"）}）
        links = [link["href"] for link in linksObj]
        familyUrls.extend（links）
    return familyUrls
def getPdfLink（familyLink）:
    html = urlopen（familyLink）
    bsObj = BeautifulSoup（html， "lxml"）
    linksObj = bsObj.find（"a"， {"href": re.compile（"http://www\.eflora\.cn/foc/pdf/[A-Z][a-z]+\.pdf"）}）
    if linksObj:
        pdfLink = linksObj["href"]
        return pdfLink
    else:
        return None
#volUrls = getVols（""）
#familyUrls = getFamilyLinks（volUrls）
#file = open（'familyUrls0929'，"w"）
#for url in familyUrls:
#file.write（url + '\n'）
file = open（'familyUrls0929'，"rU"）
familyUrls = []
while True:
    line = file.readline（）
    if line:
       familyUrls.append（line[:-1]）
    else:
        break
#for url in familyUrls:
#    print（url）
#    familyLink = 'http://foc.eflora.cn/' + url
#    print（familyLink）
#    pdfLink = getPdfLink（familyLink）
#    if pdfLink:
#        content = readPDF（pdfLink）
#        fileName = getFileName（pdfLink）
#        print（fileName）
#        getNames（content，fileName）
#pdfLink = 'http://flora.huh.harvard.edu/china/mss/volume09/Platanaceae.PDF'
pdfLink = 'http://flora.huh.harvard.edu/china/mss/volume09/Rosaceae.PDF'
content = readPDF（pdfLink）
fileName = getFileName（pdfLink）
print（fileName）
getNames（content，fileName）
