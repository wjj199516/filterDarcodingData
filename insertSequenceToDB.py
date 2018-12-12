import sys
import sqlite3

def get_taxid_for_name（cursor， name）:
    cursor.execute（"select ncbi_id from taxonomy where name = '"+name+"';"）
    ttax_id = None
    for j in cursor:
        ttax_id = str（j[0]）
    return ttax_id
seqfile = open（'/Users/Simon/Documents/DATADIARY/20171023/important_AllrbcL '，'rU'）
outfile = open（'/Users/Simon/Documents/DATADIARY/20171106/important_AllrbcL_not_insert '，'w'）
DB = '/Users/Simon/Documents/DATADIARY/20171023/pln.db'
conn = sqlite3.connect（DB）
c = conn.cursor（）
n = 1
while True:
    line = seqfile.readline（）
    if line:
        if line.startswith（'>'）:
            i = line.split（'_'）.index（'L'）
            name = line.split（'_'）[:i]
            name = ' '.join（name）[1:]
            ncbi_id = get_taxid_for_name（c，name）
            if ncbi_id != None:
                locus = '_'.join（line.strip（）.split（'_'）[i:]）
                print（name， ncbi_id， locus）
                description = name
                lastline = line.strip（）
                print（lastline）
                line = seqfile.readline（）
                seq = line.strip（）
                print（seq）
                c.execute（"INSERT INTO sequence（ncbi_id，locus，accession_id，version_id，description，title，seq） VALUES（?，?，?，?，?，?，?）"，（ncbi_id， locus， locus， locus，description，lastline，seq））
                conn.commit（）
                n += 1
            else:
                outfile.write（line）
                line = seqfile.readline（）
                outfile.write（line）
    else:
        break
print（n）
