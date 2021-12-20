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
eserved_word = {"HALT","=","+","-","*","/","%","?",":","!:",">","<",">=","<=","==","!=","[","]"}
reg = re.compile('^[0-9]+$')

if __name__ == "__main__":
    # 读文件
    args = parser.parse_args()
    filename = args.filename[0]
    with open(filename, "r") as fp:
        vm_blk = json.load(fp)
    blocks = vm_blk["blocks"]
    # 计算基本块的前驱
    for n,b in blocks.items():
        blocks[n]["pre"] = set()
    for n,b in blocks.items():
        for i in b["next"]:
            if i!=None:
                blocks[str(i)]["pre"] = blocks[str(i)]["pre"] | {n}
    # 构建支配关系
    for n,b in blocks.items():
        blocks[n]["dom"] = set([str(i) for i in range(vm_blk["summary"]["total_blocks"])])
    blocks[str(0)]["dom"] = {'0'}
    flag = True
    i = 0
    while flag:
        flag = False
        i+=1
        for n,b in blocks.items():
            if n!='0':
                domset_ori = copy.deepcopy(blocks[n]["dom"])
                domset = copy.deepcopy(blocks[n]["dom"])
                preset = set([str(i) for i in range(vm_blk["summary"]["total_blocks"])])
                for j in blocks[n]["pre"]:
                    preset = preset & blocks[j]["dom"]
                domset = {n} | preset
                if (domset!=domset_ori):
                    flag = True
                blocks[n]["dom"] = domset
    for n,b in blocks.items():
        if len(b["pre"])==0 and n!='0':
            blocks[n]["dom"] = set()
    # 寻找回边
    back_edge = []
    for n,b in blocks.items():
        for i in b["dom"]:
            if int(i) in b["next"]:
                back_edge.append((n,i))
    back_edge = list(set(back_edge))
    # 寻找回边对应的自然循环
    loops = []
    for le in back_edge:
        stack = [le[0]]
        loop = {le[0],le[1]}
        while len(stack)>0:
            m=stack[-1]
            stack.pop()
            for p in blocks[m]["pre"]:
                if p not in loop:
                    loop = loop | {p}
                    stack.append(p)
        loop = [i for i in list(loop) if len(blocks[i]["pre"])>0]
        # print(le,sorted(loop))
        loops.append(sorted(loop))
    # 找只有一个基本块的循环
    for n,b in blocks.items():
        if int(n) in b["next"]:
            loops.append([n])
    loops = sorted(loops,key = lambda x:len(x))
    # loops = list(set(loops))
    loops_res = []
    for l in loops:
        if l not in loops_res:
            loops_res.append(l)
    print(loops_res)
    for n,b in blocks.items():
        blocks[n]["dom"] = list(blocks[n]["dom"])
        blocks[n]["pre"] = list(blocks[n]["pre"])
    vm_blk["blocks"] = blocks
    vm_blk["loops"] = loops_res
    new_file = re.sub('(.*)\\.json$', r'\g<1>_loops.json', args.filename[0])
    print("Saving output to:",new_file)
    with open(new_file,"w") as fp:
        json.dump(vm_blk,fp,indent=2)