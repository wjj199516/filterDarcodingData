from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import dbm
import urllib.error
import sqlite3

def from_genera_to_family（genera）:
    print（genera）
    url = "http://foc.eflora.cn/search.aspx?k="+genera+"&id=1"
    print（url）
    try:
        html = urlopen（url）
        bsObj = BeautifulSoup（html， "lxml"）
        linksObj = bsObj.find（"a"， {"href": re.compile（"^（content\.aspx\?TaxonI（D|d）=）[0-9]+"）}）
        try:
            if linksObj.get_text（）.strip（） == genera:
                nexturl = 'http://foc.eflora.cn/'+linksObj['href']
                print（nexturl）
                nexthtml = urlopen（nexturl）
                nextbsObj = BeautifulSoup（nexthtml， "lxml"）
                familyname = nextbsObj.find（"span"，{"id":"Label17"}）.find（"a"）.get_text（）.strip（）
                print（familyname）
                db[genera] = familyname
                genera_to_familyfile.write（genera + '\t' + familyname +'\n'）
                checked_generafile.write（genera + '\n'）
            else:
                print（genera + 'is not what I wanted'）
                problem_generafile.write（genera +'\n'）
        except AttributeError:
            not_foundfile.write（genera +'\n'）
    except UnicodeEncodeError:
        not_foundfile.write（genera + '\n'）
    except urllib.error.HTTPError:
        not_foundfile.write（genera + '\n'）
FOCfile = open（'/Users/Simon/Documents/DATADIARY/20170215/Web和Pdf版FOC名称汇总'，'rU'）
generafile = open（'/Users/Simon/Documents/DATADIARY/20170919/FOC属名'，'w'）
generaSet = set（）
while True:
    line  = FOCfile.readline（）
    if line:
        genera = line.split（' '）[0]
        if genera not in generaSet:
            generafile.write（genera+'\n'）
            generaSet.add（genera）
    else:
        break
print（len（generaSet））
db = dbm.open（'FOC属名对应科名'，'c'）
generafile = open（'/Users/Simon/Documents/DATADIARY/20170919/FOC属名'，'rU'）
checked_generafile = open（'/Users/Simon/Documents/DATADIARY/20170919/已得到科名FOC属名'，'rU'）
checked_genera = checked_generafile.read（）
checked_generafile.close（）
problem_generafile = open（'/Users/Simon/Documents/DATADIARY/20170919/出现问题的FOC属名'，'rU'）
problem_genera = problem_generafile.read（）
problem_generafile.close（）
not_foundfile = open（'/Users/Simon/Documents/DATADIARY/20170919/北植FOC搜不到的属名'，'rU'）
not_found = not_foundfile.read（）
not_foundfile.close（）
checked_generafile = open（'/Users/Simon/Documents/DATADIARY/20170919/已得到科名FOC属名'，'a'）
genera_to_familyfile = open（'/Users/Simon/Documents/DATADIARY/20170919/FOC科名与属名对应'，'a'）
problem_generafile = open（'/Users/Simon/Documents/DATADIARY/20170919/出现问题的FOC属名'，'a'）
not_foundfile = open（'/Users/Simon/Documents/DATADIARY/20170919/北植FOC搜不到的属名'，'a'）
while True:
    line = generafile.readline（）
    if line:
        if line not in checked_genera and line not in problem_genera and line not in not_found:
            genera = line[:-1]
            from_genera_to_family（genera）
    else:
        break
db = dbm.open（'FOC属名对应科名'，'c'）
family = set（）
for key in db.keys（）:
    family.add（db[key]）
print（len（family））
print（family）
#北植网站出问题的用tropicos下载
db = dbm.open（'FOC属名对应科名'，'c'）
generafile = open（'/Users/Simon/Documents/DATADIARY/20170919/出现问题的FOC属名'，'rU'）
checked_generafile = open（'/Users/Simon/Documents/DATADIARY/20170919/出现问题的FOC属名通过tropicos解决.txt'，'rU'）
checked_genera = checked_generafile.read（）
checked_generafile.close（）
checked_generafile = open（'/Users/Simon/Documents/DATADIARY/20170919/出现问题的FOC属名通过tropicos解决.txt'，'a'）
genera_to_familyfile = open（'/Users/Simon/Documents/DATADIARY/20170919/FOC科名与属名对应'，'a'）
def from_genera_to_family（genera）:
    try:
        url = "http://www.efloras.org/browse.aspx?flora_id=2&name_str="+genera+"&btnSearch=Search"
        print（url）
        html = urlopen（url）
        bsObj = BeautifulSoup（html， "lxml"）
        linksObj = bsObj.find（"a"， {"href": re.compile（"^（florataxon\.aspx\?flora_id=2&taxon_id=）[0-9]+"）}）
        nexturl = 'http://www.efloras.org/' + linksObj['href']
        print（nexturl）
        nexthtml = urlopen（nexturl）
        nextbsObj = BeautifulSoup（nexthtml， "lxml"）
        familyname = nextbsObj.find（"a"， {"href": re.compile（"^（florataxon\.aspx\?flora_id=2&taxon_id=）[0-9]+"）}）.get_text（）.strip（）
        print（familyname）
        db[genera] = familyname
        genera_to_familyfile.write（genera + '\t' + familyname + '\n'）
        checked_generafile.write（genera + '\n'）
    except UnicodeEncodeError:
        pass
    except TypeError:
        pass
while True:
    line = generafile.readline（）
    if line:
        if line not in checked_genera:
            genera = line[:-1]
            from_genera_to_family（genera）
    else:
        break
generafile.close（）
checked_generafile.close（）
genera_to_familyfile.close（）
db = dbm.open（'FOC属名对应科名'，'c'）
def get_taxid_for_name（cursor， name）:
    cursor.execute（"select ncbi_id from taxonomy where name = '"+name+"';"）
    ttax_id = None
    for j in cursor:
        ttax_id = str（j[0]）
    return ttax_id
namefile = open（'/Users/Simon/Documents/DATADIARY/20170215/Web和Pdf版FOC名称汇总'，'rU'）
outfile = open（'/Users/Simon/Documents/DATADIARY/20171106/Web和Pdf版FOC名称汇总中得不到ncbi_id的属名及其科名'，'w'）
outfile2 = open（'/Users/Simon/Documents/DATADIARY/20171106/Web和Pdf版FOC名称汇总中得不到ncbi_id的科名'，'w'）
DB = '/Users/Simon/Documents/DATADIARY/20171023/pln.db'
conn = sqlite3.connect（DB）
c = conn.cursor（）
not_found_id_genus = set（）
while True:
    line = namefile.readline（）
    if line:
        name = line.strip（）
        genus = name.split（' '）[0]
        id = get_taxid_for_name（c，genus）
        if id == None and genus not in not_found_id_genus:
            #print（genus）
            try :
                family = db[genus]
                family = str（family）[2:-1]
                family_id = get_taxid_for_name（c，family）
                outfile.write（genus+'\t'+family+'\n'）
                not_found_id_genus.add（genus）
                family_id = get_taxid_for_name（c， family）
                if family_id == None:
                    print（family）
                    outfile2.write（family+'\n'）
            except KeyError:
                not_found_id_genus.add（genus）
    else:
        break
#print（len（not_found_id_genus））


