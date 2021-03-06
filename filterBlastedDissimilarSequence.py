import os
import sqlite3
from ete3 import *
from Bio.Blast import NCBIXML
import dbm

def get_ncbid_for_name（cursor， name）:
    cursor.execute（"select ncbi_id from taxonomy where name = '"+name+"';"）
    ttax_id = None
    for j in cursor:
        ttax_id = str（j[0]）
    return ttax_id
def get_locus_for_ncbi_id（cursor， ncbi_id）:
    c.execute（"select locus from sequence where ncbi_id = ?"， （ncbi_id，））
    locus = []
    for j in cursor:
        locus.append（str（j[0]））
    return locus
def get_seq_for_locus（cursor， locus）:
    c.execute（"select seq from sequence where locus = '"+locus+"';"）
    seq = None
    for j in cursor:
        seq = str（j[0]）
    return seq
def delete_wrong_locus（name）:
    file = open（'/Users/Simon/Documents/DATADIARY/20180402/物种序列存放'， 'w'）
    ncbi_id = get_ncbid_for_name（c， name）
    print（ncbi_id）
    locuses = get_locus_for_ncbi_id（c， ncbi_id）
    print（locuses）
    #只包含一个序列的物种
    if len（locuses） == 1:
    #包含两个以上序列的物种
    #if len（locuses） >= 2:
        for l in locuses:
            seq = get_seq_for_locus（c， l）
            file.write（'>' + l + '\n' + seq + '\n'）
        file.close（）
        cmd = "blastn -db /Users/Simon/Documents/DATADIARY/20180402/AllrbcL -query /Users/Simon/Documents/DATADIARY/20180402/物种序列存放 -out /Users/Simon/Documents/DATADIARY/20180402/blast结果 -max_target_seqs 2 -outfmt 5"
        os.system（cmd）
        resultfile = open（'/Users/Simon/Documents/DATADIARY/20180402/blast结果'）
        records = NCBIXML.parse（resultfile）
        query_family = db[name.split（' '）[0]]
        wrong_locuses = []
        for record in records:
            i = record.alignments[0]
            line = i.title.split（'|'）[2].split（' '）[1]
            L_n = line.split（'_'）.index（'L'）
            first_locus = '_'.join（line.strip（）.split（'_'）[L_n:]）
            if record.query == first_locus:
                i = record.alignments[1]
                line = i.title.split（'|'）[2].split（' '）[1]
                similar_genus = line.split（'_'）[0]
                similar_family = db[similar_genus]
                if query_family != similar_family:
                    print（'第二个相似序列与本科不相等'， record.query）
                    wrong_locuses.append（record.query）
                    #c.execute（"delete from sequence where locus = '" + record.query + "';"）
            else:
                similar_genus = line.split（'_'）[0]
                similar_family = db[similar_genus]
                if query_family != similar_family:
                    print（'第一个相似序列与本科不相等'， record.query）
                    wrong_locuses.append（record.query）
                    #c.execute（"delete from sequence where locus = '" + record.query + "';"）
        for i in wrong_locuses:
             wrong_locus_file.write（name + '\t' + str（len（locuses）） + '\t' + str（len（wrong_locuses）） + '\t'+ i +'\n'）
db = dbm.open（'/Users/Simon/PycharmProjects/20180225/FOC属名对应科名_根据APG修改'， 'c'）
DB = '/Users/Simon/Documents/DATADIARY/20171023/pln.db'
conn = sqlite3.connect（DB）
c = conn.cursor（）
#wrong_locus_file = open（'/Users/Simon/Documents/DATADIARY/20180402/包含两个以上物种对应的错误序号'，'a'）
wrong_locus_file = open（'/Users/Simon/Documents/DATADIARY/20180402/只包含一个序列物种对应的错误序号'，'a'）
namefile  = open（'/Users/Simon/Documents/DATADIARY/20180402/important_AllrbcL副本_根据db转换后属于FOC'，'rU'）
names = set（）
while True:
    line = namefile.readline（）
    if line:
        if line.startswith（'>'）:
            print（line）
            i = line.split（'_'）.index（'L'）
            name = line.split（'_'）[:i]
            name = ' '.join（name）[1:]
            names.add（name）
    else:
        break
print（len（names））
#checkedfile = open（'/Users/Simon/Documents/DATADIARY/20180402/已检查过的物种.txt'，'rU'）
checkedfile = open（'/Users/Simon/Documents/DATADIARY/20180402/已检查过的只有一个序列的物种.txt'，'rU'）
checkednames = []
while True:
    line = checkedfile.readline（）
    if line:
        checkednames.append（line.strip（））
    else:
        break
checkedfile.close（）
print（len（checkednames））
#checkedfile = open（'/Users/Simon/Documents/DATADIARY/20180402/已检查过的物种.txt'，'a'）
checkedfile = open（'/Users/Simon/Documents/DATADIARY/20180402/已检查过的只有一个序列的物种.txt'，'a'）
n = 0
for name in names:
    if name not in checkednames:
        print（name）
        delete_wrong_locus（name）
        checkedfile.write（name + '\n'）
        n += 1
        print（n）
wrong_locus_file.close（）
namefile.close（）
checkedfile.close（）
name = 'Camellia azalea'
delete_wrong_locus（name）
