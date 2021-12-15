#include <bits/stdc++.h>

using namespace std;

const regex variable_reg("[A-Za-z]+[A-Za-z0-9]*");
const regex int_reg("[0-9]+");
const regex float_reg("[0-9]+\\.[0-9]+");

struct quad_exp
{
    std::string op, a1, a2, a3;
};

istream &operator>>(istream &in, quad_exp &E)
{
    in >> E.op >> E.a1 >> E.a2 >> E.a3;
    return in;
};
ostream &operator<<(ostream &out, quad_exp &E)
{
    out << E.op << "\t" << E.a1 << "\t" << E.a2 << "\t" << E.a3 << " \n";
    return out;
};

struct var
{
    string var_t = "int"; // int float cint cfloat
    int addr = -1;
    int cint_val = -1;
    float cfloat_val = -1;
};

struct val
{
    string val_t = "err";
    int cint_val = 0;
    float cfloat_val = 0;
};

ostream &operator<<(ostream &out, var &E)
{
    out << E.var_t << "\t" << E.addr << "\t" << E.cint_val << "\t" << E.cfloat_val << " \n";
    return out;
};

vector<quad_exp> code;
map<string, int> labels;
map<string, var> var_table;
vector<int> memory_int;
vector<float> memory_float;

bool rt_err = false;

void show_var_table()
{
    cout << "\n=====Var_Table=====\n";
    cout << "NAME"
         << "\t"
         << "TYPE"
         << "\t"
         << "ADDR"
         << "\t"
         << "CINT"
         << "\t"
         << "CFLT"
         << "\n";
    for (auto iter : var_table)
    {
        cout << iter.first << "\t" << iter.second;
    };
    cout << "\n=====Var_Table=====\n\n\n";
};

void show_mem_var()
{
    cout << "=====MEM_Var=====\n";
    cout << "NAME"
         << "\t"
         << "TYPE"
         << "\t"
         << "ADDR"
         << "\t"
         << "MVAL"
         << "\n";
    for (auto iter : var_table)
    {
        if (iter.second.var_t == "int")
        {
            cout << iter.first << "\t" << iter.second.var_t << "\t" << iter.second.addr << "\t" << memory_int[iter.second.addr] << " \n";
        }
        else if (iter.second.var_t == "float")
        {
            cout << iter.first << "\t" << iter.second.var_t << "\t" << iter.second.addr << "\t" << memory_float[iter.second.addr] << " \n";
        }
    };
    cout << "\n=====MEM_Var=====\n\n\n";
};

val get_val(string s)
{
    var v = var_table[s];
    val ret;
    if (v.var_t == "int")
    {
        ret.val_t = "i";
        ret.cint_val = memory_int[v.addr];
    }
    else if (v.var_t == "float")
    {
        ret.val_t = "f";
        ret.cfloat_val = memory_float[v.addr];
    }
    else if (v.var_t == "cint")
    {
        ret.val_t = "i";
        ret.cint_val = v.cint_val;
    }
    else if (v.var_t == "cfloat")
    {
        ret.val_t = "f";
        ret.cfloat_val = v.cfloat_val;
    }
    return ret;
}

val add_val(string s1, string s2)
{

    val a1, a2, ret;
    a1 = get_val(s1);
    a2 = get_val(s2);
    if (a1.val_t == "err" || a2.val_t == "err")
    {
        cout << "RUNTIME ERROR!\n";
        rt_err = true;
        return ret;
    };
    if (a1.val_t == a2.val_t)
    {
        ret.val_t = a1.val_t;
        ret.cfloat_val = a1.cfloat_val + a2.cfloat_val;
        ret.cint_val = a1.cint_val + a2.cint_val;
    }
    else
    {
        ret.val_t = "float";
        ret.cfloat_val = a1.cfloat_val + a2.cfloat_val + (float)a1.cint_val + (float)a2.cint_val;
    };
    return ret;
};

val sub_val(string s1, string s2)
{

    val a1, a2, ret;
    a1 = get_val(s1);
    a2 = get_val(s2);
    if (a1.val_t == "err" || a2.val_t == "err")
    {
        cout << "RUNTIME ERROR!\n";
        rt_err = true;
        return ret;
    };
    if (a1.val_t == a2.val_t)
    {
        ret.val_t = a1.val_t;
        ret.cfloat_val = a1.cfloat_val - a2.cfloat_val;
        ret.cint_val = a1.cint_val - a2.cint_val;
    }
    else
    {
        ret.val_t = "float";
        ret.cfloat_val = a1.cfloat_val - a2.cfloat_val + (float)a1.cint_val - (float)a2.cint_val;
    };
    return ret;
};

val mul_val(string s1, string s2)
{

    val a1, a2, ret;
    a1 = get_val(s1);
    a2 = get_val(s2);
    if (a1.val_t == "err" || a2.val_t == "err")
    {
        cout << "RUNTIME ERROR!\n";
        rt_err = true;
        return ret;
    };
    if (a1.val_t == a2.val_t)
    {
        ret.val_t = a1.val_t;
        ret.cfloat_val = a1.cfloat_val * a2.cfloat_val;
        ret.cint_val = a1.cint_val * a2.cint_val;
    }
    else
    {
        ret.val_t = "float";
        if (a1.val_t == "float")
        {
            ret.cfloat_val = a1.cfloat_val * (float)a2.cint_val;
        }
        else
        {
            ret.cfloat_val = a2.cfloat_val * (float)a1.cint_val;
        }
    };
    return ret;
};

