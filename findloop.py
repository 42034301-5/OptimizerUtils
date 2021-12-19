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
    vm_src = {}
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
    stack = ['0']
    visited = {str(i):False for i in range(vm_blk["summary"]["total_blocks"])}
    dfn = {str(i):vm_blk["summary"]["total_blocks"]*7 for i in range(vm_blk["summary"]["total_blocks"])}
    low = {str(i):vm_blk["summary"]["total_blocks"]*7 for i in range(vm_blk["summary"]["total_blocks"])}
    parent = {str(i):None for i in range(vm_blk["summary"]["total_blocks"])}
    cnt = 0
    back_edge = []
    while len(stack)>0:
        tmp = stack[-1]
        visited[tmp] = True
        stack.pop()
        # print(tmp)
        for i in blocks[tmp]["next"]:
            if (i!=None):
                if not visited[str(i)]:
                    stack.append(str(i))
                    dfn[str(i)] = cnt
                    cnt+=1
                    parent[str(i)] = tmp
                else:
                    # print(tmp,dfn[tmp],"->",str(i),dfn[str(i)])
                    back_edge.append((tmp,str(i)))
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
        loops.append(loop)
    loops = sorted(loops,key = lambda x:len(x))
    print(loops)

    new_file = re.sub('(.*)\\.json$', r'\g<1>_loops.json', args.filename[0])
    print("Saving output to:",new_file)
    with open(new_file,"w") as fp:
        json.dump(loops,fp,indent=2)