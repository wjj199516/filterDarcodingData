from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def getFamilyLinks（volUrl）:
    familyUrls = []
    for url in volUrls:
        html = urlopen（"http://foc.eflora.cn/" + url）
        bsObj = BeautifulSoup（html， "lxml"）
        linksObj = bsObj.findAll（"a"， {"href": re.compile（"^（content\.aspx\?TaxonId=）[0-9]+$"）}）
        links = [link["href"] for link in linksObj]
        familyUrls.extend（links）
    return familyUrls
def getVols（url）:
    html = urlopen（"http://foc.eflora.cn/" + url）
    bsObj = BeautifulSoup（html， "lxml"）
    linksObj = bsObj.findAll（"a"， {"href": re.compile（"^（volume\.aspx\?num=）[0-9]+"）}）
    links = [link["href"] for link in linksObj]
    return links
def getLinks（url）:
    html = urlopen（"http://foc.eflora.cn/content.aspx?TaxonID=" + url）
 
    bsObj = BeautifulSoup（html，"lxml"）
    linksObj = bsObj.find（"table"，{"align":"left"}）.findAll（"a"， {"href":re.compile（"^（content\.aspx\?TaxonI（D|d）=）[0-9]+"）}）
    if linksObj == []:
        return bsObj
    else:
        links = [link["href"] for link in linksObj]
        numbers = set（）
        for link in links:
            pattern = re.compile（'[0-9]+'， re.S）
            number = re.search（pattern，link）
            numbers.add（number.group（0））
        return numbers
def filter（urls）:
    global gotten_page
    global went_link
    global file
    newurls = set（）
    for url in urls:
        if url not in gotten_page and url not in went_link:
            result = getLinks（url）
            print（type（result））
            if type（result） == set:
                newurls = newurls | result
                print（url）
                went_link.add（url）
            else:
                name = result.find（"span"，{"id":"Label4"}）.find（"b"）.get_text（）
                print（url）
                print（name）
                file.write（name + '\n'）
                gotten_page.add（url）
    new =  list（newurls）
    newu = [num for num in new if len（num） >= 5 ]
    return newu
def getNextLink（bsObj）:
    ListlinkObj = bsObj.find（"span"，{"id":"Label10"}）.find（"a"， {"href":re.compile（"^（Familylist\.aspx\?Taxon_num=）[0-9]+"）}）
    if not ListlinkObj:
        linksObj = bsObj.find（"span"，{"id":"Label10"}）.findAll（"a"，{"href":re.compile（"^（content\.aspx\?TaxonI（D|d）=）[0-9]+"）}）
        links = [link['href'] for link in linksObj]
        print（links）
        return links
    else:
        print（ListlinkObj['href']）
        return ListlinkObj['href']
def getFamilyName（url）:
    link = 'http://foc.eflora.cn/' + url
    html = urlopen（link）
    bsObj = BeautifulSoup（html， "lxml"）
    name = bsObj.find（"span"，{'id':'Label4'}）.find（'b'）.get_text（）
    return name
def makeSureFamily（url）:
    link = 'http://foc.eflora.cn/' + url
    html = urlopen（link）
    bsObj = BeautifulSoup（html， "lxml"）
    familyName = bsObj.find（"span"，{'id':'Label17'}）.find（"a"）.get_text（）
    print（familyName）

def getListLink（link）:
   url = 'http://foc.eflora.cn/' + link
   html = urlopen（url）
   bsObj = BeautifulSoup（html， "lxml"）
   generaslist = bsObj.find（'table'， {'class': 'tb_family'}）.findAll（"a"， {
       "href": re.compile（"^（content\.aspx\?TaxonI（D|d）=）[0-9]+"）}）
   generasurl = [genera['href'] for genera in generaslist]
   return generasurl
def getListLink2（link）:
   url = 'http://foc.eflora.cn/' + link
   html = urlopen（url）
   bsObj = BeautifulSoup（html， "lxml"）
   generaslist = bsObj.find（'table'， {'class': 'tb_family'}）.findAll（"a"， {
       "href": re.compile（"^（content\.aspx\?TaxonI（D|d）=）[0-9]+"）}）
   generasurl = []
   for n in generaslist:
       if decideIfNone（n['href']） == 'Yes':
           print（n）
           generasurl.append（n.get_text（））
   return generasurl
