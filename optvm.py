import re
import json
import argparse
import copy


parser = argparse.ArgumentParser(prog='optvm', prefix_chars='-', description='read the json file and run the vm',
                                 epilog="before using, check the json file")
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
    args = parser.parse_args()
    with open(args.filename[0], "r") as fp:
        vm_runtime = json.load(fp)
    vm_runtime["PC"] = 0
    cnt = 1
    hist = []
    print("="*7+"RUNNING"+"="*7+"\n")
    while (vm_runtime["code"][vm_runtime["PC"]] != "HALT"):
        line = vm_runtime["code"][vm_runtime["PC"]]
        symbols = line.split(" ")
        hist.append((cnt, line, copy.deepcopy(vm_runtime["table"])))
        print("{:3d} {:3d}: ".format(cnt, vm_runtime["PC"]), line)
        vm_runtime["PC"] = vm_runtime["PC"]+1
        if "!:" in symbols:
            print("GOTO", vm_runtime["table"][symbols[1]]["val"])
            vm_runtime["PC"] = vm_runtime["table"][symbols[1]]["val"]
        elif "?" in symbols:
            if cond_f[symbols[2]](vm_runtime["table"][symbols[1]]["val"], vm_runtime["table"][symbols[3]]["val"]):
                print("TRUE {} {} {} ( {} {} {} )".format(symbols[1], symbols[2], symbols[3], vm_runtime["table"][symbols[1]]["val"], symbols[2], vm_runtime["table"][symbols[3]]["val"]))
                print("GOTO", vm_runtime["table"][symbols[5]]["val"])
                vm_runtime["PC"] = vm_runtime["table"][symbols[5]]["val"]
            else:
                print("FALSE {} {} {} ( {} {} {} )".format(symbols[1], symbols[2], symbols[3], vm_runtime["table"][symbols[1]]["val"], symbols[2], vm_runtime["table"][symbols[3]]["val"]))
        else:
            if len(symbols) == 3:
                vm_runtime["table"][symbols[0]
                                    ]["val"] = vm_runtime["table"][symbols[2]]["val"]
            elif symbols[3] == "]":
                print("ASSIGN {}[{}]".format(symbols[0],
                      vm_runtime["table"][symbols[2]]["val"]))
                vm_runtime["table"][symbols[0]]["val"][vm_runtime["table"]
                                                       [symbols[2]]["val"]] = vm_runtime["table"][symbols[5]]["val"]
            elif symbols[3] == "[":
                print("ACCESS {}[{}]".format(symbols[2],
                      vm_runtime["table"][symbols[4]]["val"]))
                vm_runtime["table"][symbols[0]]["val"] = vm_runtime["table"][symbols[2]
                                                                             ]["val"][vm_runtime["table"][symbols[4]]["val"]]
            elif symbols[3] in arith_f:
                vm_runtime["table"][symbols[0]]["val"] = arith_f[symbols[3]](
                    vm_runtime["table"][symbols[2]]["val"], vm_runtime["table"][symbols[4]]["val"])
            else:
                print("! RUNTIME ERROR")
                break
        cnt = cnt+1
        # print(vm_runtime["table"])
    print("{:3d} {:3d}: ".format(
        cnt, vm_runtime["PC"]), vm_runtime["code"][vm_runtime["PC"]])
    print("="*7+"DONE"+"="*7+"\n\n")
    print("="*7+"IN VAR"+"="*7)
    print("".join(["{} : {}\n".format(i[0], i[1]["val"])
          for i in hist[0][2].items() if reg.match(i[0]) == None]))
    print("="*7+"OUT VAR"+"="*7)
    print("".join(["{} : {}\n".format(i[0], i[1]["val"])
          for i in vm_runtime["table"].items() if reg.match(i[0]) == None]))
    new_file = re.sub('(.*)\\.json$', r'\g<1>_vmout.json', args.filename[0])
    print("Saving output to:", new_file)
    with open(new_file, "w") as fp:
        json.dump(hist, fp, indent=2)
