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
};

vector<quad_block> blocks;

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
        blocks.push_back(tmp);
    };

    // 后处理基本块
    int cnt = 0;
    for (auto &b : blocks)
    {
        // 输出基本块内的所有四元式
        cout << "\n\n#BLK " << ++cnt << "\n";
        for (auto &l : b.lines)
        {
            cout << l;
        };

        // 处理跳转目标
        if ((b.lines.end() - 1)->op == "HALT")
        {
            cout << ";END\n";
        }
        else
        {
            cout << ";NXT ";
            string tempop = (b.lines.end() - 1)->op;
            if (tempop == "JGT" || tempop == "JLT" || tempop == "JEQ")
            {
                int j = 0;
                for (; j < blocks.size(); j++)
                {
                    if (blocks[j].lines.begin()->a1 == (b.lines.end() - 1)->a3)
                        break;
                };
                cout << cnt + 1 << " " << j + 1;
            }
            else if (tempop == "JMP")
            {
                int j = 0;
                for (; j < blocks.size(); j++)
                {
                    if (blocks[j].lines.begin()->a1 == (b.lines.end() - 1)->a1)
                        break;
                };
                cout << " " << j + 1;
            }
            else
            {
                cout << cnt + 1;
            };
            cout << "\n";
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
        cout << ";VAR";
        for (auto v = vars.begin(); v != vars.end(); v++)
        {
            cout << " " << *v;
        };
        cout << "\n";

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
        cout << ";DEF";
        for (auto v = defd.begin(); v != defd.end(); v++)
        {
            cout << " " << *v;
        };
        cout << "\n";

        // 处理基本块中首次出现是引用的变量
        set<string> used;
        for (int i = 0; i < b.lines.size(); i++)
        {
            quad_exp l = b.lines[i];
            string tempop = l.op;
            if (tempop != "JMP" && tempop != "READ" && tempop != "LABEL" && tempop != "JEQ" && tempop != "JGT" && tempop != "JLT")
            {
                if (regex_match(l.a2, variable_reg) && l.a1 != l.a2)
                {
                    bool flag = true;
                    for (int j = 0; j < i; j++)
                        if (b.lines[j].a1 == l.a2)
                            flag = false;
                    if (flag)
                        used.insert(l.a2);
                };
                if (regex_match(l.a3, variable_reg) && l.a1 != l.a3)
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
        cout << ";USE";
        for (auto v = used.begin(); v != used.end(); v++)
        {
            cout << " " << *v;
        };
        cout << "\n";
    };

    return 0;
}