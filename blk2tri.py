import re
import json
import argparse

parser = argparse.ArgumentParser(prog='blk2tri', prefix_chars='-', description='convert blk json to tri code txt',
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
    # 读文件
    args = parser.parse_args()
    filename = args.filename[0]
    with open(filename, "r") as fp:
        vm_blk = json.load(fp)
    blocks = vm_blk["blocks"]
    # DFS并分配行号
    stack = ['0']
    visited = ['0']

    line_count = 0
    while len(stack)>0:
        tmp = stack[-1]
        stack.pop()
        blocks[tmp]["entry_line_num"] = line_count
        # print(tmp,":",line_count)
        if "!:" in blocks[tmp]["code"][-1]:
            line_count += len(blocks[tmp]["code"])
        elif blocks[tmp]["code"][-1] == "HALT":
            line_count += len(blocks[tmp]["code"])
        else:
            line_count += len(blocks[tmp]["code"]) + 1

        for i in reversed(blocks[tmp]["next"]) :
            if (i!=None):
                if str(i) not in visited:
                    stack.append(str(i))
                    visited.append(str(i))
    out_code = ['' for i in range(line_count)]
    for n,b in blocks.items():
        if "entry_line_num" not in b.keys():
            continue
        if len(blocks[n]["code"])==1:
            blocks[n]["code"] = list(blocks[n]["code"])
        if b["next"][1]!=None:
            symbols = blocks[n]["code"][-1].split(" ")
            symbols[-1] = str(blocks[str(b["next"][1])]["entry_line_num"])
            blocks[n]["code"][-1] = " ".join(symbols)
        if b["next"][0]!=None:
            if "!:" in blocks[n]["code"][-1]:
                blocks[n]["code"][-1] = "!: {}".format(blocks[str(b["next"][0])]["entry_line_num"])
            else:
                blocks[n]["code"].append("!: {}".format(blocks[str(b["next"][0])]["entry_line_num"]))
        for i,l in enumerate(blocks[n]["code"]):
            out_code[blocks[n]["entry_line_num"]+i] = l
    # 去除无用goto
    opt_goto = {}
    for i,l in enumerate(out_code):
        symbols = l.split(" ")
        if (symbols[0]=="!:") and (int(symbols[-1])==i+1):
            print("{:4d} -   {}  (DEL)".format(i,l))
        else:
            print("{:4d} -   {}".format(i,l))
            opt_goto[i]=symbols
    opt_goto_list = sorted(list(opt_goto.items()))
    line_num_map = {opt_goto_list[i][0]:i for i in range(len(opt_goto_list))}
    retlines = []
    for li in opt_goto_list:
        l = li[1]
        if "!:"==l[0] or "?" == l[0]:
            l[-1] = str(line_num_map[int(l[-1])])
        # print("{:4d} -   {}".format(line_num_map[li[0]]," ".join(l)))
        retlines.append(" ".join(l)+'\n')

    new_file = re.sub('(.*)\\.json$', r'\g<1>_codegen.txt', args.filename[0])
    print("Saving output to:",new_file)
    with open(new_file,"w") as fp:
        fp.writelines(retlines)