seq = {}
file = open（'/Users/Simon/Documents/DATADIARY/20170914/important_AllrbcL.fasta'， 'rU'）
while True:
    line = file.readline（）
    if line:
        name = ' '.join（line.split（'_'）[:line.split（'_'）.index（'L'）]）
        print（line）
        if name not in seq.keys（）:
            print（'never show up'）
            lastline = line
            line = file.readline（）
            seq[name] = lastline + line[:-1]
        else:
            lastline = line
            line = file.readline（）
            if len（line[:-1]） > len（seq[name].split（'\n'）[1]）:
                print（'already show， and this is longer'）
                seq[name] = lastline + line[:-1]
    else:
        break
outfile = open（'/Users/Simon/Documents/DATADIARY/20170914/important_LongestrbcL.fasta '， 'w'）
for key in seq.keys（）:
    print（key，seq[key]）
    outfile.write（seq[key]+'\n'）
file.close（）
outfile.close（）
print（len（seq.keys（）））