def pageNumber（link）:
    url = 'http://foc.eflora.cn/' + link
    html = urlopen（url）
    bsObj = BeautifulSoup（html， "lxml"）
    generaUrl = bsObj.find（'span'， {'id': 'Label11'}）.findAll（'a'）
    if generaUrl:
        s = generaUrl[-2]['href']
        npattern = re.compile（'\?page=（[0-9]+）'）
        n = re.findall（npattern， s）
        nn = int（n[0]）
        return nn
    else:
        return None
def getshujiurl（url）:
    shu = []
    nn = pageNumber（url）
    if nn:
        for i in range（1， nn + 1）:
            ss = url.split（'?'）
            new = ss[0] + '?page=' + str（i） + '&' + ss[1]
            generaurls = getListLink（new）
            shu += generaurls
        return shu
    else:
        return getListLink（url）
def getshujiurl2（url）:
    shu = []
    nn = pageNumber（url）
    if nn:
        for i in range（1， nn + 1）:
            ss = url.split（'?'）
            new = ss[0] + '?page=' + str（i） + '&' + ss[1]
            generaurls = getListLink2（new）
            shu += generaurls
        return shu
    else:
        return getListLink2（url）

def shujiurl（familyurl）:
    Url = 'http://foc.eflora.cn/' + familyurl
    html = urlopen（Url）
    bsObj = BeautifulSoup（html， "lxml"）
    generaList = getNextLink（bsObj）
    if type（generaList） == str:
        shujiurl = getshujiurl（generaList）
        return shujiurl
    else:
        return generaList
def decideIfNone（link）:
    url = "http://foc.eflora.cn/" + link
    html = urlopen（url）
    bsObj = BeautifulSoup（html， "lxml"）
    content = bsObj.findAll（"tr"，{"bgcolor":"#ffffff"}）
    yiming = content[0].get_text（）.strip（）
    neirong = content[1].get_text（）.strip（）
    if yiming or neirong:
        return 'Yes'
    else:
        return 'No'
def getSpeciesName（generaUrl）:
    Url = 'http://foc.eflora.cn/' + generaUrl
    html = urlopen（Url）
    bsObj = BeautifulSoup（html， "lxml"）
    one = bsObj.find（'span'， {'id': 'Label10'}）
    if one:
        two = one.find（"a"， {"href":re.compile（"^（Familylist\.aspx\?Taxon_num=）[0-9]+"）}）
        if not two:
            three = one.findAll（"a"， {"href": re.compile（"^（content\.aspx\?TaxonI（D|d）=）[0-9]+"）}）
            names = []
            for n in three:
                if decideIfNone（n['href']） == 'Yes':
                    print（n）
                    names.append（n.find（"i"）.get_text（））
            return names
        else:
            print（two['href']）
            return two['href']
    else:
        return one
def sss（url）:
    species = getSpeciesName（url）
    if species:
        if type（species） == str:
            return getshujiurl2（species）
        else:
            return species
    else:
        return []
def all（generaList）:
    list = []
    for url in generaList:
        part = sss（url）
        list += part
    return list
#print（getSpeciesName（'content.aspx?TaxonId=317304'））
#print（getListLink2（'Familylist.aspx?Taxon_num=104853'））
#familyname = open（"foc/focFamilyName"，"w"）
#volUrls = getVols（""）
#familyUrls = getFamilyLinks（volUrls）
#for url in familyUrls:
#    familyname.write（url + "\n"）
filefamily = open（"foc/focFamilyName"，"rU"）
while True:
    line = filefamily.readline（）
    if line:
        familyUrl = line[:-1]
        print（familyUrl）
        familyname = getFamilyName（familyUrl）
        print（familyname）
        file = open（'20160921focFromWeb/' + familyname， "w"）
        gene = shujiurl（familyUrl）
        print（gene）
        spe = all（gene）
        for speName in spe:
            file.write（speName + '\n'）
        file.close（）
    else:
        break
