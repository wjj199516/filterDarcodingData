from ete3 import *

def find_taxa（node， family）:
    matches = []
    for leaf in node:
       if leaf.name.startswith（family）:
          matches.append（leaf.name）
    return matches
def find_outgroup_percent（node，family）:
    outgroupNumber = 0
    for leaf in node:
       if not leaf.name.startswith（family）:
           outgroupNumber += 1
    return outgroupNumber/len（node）
def find_number_percent（node，family）:
    familyAllNumber = len（find_taxa（t， family））
    familyNodeNumber = len（find_taxa（node， family））
    numberPercent = familyNodeNumber/familyAllNumber
    return 1-numberPercent
def find_outgroup_percent_of_nodes（sorted_node_outgroup_percent）:
    tips_of_nodes = 0
    tips_of_family = 0
    for i in sorted_node_outgroup_percent:
        tips_of_nodes += len（i[0]）
        tips_of_family += len（find_taxa（i[0]， family））
    tips_of_outgroup = tips_of_nodes - tips_of_family
    return tips_of_outgroup/tips_of_nodes
def find_mrca（family，t，threshold）:
    taxa_set = find_taxa（t， family）
    mrca = t.get_common_ancestor（taxa_set）
    #print（find_outgroup_percent（mrca， family））
    if find_outgroup_percent（mrca， family） > threshold:
        node_outgroup_percent = {}
        for node in mrca.children:
            outgroup_percent = find_outgroup_percent（node，family）
            if outgroup_percent != 1:
                minus_number_percent = find_number_percent（node，family）
                mix_percent = outgroup_percent*0.5 + minus_number_percent*0.5
                #print（find_outgroup_percent（node，family））
                node_outgroup_percent[node] = mix_percent
        sorted_node_outgroup_percent = sorted（node_outgroup_percent.items（），key = lambda item:item[1]，reverse=True）
        #print（sorted_node_outgroup_percent）
        while find_outgroup_percent_of_nodes（sorted_node_outgroup_percent） > threshold:
            if len（sorted_node_outgroup_percent） == 1:
                #print（sorted_node_outgroup_percent[0]）
                t = sorted_node_outgroup_percent[0][0]
                return find_mrca（family，t，threshold）
            else:
                sorted_node_outgroup_percent = sorted_node_outgroup_percent[1:]
        delete_node = []
        for i in sorted_node_outgroup_percent:
            if len（find_taxa（i[0]， family）） == 1 and find_outgroup_percent（i[0]， family） > threshold:
                print（find_taxa（i[0]， family）， find_outgroup_percent（i[0]， family））
                delete_node.append（i）
            elif len（find_taxa（i[0]， family）） == 2 and find_outgroup_percent（i[0]， family） > threshold:
                print（find_taxa（i[0]， family）， find_outgroup_percent（i[0]， family））
                delete_node.append（i）
            else:
                pass
                # print（sorted_node_outgroup_percent）
        # print（find_outgroup_percent_of_nodes（sorted_node_outgroup_percent））
        mrcas = []
        for i in sorted_node_outgroup_percent:
            if i not in delete_node:
                mrcas.append（i[0]）
        return mrcas
    else:
        #print（find_outgroup_percent（mrca， family））
        return [mrca]
def return_missing_number（family_mrcas）:
    #missingfile = open（tname + '_missingperfamily.txt' + '_' + str（threshold）， 'w'）
    #missingSummaryFile = open（tname + '_missingSummary.txt' + '_' + str（threshold）， 'w'）
    missingTips = 0
    for family in family_mrcas.keys（）:
        familyAllTip = find_taxa（t， family）
        mrcas = family_mrcas[family]
        familyMrcaTips = []
        for node in mrcas:
            familyMrcaTips += find_taxa（node， family）
        missiingPerfamily = []
        for tip in familyAllTip:
            if tip not in familyMrcaTips:
                missiingPerfamily.append（tip）
                #missingfile.write（family + '\t' + tip + '\n'）
        #missingSummaryFile.write（family + '\t' + str（len（familyAllTip）） + '\t' + str（len（mrcas）） + '\t' + str（len（missiingPerfamily）） + '\n'）
        print（family，len（missiingPerfamily））
        missingTips += len（missiingPerfamily）
    print（'missingTips'，missingTips）
    return （missingTips）
def return_overlap_number（family_mrcas）:
    #overlapfile = open（tname + '_overlapbetweenfamily.txt' + '_' + str（threshold）， 'w'）
    overlap_dic = {}
    compared_family = []
    for family in family_mrcas.keys（）:
        mrcas = family_mrcas[family]
        for otherfamily in family_mrcas.keys（）:
            overlapTaxa = []
            if otherfamily != family:
                if set（[family， otherfamily]） not in compared_family:
                    othermrcas = family_mrcas[otherfamily]
                    for node in mrcas:
                        for othernode in othermrcas:
                            if node == othernode:
                                for leaf in node:
                                    overlapTaxa.append（leaf.name）
                            elif node in othernode:
                                for leaf in node:
                                    overlapTaxa.append（leaf.name）
                            elif othernode in node:
                                for leaf in othernode:
                                    overlapTaxa.append（leaf.name）
                            else:
                                pass
            overlap_dic[family + '_' + otherfamily] = overlapTaxa
            #for name in overlapTaxa:
                #overlapfile.write（family + '_' + otherfamily + '\t' + name + '\t' + str（len（overlapTaxa）） + '\n'）
            compared_family.append（set（[family， otherfamily]））
    overlapnumber = set（）
    for key in overlap_dic.keys（）:
        overlapnumber = overlapnumber|set（overlap_dic[key]）
    return （len（overlapnumber））
tname = '/Users/Simon/Documents/DATADIARY/20180405/new/RAxML_bipartitions.rbcL_withfamilyname.tree_坍塌支持率低的节点_80.tree'
t = Tree（tname）
#nonmonofile = open（tname + '_nonmonofamily.txt'，'rU'）
nonmonofile = open（'/Users/Simon/Documents/DATADIARY/20180405/new/RAxML_bipartitions.rbcL_withfamilyname.tree_nonmonofamily.txt'，'rU'）
nonmonofamilies = []
while True:
    line = nonmonofile.readline（）
    if line:
        nonmonofamilies.append（line.strip（））
    else:
        break
file = open（tname + '_find_threshold.txt'，'w'）
threshold = 0
while threshold <= 0.5:
    print（threshold）
    family_mrcas = {}
    for family in nonmonofamilies:
        #print（family）
        mrcas = find_mrca（family，t，threshold）
        family_mrcas[family] = mrcas
    missing_number = return_missing_number（family_mrcas）
    overlap_number = return_overlap_number（family_mrcas）
    file.write（str（threshold） + '\t' + str（missing_number） + '\t' + str（overlap_number） + '\n'）
    threshold += 0.01









