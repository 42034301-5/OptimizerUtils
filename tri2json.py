import re
import json
import argparse

parser = argparse.ArgumentParser(prog='tri2json', prefix_chars='-', description='read the txt code file and convert it to optvm json',
                                 epilog="before using, check the txt file")
parser.add_argument(
    'filename', help='the filename of input json', type=str, nargs=1)

cond_f = {"==": lambda x, y: x == y, "!=": lambda x, y: x != y, ">=": lambda x, y: x >=
          y, "<=": lambda x, y: x <= y, ">": lambda x, y: x > y, "<": lambda x, y: x < y}
arith_f = {"+": lambda x, y: x+y, "-": lambda x, y: x-y, "*": lambda x,
           y: x*y, "/": lambda x, y: x//y, "%": lambda x, y: x % y}
eserved_word = {"HALT","=","+","-","*","/","%","?",":","!:",">","<",">=","<=","==","!=","[","]"}
reg = re.compile('^[0-9]+$')

if __name__ == "__main__":
    args = parser.parse_args()
    flines = []
    with open(args.filename[0],"r") as fp:
        flines = fp.readlines()
    code = [l.replace("\n","") for l in flines]
    # print(code)
    var_table = {}
    for line in code:
        symbols = line.split(" ")
        var_names = [v for v in symbols if v not in eserved_word]
        for k in var_names:
            if k not in var_table:
                var_table[k]={'t':'int','val':eval(k) if (reg.match(k)!=None) else 0}
        if '[' in symbols:
            var_table[symbols[symbols.index('[')-1]]={'t':'int_array','size':0,'val':[]}
    vm_src = {"table":var_table,"code":code}
    new_file = re.sub('(.*)\\.txt$', r'\g<1>.json', args.filename[0])
    print("Saving output to:",new_file)
    with open(new_file,"w") as fp:
        json.dump(vm_src,fp,indent=2)