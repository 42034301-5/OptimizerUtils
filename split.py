import re
import json
import argparse

parser = argparse.ArgumentParser(prog='split', prefix_chars='-', description='split optvm json to basic blocks',
                                 epilog="before using, check the input file")
parser.add_argument(
    'filename', help='the filename of input json', type=str, nargs=1)

cond_f = {"==": lambda x, y: x == y, "!=": lambda x, y: x != y, ">=": lambda x, y: x >=
          y, "<=": lambda x, y: x <= y, ">": lambda x, y: x > y, "<": lambda x, y: x < y}
arith_f = {"+": lambda x, y: x+y, "-": lambda x, y: x-y, "*": lambda x,
           y: x*y, "/": lambda x, y: x//y, "%": lambda x, y: x % y}
eserved_word = {"HALT","=","+","-","*","/","%","?",":","!:",">","<",">=","<=","==","!=","[","]"}
reg = re.compile('^[0-9]+$')

if __name__ == "__main__":
    # 读文件
    args = parser.parse_args()
    filename = args.filename[0]
    vm_src = {}
    with open(filename, "r") as fp:
        vm_src = json.load(fp)
    table = vm_src["table"]
    code = vm_src["code"]
    # 开始切
    jump_targets = [table[i.split(" ")[-1]]["val"] for i in code if i.split(" ")[0] in {"?","!:"}]
    after_jump = [n+1 for n,i in enumerate(code) if i.split(" ")[0] in {"?","!:"}]
    split_points = list(set([0]+jump_targets+after_jump+[len(code)]))
    split_points = sorted(split_points)
    blocks_linenum = [(split_points[i-1],split_points[i]-1) for i in range(1,len(split_points))]
    intro_block = {i[0]:n for n,i in enumerate(blocks_linenum)}
    # 切的基本块预览
    for n,b in enumerate(blocks_linenum):
        print("#BLOCK {:3d}".format(n))
        for i in range(b[0],b[1]+1):
            print("{:3d} : {}".format(i,code[i])) 
        print()
    # 构建dict
    blocks = {"summary":{},"blocks":{}}
    blocks["summary"] = {"total_blocks":len(blocks_linenum)}
    for n,b in enumerate(blocks_linenum):
        nxt = [None,None]
        if code[b[1]].split(" ")[0] == "!:":
            nxt[0]=intro_block[table[code[b[1]].split(" ")[1]]["val"]]
        elif code[b[1]].split(" ")[0] == "?":
            nxt[1]=intro_block[table[code[b[1]].split(" ")[5]]["val"]]
            nxt[0]=n+1
        elif code[b[1]]=="HALT":
            pass
        else:
            nxt[0]=n+1
        blocks["blocks"][n]={"line_num":b,"next":tuple(nxt),"code":code[b[0]:b[1]+1]}
    # 找活跃变量
    for n,b in blocks["blocks"].items():
        blines = b["code"]
        used = []
        defd = []
        for s in blines:
            symbols = s.split(" ")
            if "=" in symbols:
                if len(symbols) == 3:
                    if (symbols[2] not in used) and (symbols[2] not in defd):
                        used.append(symbols[2])
                    if (symbols[0] not in used) and (symbols[0] not in defd):
                        defd.append(symbols[0])
                elif symbols[3] == "]":
                    if (symbols[2] not in used) and (symbols[2] not in defd):
                        used.append(symbols[2])
                    if (symbols[5] not in used) and (symbols[5] not in defd):
                        used.append(symbols[5])
                    if (symbols[0] not in used) and (symbols[0] not in defd):
                        defd.append(symbols[0])
                elif symbols[3] == "[":
                    if (symbols[2] not in used) and (symbols[2] not in defd):
                        used.append(symbols[2])
                    if (symbols[4] not in used) and (symbols[4] not in defd):
                        used.append(symbols[4])
                    if (symbols[0] not in used) and (symbols[0] not in defd):
                        defd.append(symbols[0])

                elif symbols[3] in arith_f:
                    if (symbols[2] not in used) and (symbols[2] not in defd):
                        used.append(symbols[2])
                    if (symbols[4] not in used) and (symbols[4] not in defd):
                        used.append(symbols[4])
                    if (symbols[0] not in used) and (symbols[0] not in defd):
                        defd.append(symbols[0])
            elif "?" in symbols:
                    if (symbols[1] not in used) and (symbols[1] not in defd):
                        used.append(symbols[1])
                    if (symbols[3] not in used) and (symbols[3] not in defd):
                        used.append(symbols[3])
        used = [i for i in used if reg.match(i)==None]
        defd = [i for i in defd if reg.match(i)==None]

        blocks["blocks"][n]["defd"] = set(defd)
        blocks["blocks"][n]["used"] = set(used)
        blocks["blocks"][n]["in"] = set([])
        blocks["blocks"][n]["out"] = set([])
    flag = True
    while flag:
        flag = False
        for n,b in blocks["blocks"].items():
            inset = copy.deepcopy(blocks["blocks"][n]["in"])
            inset_ori = copy.deepcopy(blocks["blocks"][n]["in"])
            outset = copy.deepcopy(blocks["blocks"][n]["out"])
            if b["next"][0]!=None:
                outset = outset | blocks["blocks"][b["next"][0]]["in"]
            if b["next"][1]!=None:
                outset = outset | blocks["blocks"][b["next"][1]]["in"]
            inset = blocks["blocks"][n]["used"] | (outset - blocks["blocks"][n]["defd"])
            blocks["blocks"][n]["in"] = inset
            blocks["blocks"][n]["out"] = outset
            if (inset!=inset_ori):
                flag = True
    # 写json
    new_file = re.sub('(.*)\\.json$', r'\g<1>_blk.json', args.filename[0])
    print("Saving output to:",new_file)
    with open(new_file,"w") as fp:
        json.dump(blocks,fp,indent=2)