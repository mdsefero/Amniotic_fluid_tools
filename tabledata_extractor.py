def preamble():
    return ("""
This script extracts lines of interest from a table by sample name/number for example a subset of samples from a metadata file. 
The metadata or other data file must have names/numbers in first column. It assumes headders. There can be no spaces or odd characters
in the sample names. Copy/paste or enter in a list of samples of interest. Whitesapace or most punctuaton (eg -,.:;) are all suitable 

Usage: tabledata_extractor.py -m [TSV separated metadata or other file UTF-8] 

Last Updated: 16 Sept 2021
Maxim Seferovic, seferovi@bcm.edu
""")

import argparse, os.path, collections, re

def save(outdata):
    i = 0
    while os.path.exists(f"{file[0].rsplit('.', 1)[0]}_outlist_{i}.{file[0].rsplit('.', 1)[-1]}"): i += 1
    savename = f"{file[0].rsplit('.', 1)[0]}_out_{i}.{file[0].rsplit('.', 1)[-1]}"
    with open(savename, mode='wt', encoding='utf-8') as f:  
        f.write('\n'.join(outdata))

def extractdata():
    data = collections.defaultdict(list)
    with open (file[0], 'r') as f:
        firstline = f.readline().strip('\n') 
        for line in f: 
            name = (line.split('\t')[0]).strip()
            data[name].append(line.strip('\n'))
             
    outdata = [firstline]
    while True:
        choice = input(f"""
\n{chr(10)} Input number(s)/name(s) to recall from metadata or other file. (Enter 'B' to go back)
>>> """) 
        samples = re.split('[;:,.\'\"|\s\-]', choice)
        samples[:] = [x for x in samples if x != '']
        print ('\nInterpreted list of samples of interest:\n%s' % samples)
        if choice.upper() == "B": return
        elif choice == "": continue
        else: 
            for sample in samples: 
                outdata.append(data.get(sample)[0])
         
            while True:
                choice = input(f"\n{chr(10)}(S)ave or (d)isplay output? >>> ")
                if choice.upper() == "S": 
                    save(outdata)
                    break
                elif choice.upper() == "D": 
                    for i in outdata: print(i)
                    break
                else: continue
            return

def main ():
    extractdata()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=print(preamble()))
    parser.add_argument('-m',  '--metadata', nargs = 1, required=True, type=str, dest='in_file')
    args = parser.parse_args()
    file = args.in_file
    main()