int main()
{
    quad_exp tmp;
    while (cin >> tmp)
    {
        code.push_back(tmp);
        if (tmp.op == "LABEL")
            labels.insert({tmp.a1, code.size() - 1});
    };

    // 注册各个变量
    int addr_cnt = 100;
    for (auto &l : code)
    {
        if (l.op != "HALT" && l.op != "LABEL" && l.op != "JMP" && l.op != "JEQ" && l.op != "JLE" && l.op != "JGT")
        {
            if (regex_match(l.a1, variable_reg))
            {
                var tmp;
                tmp.addr = addr_cnt;
                addr_cnt += 100;
                var_table.insert({l.a1, tmp});
            }
            else if (regex_match(l.a1, int_reg))
            {
                var tmp;
                tmp.addr = -1;
                tmp.var_t = "cint";
                tmp.cint_val = stoi(l.a1);
                var_table.insert({l.a1, tmp});
            }
            else if (regex_match(l.a1, float_reg))
            {
                var tmp;
                tmp.addr = -1;
                tmp.var_t = "cfloat";
                tmp.cfloat_val = stof(l.a1);
                var_table.insert({l.a1, tmp});
            }
            else if (l.op != "HALT")
            {
                cout << "SYTAX ERROR!\n"
                     << l;
                return 1;
            };
            if (regex_match(l.a2, variable_reg))
            {
                var tmp;
                tmp.addr = addr_cnt;
                addr_cnt += 100;
                var_table.insert({l.a2, tmp});
            }
            else if (regex_match(l.a2, int_reg))
            {
                var tmp;
                tmp.addr = -1;
                tmp.var_t = "cint";
                tmp.cint_val = stoi(l.a2);
                var_table.insert({l.a2, tmp});
            }
            else if (regex_match(l.a2, float_reg))
            {
                var tmp;
                tmp.addr = -1;
                tmp.var_t = "cfloat";
                tmp.cfloat_val = stof(l.a2);
                var_table.insert({l.a2, tmp});
            }
            else if (l.a2 != "-")
            {
                cout << "SYTAX ERROR!\n"
                     << l;
                return 1;
            };
            if (regex_match(l.a3, variable_reg))
            {
                var tmp;
                tmp.addr = addr_cnt;
                addr_cnt += 100;
                var_table.insert({l.a3, tmp});
            }
            else if (regex_match(l.a3, int_reg))
            {
                var tmp;
                tmp.addr = -1;
                tmp.var_t = "cint";
                tmp.cint_val = stoi(l.a3);
                var_table.insert({l.a3, tmp});
            }
            else if (regex_match(l.a3, float_reg))
            {
                var tmp;
                tmp.addr = -1;
                tmp.var_t = "cfloat";
                tmp.cfloat_val = stof(l.a3);
                var_table.insert({l.a3, tmp});
            }
            else if (l.a3 != "-")
            {
                cout << "SYTAX ERROR!\n"
                     << l;
                return 1;
            };
        }
        else if (l.op == "JEQ" || l.op == "JLE" || l.op == "JGT")
        {
            if (regex_match(l.a1, variable_reg))
            {
                var tmp;
                tmp.addr = addr_cnt;
                addr_cnt += 100;
                var_table.insert({l.a1, tmp});
            }
            else if (regex_match(l.a1, int_reg))
            {
                var tmp;
                tmp.addr = -1;
                tmp.var_t = "cint";
                tmp.cint_val = stoi(l.a1);
                var_table.insert({l.a1, tmp});
            }
            else if (regex_match(l.a1, float_reg))
            {
                var tmp;
                tmp.addr = -1;
                tmp.var_t = "cfloat";
                tmp.cfloat_val = stof(l.a1);
                var_table.insert({l.a1, tmp});
            }
            else if (l.op != "HALT")
            {
                cout << "SYTAX ERROR!\n"
                     << l;
                return 1;
            };
            if (regex_match(l.a2, variable_reg))
            {
                var tmp;
                tmp.addr = addr_cnt;
                addr_cnt += 100;
                var_table.insert({l.a2, tmp});
            }
            else if (regex_match(l.a2, int_reg))
            {
                var tmp;
                tmp.addr = -1;
                tmp.var_t = "cint";
                tmp.cint_val = stoi(l.a2);
                var_table.insert({l.a2, tmp});
            }
            else if (regex_match(l.a2, float_reg))
            {
                var tmp;
                tmp.addr = -1;
                tmp.var_t = "cfloat";
                tmp.cfloat_val = stof(l.a2);
                var_table.insert({l.a2, tmp});
            }
            else if (l.a2 != "-")
            {
                cout << "SYTAX ERROR!\n"
                     << l;
                return 1;
            };
        }
    };

    // 分配内存空间
    memory_int.assign(addr_cnt, 0);
    memory_float.assign(addr_cnt, 0.0);
    show_var_table();
    // 开始执行代码
    int cyc = 0;
    int pc = 0;
    while (code[pc].op != "HALT")
    {
        cout << ++cyc << "\t" << code[pc];
        if (code[pc].op == "JMP")
        {
            pc = labels[code[pc].a1];
        }
        else if (code[pc].op == "JEQ")
        {
        }
        else if (code[pc].op == "JGT")
        {
        }
        else if (code[pc].op == "JLT")
        {
        }

        show_mem_var();
        pc++;
    };
    cout << ++cyc << "\t" << code[pc];
    return 0;
}