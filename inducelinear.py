# %%
import re
import json
import argparse
import copy
import random


# %%
parser = argparse.ArgumentParser(prog='inducelinearvariable', prefix_chars='-', description='induce linear variables',
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


# %%
# 文件读写
program = {}
args = parser.parse_args()
filename = args.filename[0]
with open(filename, "r") as fp:
    program = json.load(fp)


# %% [markdown]
# testjson='''
# {
#   "summary": {
#     "total_blocks": 4
#   },
#   "blocks": {
#     "0": {
#       "line_num": [
#         0,
#         2
#       ],
#       "next": [
#         "1",
#         null
#       ],
#       "code": [
#         "S = 0",
#         "I = 1",
#         "N = 100"
#       ],
#       "defd": [
#         "S",
#         "I",
#         "N"
#       ],
#       "used": [],
#       "in": [],
#       "out": [
#         "N",
#         "S",
#         "I"
#       ],
#       "pre": [],
#       "dom": [
#         "0"
#       ]
#     },
#     "1": {
#       "line_num": [
#         3,
#         3
#       ],
#       "next": [
#         "2",
#         "3"
#       ],
#       "code": [
#         "? I > N : 9"
#       ],
#       "defd": [],
#       "used": [
#         "N",
#         "I"
#       ],
#       "in": [
#         "N",
#         "S",
#         "I"
#       ],
#       "out": [
#         "S",
#         "I",
#         "N"
#       ],
#       "pre": [
#         "2",
#         "0"
#       ],
#       "dom": [
#         "0",
#         "1"
#       ]
#     },
#     "2": {
#       "line_num": [
#         4,
#         8
#       ],
#       "next": [
#         "1",
#         null
#       ],
#       "remainedvar":[
#           "2",
#           "1"
#       ],
#       "code": [
#         "J = I * 2",
#         "J = J - 1",
#         "S = S + J",
#         "I = I + 2",
#         "!: 3"
#       ],
#       "defd": [
#         "J"
#       ],
#       "used": [
#         "S",
#         "I"
#       ],
#       "in": [
#         "S",
#         "N",
#         "I"
#       ],
#       "out": [
#         "N",
#         "S",
#         "I"
#       ],
#       "pre": [
#         "1"
#       ],
#       "dom": [
#         "2",
#         "1",
#         "0"
#       ]
#     },
#     "3": {
#       "line_num": [
#         9,
#         9
#       ],
#       "next": [
#         null,
#         null
#       ],
#       "code": [
#         "HALT"
#       ],
#       "defd": [],
#       "used": [],
#       "in": [],
#       "out": [],
#       "pre": [
#         "1"
#       ],
#       "dom": [
#         "0",
#         "3",
#         "1"
#       ]
#     }
#   },
#   "loops": [
#     {
#       "loop_blks": [
#         "1",
#         "2"
#       ],
#       "back_edge": [
#         "2",
#         "1"
#       ]
#     }
#   ]
# }
# '''

# %%

# 加基本块事宜
def appendblk(loopkey):
    # 循环
    loop = program['loops'][loopkey]
    # 回基本块
    backblk = program['blocks'][loop['back_edge'][1]]

    # 新基本块
    maxblock = program['summary']['total_blocks']

    program['blocks'][str(maxblock)] = {
        "line_num": [0, 0],
        "next": [loop['back_edge'][1], None],
        "code": [],
        "defd": [],
        "remainedvar": [],
        "used": [],
        "in": [],
        "out": [],
        "pre": list(set(backblk['pre'])-set(loop['back_edge'][0])),
        "dom": []
    }
    program['summary']['total_blocks'] = maxblock
    newblk = program['blocks'][str(maxblock)]

    # 改变所有权
    for blkname in newblk['pre']:
        blk = program['blocks'][blkname]
        if(blk['next'][0] == loop['back_edge'][1]):
            blk['next'][0] = str(maxblock)
        if(blk['next'][1] == loop['back_edge'][1]):
            blk['next'][1] = str(maxblock)

    backblk['pre'] = [str(maxblock), loop['back_edge'][0]]

    # loop["loop_blks"].append(str(maxblock))
    maxblock += 1

    return newblk


def appendcode(ope, blk):
    blk['code'].append(ope)
    # blk['defd'].append()
    # blk["used"].append()
    # blk['in'].append()
    # blk['out'].append()
    pass


def updatecode(ope, start, end, blk):
    upcodes = blk['code'][:start]
    downcodes = blk['code'][end+1:]
    blk['code'] = upcodes+[ope]+downcodes


# %%
# 处理头
for loop in program['loops']:
    head = []
    for blk_name in loop['loop_blks']:
        blk = program['blocks'][blk_name]
        # 回边指向或唯一前驱
        if(blk_name == loop['back_edge'][1] or len(blk['pre']) <= 1):
            head.append(blk_name)
        else:
            # 头必须连续
            break
    loop['head'] = head

print(program['loops'])

# %%
# 解析代码


def simpleassign(code):
    if(re.match('^.*=.*$', code)):
        if(re.match(r'^[A-Za-z_][A-Za-z0-9_]*\[.*\]\s*=\s*.*$', code)):
            return None
        thisvar = re.search(
            r'^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*.*', code).group(1)
        # print(thisvar)
        return thisvar
    return None


def simpleselfplusminus(code):
    if(re.match('^.*=.*$', code)):
        if(re.match(r'^[A-Za-z_][A-Za-z0-9_]*\[.*\]\s*=\s*.*$', code)):
            return None
        search = re.search(
            r'^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*([A-Za-z_][A-Za-z0-9_]*)\s*([\+\-])\s*([0-9]*)', code)
        if(search):
            res = search.group(1)
            left = search.group(2)
            opt = search.group(3)
            right = search.group(4)
            if(res and left and opt and right and res == left):
                # print("out",res,left,opt,right)
                return res, left, opt, right
    return None


def simpleselfmultiply(code):
    if(re.match('^.*=.*$', code)):
        if(re.match(r'^[A-Za-z_][A-Za-z0-9_]*\[.*\]\s*=\s*.*$', code)):
            return None
        search = re.search(
            r'^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*([A-Za-z_][A-Za-z0-9_]*)\s*(\*)\s*([0-9]*)', code)
        if(search):
            res = search.group(1)
            left = search.group(2)
            opt = search.group(3)
            right = search.group(4)
            if(res and left and opt and right and res == left):
                # print("out",res,left,opt,right)
                return res, left, opt, right
        return None


def simplemultiply(code):
    if(re.match('^.*=.*$', code)):
        if(re.match(r'^[A-Za-z_][A-Za-z0-9_]*\[.*\]\s*=\s*.*$', code)):
            return None
        search = re.search(
            r'^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*([A-Za-z_][A-Za-z0-9_]*)\s*(\*)\s*([0-9]*)', code)
        if(search):
            res = search.group(1)
            left = search.group(2)
            opt = search.group(3)
            right = search.group(4)
            if(res and left and opt and right):
                # print("out",res,left,opt,right)
                return res, left, opt, right
        return None


def simpleplusminus(code):
    if(re.match('^.*=.*$', code)):
        if(re.match(r'^[A-Za-z_][A-Za-z0-9_]*\[.*\]\s*=\s*.*$', code)):
            return None
        search = re.search(
            r'^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*([A-Za-z_][A-Za-z0-9_]*)\s*([\+\-])\s*([0-9]*)', code)
        if(search):
            res = search.group(1)
            left = search.group(2)
            opt = search.group(3)
            right = search.group(4)
            if(res and left and opt and right):
                # print("out",res,left,opt,right)
                return res, left, opt, right
        return None


def assigned(var, code):
    return var == simpleassign(code)


print(simpleassign('T = T + 1'))
print(simpleselfplusminus('T = T + 2'))
print(simpleselfmultiply('T = T * 2'))


# %%
# 求符合的变量和变量的段

def getappear(codes):
    options = []
    for code in codes:
        var = simpleassign(code)
        if(var):
            ope = simpleselfplusminus(code)
            if(ope):
                # 加减法自增
                res, left, opt, right = ope
                options.append((2, res, left, opt, right))
                continue
            ope = simpleselfmultiply(code)
            if(ope):
                # 乘法自增
                res, left, opt, right = ope
                options.append((3, res, left, opt, right))
                continue
            ope = simpleplusminus(code)
            if(ope):
                # 非自增加法
                res, left, opt, right = ope
                options.append((4, res, left, opt, right))
                continue
            ope = simplemultiply(code)
            if(ope):
                # 非自增乘法
                res, left, opt, right = ope
                options.append((5, res, left, opt, right))
                continue
            else:
                # 其他简单赋值
                options.append((1, var, None, None, None))
                continue
        else:
            # 不是简单赋值
            options.append((None, None, None, None, None))
            continue
    return options


def basicsegment(var, options):
    i = 0
    cur = 0
    start = -1
    end = -1
    res = []
    while(i < len(options)):
        option = options[i]
        if(option[0] is None):
            i += 1
            continue
        thisvar = option[1]
        if(var == thisvar):
            if(option[0] != 2):
                return None
            if(option[0] == 2):
                end = i
                if(start == -1):
                    start = i
                i += 1
                continue
        else:
            if(start != -1 and end != -1):
                res.append((start, end))
                start = -1
                end = -1
                cur += 1
            i += 1
            continue
    if(start != -1 and end != -1):
        res.append((start, end))
        start = -1
        end = -1
        cur += 1
    if(cur != 1):
        return None
    return res[0]


def inducesegment(var, options):
    # print("var", var)
    i = 0
    cur = 0
    start = -1
    end = -1
    res = []
    while(i < len(options)):
        option = options[i]
        # print("option", option)
        # print("res", res)
        # print("start", start, "end", end)
        if(option[0] is None):
            i += 1
            continue
        thisvar = option[1]
        # print("thisvar", thisvar)
        if(var == thisvar):
            if(option[0] == 1):
                return None
            if(option[0] == 5):
                end = i
                if(start == -1):
                    start = i
                i += 1
                continue
            if(option[0] == 2 or option[0] == 3 or option[0] == 4):
                if(start != -1):
                    end = i
                i += 1
                continue
        else:
            if(start != -1 and end != -1):
                res.append((start, end))
                start = -1
                end = -1
                cur += 1
            i += 1
            continue
    if(start != -1 and end != -1):
        res.append((start, end))
        start = -1
        end = -1
        cur += 1
    if(cur != 1):
        return None
    return res[0]


def getbasic(options):
    basic = []
    for option in options:
        if(option[0] is None):
            continue
        var = option[1]
        seg = basicsegment(var, options)
        if(seg is None):
            continue
        (_, res, left, opt, right) = options[seg[1]]
        varbasic = (var, opt, right, seg[1], seg[1])
        if(varbasic not in basic):
            basic.append(varbasic)
    return basic


def getinduce(options):
    induce = []
    for option in options:
        if(option[0] is None):
            continue
        var = option[1]
        seg = inducesegment(var, options)
        if(seg is None):
            continue
        start, end = seg

        varinduce = []
        for j in range(start, end+1):
            (_, res, left, opt, right) = options[j]
            varinduce.append((res, left, opt, right, start, end))
        if(varinduce not in induce):
            induce.append(varinduce)
    return induce


# %%
def dealwithbasic(blk, newblk):
    basic = blk['basics']


def dealwithinduce(blk, newblk):
    induces = blk['induces']
    basic = blk['basics']

    func = {
        '+': lambda x, y: x+y,
        '-': lambda x, y: x-y,
    }

    inverseopt = {
        '+': '-',
        '-': '+'
    }

    for induce in induces:
        inducevar = ""
        basicvar = ""
        k, b, c, back = 1, 0, 0, False
        operation, inverseoperation, initoperation = '+', '-', '+'
        first = -1
        last = -1
        basicfirst = -1
        basiclast = -1
        for (var, left, opt, right, start, end) in induce:
            inducevar = var
            first = start
            last = end
            if(left == var):
                b = int(right)
                initoperation = opt
                continue
            for bsc, op, rt, st, ed in basic:
                if(left == bsc):
                    basicfirst = st
                    basiclast = ed
                    basicvar = bsc
                    if(start > ed):
                        back = True
                    c = int(rt)
                    operation = op
                    inverseoperation = inverseopt[op]
                    if(opt == '*'):
                        k = int(right)
                    if(opt == '+' or opt == '-'):
                        k = 1
                        initoperation = opt
                        b = int(right)

        print(k, b, c, operation)
        if(back):
            init1 = inducevar+" = "+basicvar+" * "+str(k)
            init2 = inducevar+" = "+inducevar+" "+initoperation+" "+str(b)

            tempvar = 'T_'+str(random.randint(100, 200))
            init3 = tempvar+" = "+str(k)+" * "+str(c)

            step = inducevar+" = "+inducevar+" "+operation+" "+tempvar

            appendcode(init1, newblk)
            appendcode(init2, newblk)
            appendcode(init3, newblk)

            updatecode(step, first, last, blk)

        else:
            tempinit = 'T_'+str(random.randint(100, 200))
            init0 = tempinit+" = "+basicvar+" "+inverseoperation+" "+str(c)

            init1 = inducevar+" = "+tempinit+" * "+str(k)
            init2 = inducevar+" = "+inducevar+" "+initoperation+" "+str(b)

            tempvar = 'T_'+str(random.randint(100, 200))
            init3 = tempvar+" = "+str(k)+" * "+str(c)

            step = inducevar+" = "+inducevar+" "+operation+" "+tempvar

            appendcode(init0, newblk)
            appendcode(init1, newblk)
            appendcode(init2, newblk)
            appendcode(init3, newblk)

            updatecode(step, first, last, blk)


# %%
# 求解每一个循环的每一个基本块
for loopidx in range(len(program['loops'])):

    # 新建块
    loop = program['loops'][loopidx]
    # print(loopidx)
    newblk = appendblk(loopidx)

    # 对于每一个循环里的基本块
    for blk_name in loop['head']:
        blk = program['blocks'][blk_name]

        blk['options'] = getappear(blk['code'])
        blk['basics'] = getbasic(blk['options'])
        blk['induces'] = getinduce(blk['options'])
        # print(blk['options'])
        # print(blk['basics'])
        # print(blk['induces'])

        dealwithbasic(blk, newblk)
        dealwithinduce(blk, newblk)

program['blocks']
# 跑blocktotri然后再跑tritojson再跑split再跑findloop


# %%
new_file = re.sub('(.*)\\.json$', r'\g<1>_induce.json', args.filename[0])
print("Saving output to:", new_file)
with open(new_file, "w") as fp:
    json.dump(program, fp, indent=2)
