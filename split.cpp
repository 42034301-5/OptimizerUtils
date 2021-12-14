#include <bits/stdc++.h>

using namespace std;

const regex variable_reg("[A-Za-z]+[A-Za-z0-9]*");

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

vector<quad_exp> code;
priority_queue<int, vector<int>, greater<int>> intro;
map<string, int> labels;

struct quad_block
{
    int in_line, ext_line;
    vector<quad_exp> lines;
    int next_blk, jop_blk;
    set<string> inblkv;
    set<string> defdv;
    set<string> usedv;
    set<string> in_v;
    set<string> out_v;
};

vector<quad_block> blocks;

bool set_changed(const set<string> &s1, const set<string> &s2)
{
    if (s1.size() != s2.size())
    {
        return true;
    }
    set<string>::iterator it;
    set<string>::iterator it1;
    for (it = s1.begin(), it1 = s2.begin(); it != s1.end(); it++, it1++)
    {
        if (*it1 != *it)
        {
            return true;
        }
    };
    return false;
};
int main()
{
    std::string op, a1, a2, a3;
    quad_exp tmp;
    while (cin >> tmp)
    {
        code.push_back(tmp);
        if (tmp.op == "LABEL")
            labels.insert({tmp.a1, code.size() - 1});
    };
    intro.push(0);
    for (int i = 0; i < code.size(); i++)
    {
        if (code[i].op == "JMP")
        {
            intro.push(labels[code[i].a1]);
        }
        else if (code[i].op == "JGT" || code[i].op == "JEQ" || code[i].op == "JLT")
        {
            intro.push(labels[code[i].a3]);
            intro.push(i + 1);
        };
    };
    while (!intro.empty())
    {
        int i = intro.top();
        intro.pop();
        int t;
        if (!intro.empty())
        {
            t = intro.top();
        }
        else
        {
            t = code.size();
        };
        quad_block tmp;
        tmp.in_line = i;
        int j = i;
        for (; j < t; j++)
        {
            if (code[j].op == "JGT" || code[j].op == "JEQ" || code[j].op == "JLT" || code[j].op == "JMP" || code[j].op == "HALT")
            {
                // cout << code[j];
                tmp.lines.push_back(code[j]);
                break;
            };
            // cout << code[j];
            tmp.lines.push_back(code[j]);
        };
        tmp.ext_line = j;
        if (tmp.lines.size() > 0)
            blocks.push_back(tmp);
    };

    // 后处理基本块
    int cnt = 0;
    for (auto &b : blocks)
    {
        cnt++;
        // 处理跳转目标
        if ((b.lines.end() - 1)->op == "HALT")
        {
            b.next_blk = 0;
            b.jop_blk = 0;
            // cout << "; NXT 0 0\n";
        }
        else
        {
            // cout << "; NXT ";
            string tempop = (b.lines.end() - 1)->op;
            if (tempop == "JGT" || tempop == "JLT" || tempop == "JEQ")
            {
                int j = 0;
                for (; j < blocks.size(); j++)
                {
                    if (blocks[j].lines.begin()->a1 == (b.lines.end() - 1)->a3)
                        break;
                };
                // cout << cnt + 1 << " " << j + 1;
                b.next_blk = cnt + 1;
                b.jop_blk = j + 1;
            }
            else if (tempop == "JMP")
            {
                int j = 0;
                for (; j < blocks.size(); j++)
                {
                    if (blocks[j].lines.begin()->a1 == (b.lines.end() - 1)->a1)
                        break;
                };
                // cout << " " << j + 1;
                b.next_blk = j + 1;
                b.jop_blk = 0;
            }
            else
            {
                // cout << cnt + 1;
                b.next_blk = cnt + 1;
                b.jop_blk = 0;
            };
            // cout << b.next_blk << " " << b.jop_blk << "\n";
        };

        // 处理基本块中涉及的变量
        set<string> vars;
        for (auto &l : b.lines)
        {
            string tempop = l.op;
            if (tempop != "JMP" && tempop != "JEQ" && tempop != "JGT" && tempop != "JLT" && tempop != "LABEL")
            {
                if (regex_match(l.a1, variable_reg))
                    vars.insert(l.a1);
                if (regex_match(l.a2, variable_reg))
                    vars.insert(l.a2);
                if (regex_match(l.a3, variable_reg))
                    vars.insert(l.a3);
            }
            else if (tempop == "JGT" || tempop == "JLT" || tempop == "JEQ")
            {
                if (regex_match(l.a1, variable_reg))
                    vars.insert(l.a1);
                if (regex_match(l.a2, variable_reg))
                    vars.insert(l.a2);
            };
        };
        b.inblkv = vars;
        // cout << "; VAR";
        // for (auto v = b.inblkv.begin(); v != b.inblkv.end(); v++)
        // {
        //     cout << " " << *v;
        // };
        // cout << "\n";

        // 处理基本块中首次出现是定值的变量
        set<string> defd;
        for (int i = 0; i < b.lines.size(); i++)
        {
            quad_exp l = b.lines[i];
            string tempop = l.op;
            if (tempop != "JMP" && tempop != "JEQ" && tempop != "JGT" && tempop != "JLT" && tempop != "LABEL" && tempop != "WRITE")
            {
                if (regex_match(l.a1, variable_reg) && l.a1 != l.a2 && l.a1 != l.a3)
                {
                    bool flag = true;
                    for (int j = 0; j < i; j++)
                        if (b.lines[j].a2 == l.a1 || b.lines[j].a3 == l.a1)
                            flag = false;
                    if (flag)
                        defd.insert(l.a1);
                };
            };
        };
        b.defdv = defd;
        // cout << "; DEF";
        // for (auto v = b.defdv.begin(); v != b.defdv.end(); v++)
        // {
        //     cout << " " << *v;
        // };
        // cout << "\n";

        // 处理基本块中首次出现是引用的变量
        set<string> used;
        for (int i = 0; i < b.lines.size(); i++)
        {
            quad_exp l = b.lines[i];
            string tempop = l.op;
            if (tempop != "JMP" && tempop != "READ" && tempop != "LABEL" && tempop != "JEQ" && tempop != "JGT" && tempop != "JLT")
            {
                if (regex_match(l.a2, variable_reg))
                {
                    bool flag = true;
                    for (int j = 0; j < i; j++)
                        if (b.lines[j].a1 == l.a2)
                            flag = false;
                    if (flag)
                        used.insert(l.a2);
                };
                if (regex_match(l.a3, variable_reg))
                {
                    bool flag = true;
                    for (int j = 0; j < i; j++)
                        if (b.lines[j].a1 == l.a3)
                            flag = false;
                    if (flag)
                        used.insert(l.a3);
                };
            }
            else if (tempop == "JGT" || tempop == "JLT" || tempop == "JEQ")
            {
                if (regex_match(l.a1, variable_reg))
                {
                    bool flag = true;
                    for (int j = 0; j < i; j++)
                        if (b.lines[j].a1 == l.a1)
                            flag = false;
                    if (flag)
                        used.insert(l.a1);
                };
                if (regex_match(l.a2, variable_reg))
                {
                    bool flag = true;
                    for (int j = 0; j < i; j++)
                        if (b.lines[j].a1 == l.a2)
                            flag = false;
                    if (flag)
                        used.insert(l.a2);
                };
            };
        };
        b.usedv = used;
        // cout << "; USE";
        // for (auto v = b.usedv.begin(); v != b.usedv.end(); v++)
        // {
        //     cout << " " << *v;
        // };
        // cout << "\n";
    };

    // 生成各基本块的活跃变量
    bool in_changed;
    do
    {
        in_changed = false;
        for (auto &b : blocks)
        {
            if (b.next_blk != 0)
            {
                set<string> tmp;
                set_union(b.out_v.begin(), b.out_v.end(), blocks[b.next_blk - 1].in_v.begin(), blocks[b.next_blk - 1].in_v.end(), inserter(tmp, tmp.begin()));
                b.out_v = tmp;
            };
            if (b.jop_blk != 0)
            {
                set<string> tmp;
                set_union(b.out_v.begin(), b.out_v.end(), blocks[b.jop_blk - 1].in_v.begin(), blocks[b.jop_blk - 1].in_v.end(), inserter(tmp, tmp.begin()));
                b.out_v = tmp;
            };
            set<string> tmp, dif;
            set_difference(b.out_v.begin(), b.out_v.end(), b.defdv.begin(), b.defdv.end(), inserter(dif, dif.begin()));
            set_union(dif.begin(), dif.end(), b.usedv.begin(), b.usedv.end(), inserter(tmp, tmp.begin()));
            in_changed = in_changed || set_changed(tmp, b.in_v);
            b.in_v = tmp;
        };
    } while (in_changed);

    // 大功告成，开始输出
    cout << "; SPLITTED RESULTS\n";
    for (int i = 0; i < blocks.size(); i++)
    {
        cout << "\n; #BLK " << i + 1 << "\n";
        quad_block b = blocks[i];
        // 输出各行
        for (auto &l : b.lines)
        {
            cout << l;
        };
        // 输出下个基本块的标号
        cout << "; NXT ";
        cout << b.next_blk << " " << b.jop_blk;
        cout << "\n";
        // 输出基本块内的变量
        cout << "; VAR";
        for (auto v = b.inblkv.begin(); v != b.inblkv.end(); v++)
        {
            cout << " " << *v;
        };
        cout << "\n";
        // 输出基本块内首次使用为定值的变量
        cout << "; DEF";
        for (auto v = b.defdv.begin(); v != b.defdv.end(); v++)
        {
            cout << " " << *v;
        };
        cout << "\n";
        // 输出基本块内首次使用为引用的变量
        cout << "; USE";
        for (auto v = b.usedv.begin(); v != b.usedv.end(); v++)
        {
            cout << " " << *v;
        };
        cout << "\n";
        // 输出出基本块活跃的变量
        cout << "; OUT";
        for (auto v = b.out_v.begin(); v != b.out_v.end(); v++)
        {
            cout << " " << *v;
        };
        cout << "\n";
        // 输出入口处活跃的变量
        cout << "; IN";
        for (auto v = b.in_v.begin(); v != b.in_v.end(); v++)
        {
            cout << " " << *v;
        };
        cout << "\n";
    };

    return 0;
}