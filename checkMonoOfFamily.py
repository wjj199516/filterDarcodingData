from ete3 import *

newtname = '/Users/Simon/Documents/DATADIARY/20180405/new/RAxML_bipartitions.rbcL_withfamilyname.tree_去除missing序列.tree'
newt = Tree（newtname）
families = set（）
for leaf in newt:
    family = leaf.name.split（'_'）[0]
    families.add（family）
print（'树包含的tip个数'，len（newt））
print（'树包含的科个数'，len（families））
# 检查科的单系
def search_by_name（node， family）:
    matches = []
    for leaf in node:
        if leaf.name.startswith（family）:
            matches.append（leaf.name）
    return matches
file = open（newtname+"_monophyly.txt"，'w'）
nonmonofile = open（newtname+"_nonmonofamily.txt"，'w'）
for family in families:
    print（family）
    matches = search_by_name（newt， family）
    mono = newt.check_monophyly（values=matches， target_attr='name'， unrooted=True）
    print（family， mono）
    file.write（family + '\t' + str（mono） + '\n'）
    if str（mono）[1:6] == 'False':
        nonmonofile.write（family + '\n'）
