#include <bits/stdc++.h>

using namespace std;

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
    // vector<quad_exp> lines;
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
            // cout << "=========\n";
            // cout << i;
            // cout << labels[i.a1] << ":" << code[labels[i.a1]];
        }
        else if (code[i].op == "JGT" || code[i].op == "JEQ" || code[i].op == "JLT")
        {
            intro.push(labels[code[i].a3]);
            intro.push(i + 1);
            // cout << "=========\n";
            // cout << i;
            // cout << labels[i.a3] << ":" << code[labels[i.a3]];
        };
    };
    cout << "=========\n";
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
        for (int j = i; j < t; j++)
        {
            if (code[j].op == "JGT" || code[j].op == "JEQ" || code[j].op == "JLT" || code[j].op == "JMP" || code[j].op == "HALT")
            {
                cout << code[j];

                break;
            };
            cout << code[j];
        };
        cout << "=========\n";
    }

    return 0;
}