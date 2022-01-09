import enum
import re
import json
import argparse
import copy

parser = argparse.ArgumentParser(prog='findloop', prefix_chars='-', description='find nature loops in basic blocks',
                                 epilog="before using, check the input file")
parser.add_argument(
    'filename', help='the filename of input json', type=str, nargs=1)

cond_f = {"==": lambda x, y: x == y, "!=": lambda x, y: x != y, ">=": lambda x, y: x >=
          y, "<=": lambda x, y: x <= y, ">": lambda x, y: x > y, "<": lambda x, y: x < y}
arith_f = {"+": lambda x, y: x+y, "-": lambda x, y: x-y, "*": lambda x,
           y: x*y, "/": lambda x, y: x//y, "%": lambda x, y: x % y}
eserved_word = {"HALT", "=", "+", "-", "*", "/", "%", "?",
                ":", "!:", ">", "<", ">=", "<=", "==", "!=", "[", "]"}
reg = re.compile('^[0-9]+$')

if __name__ == "__main__":
    # 读文件
    args = parser.parse_args()
    filename = args.filename[0]
    with open(filename, "r") as fp:
        vm_blk = json.load(fp)
    blocks = vm_blk["blocks"]
    for n, b in blocks.items():
        print("# BLOCK {}".format(n))
        vers = {}
        ssa_code = []
        for line in b["code"]:
            symbols = line.split(" ")
            # print(symbols)
            var_names = [v for v in symbols if (v not in eserved_word) and (reg.match(v)==None)]
            # print(var_names)
            for k in var_names:
                if k not in vers:
                    vers[k] = 0
            # print(vers)
            if "=" in symbols:
                for i, v in enumerate(symbols[1:]):
                    if v in vers:
                        symbols[i+1] = symbols[i+1]+"_"+str(vers[v])
                symbols[0] = symbols[0]+"_"+str(vers[symbols[0]]+1)
                vers[var_names[0]] += 1
            elif ":" in line:
                for i, v in enumerate(symbols):
                    if v in vers:
                        symbols[i] = symbols[i]+"_"+str(vers[v])
            print(" ".join(symbols))
            ssa_code.append(" ".join(symbols))
        blocks[n]["ssa_code"] = ssa_code
        print()
    vm_blk["blocks"] = blocks
    new_file = re.sub('(.*)\\.json$', r'\g<1>_ssa.json', args.filename[0])
    print("Saving output to:", new_file)
    with open(new_file, "w") as fp:
        json.dump(vm_blk, fp, indent=2)
