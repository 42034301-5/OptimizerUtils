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
        else:
            nxt[0]=n+1
        blocks["blocks"][n]={"line_num":b,"next":tuple(nxt),"code":code[b[0]:b[1]+1]}
    # 写json
    new_file = re.sub('(.*)\\.json$', r'\g<1>_blk.json', args.filename[0])
    print("Saving output to:",new_file)
    with open(new_file,"w") as fp:
        json.dump(blocks,fp,indent=2)