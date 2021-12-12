#include <bits/stdc++.h>

using namespace std;

const regex tri00("^READ\t([A-Za-z]+[A-Za-z0-9]*)\t-\t-\\s*");
const regex tri01("^WRITE\t([A-Za-z]+[A-Za-z0-9]*)\t-\t-\\s*");
const regex tri02("^SET\t([A-Za-z]+[A-Za-z0-9]*)\t([A-Za-z0-9.]+)\t-\\s*");
const regex tri03("^ADD\t([A-Za-z]+[A-Za-z0-9]*)\t([A-Za-z0-9.]+)\t([A-Za-z0-9.]+)\\s*");
const regex tri04("^SUB\t([A-Za-z]+[A-Za-z0-9]*)\t([A-Za-z0-9.]+)\t([A-Za-z0-9.]+)\\s*");
const regex tri05("^MUL\t([A-Za-z]+[A-Za-z0-9]*)\t([A-Za-z0-9.]+)\t([A-Za-z0-9.]+)\\s*");
const regex tri06("^DIV\t([A-Za-z]+[A-Za-z0-9]*)\t([A-Za-z0-9.]+)\t([A-Za-z0-9.]+)\\s*");
const regex tri07("^MOD\t([A-Za-z]+[A-Za-z0-9]*)\t([A-Za-z0-9.]+)\t([A-Za-z0-9.]+)\\s*");
const regex tri08("^TAR\t([A-Za-z]+[A-Za-z0-9]*)\t([A-Za-z0-9.]+)\t([A-Za-z0-9.]+)\\s*");
const regex tri09("^FAR\t([A-Za-z]+[A-Za-z0-9]*)\t([A-Za-z]+[A-Za\tz0-9]*)\t([A-Za-z0-9.]+)\\s*");
const regex tri10("^ADDR\t([A-Za-z]+[A-Za-z0-9]*)\t([A-Za-z]+[A-Za-z0-9]*)\t-\\s*");
const regex tri11("^JMP\t([A-Za-z]+[A-Za-z0-9]*)\t-\t-\\s*");
const regex tri12("^JGT\t([A-Za-z0-9.]+)\t([A-Za-z0-9.]+)\t([A-Za-z]+[A-Za-z0-9]*)\\s*");
const regex tri13("^JLT\t([A-Za-z0-9.]+)\t([A-Za-z0-9.]+)\t([A-Za-z]+[A-Za-z0-9]*)\\s*");
const regex tri14("^JEQ\t([A-Za-z0-9.]+)\t([A-Za-z0-9.]+)\t([A-Za-z]+[A-Za-z0-9]*)\\s*");
const regex tri15("^LABEL\t([A-Za-z0-9.]+)\t-\t-\\s*");
const regex tri16("^HALT\t-\t-\t-\\s*");

int main()
{
    std::string s;
    while (std::getline(cin, s))
    {
        // s.erase(s.end() - 1); // for windows CR LF
        if (regex_match(s, tri00))
        {
            smatch m;
            auto ret = regex_match(s, m, tri00);
            cout << "READ " << *(m.begin() + 1) << "\n";
        }
        else if (regex_match(s, tri01))
        {
            smatch m;
            auto ret = regex_match(s, m, tri01);
            cout << "WRITE " << *(m.begin() + 1) << "\n";
        }
        else if (regex_match(s, tri02))
        {
            smatch m;
            auto ret = regex_match(s, m, tri02);
            cout << *(m.begin() + 1) << " := " << *(m.begin() + 2) << "\n";
        }
        else if (regex_match(s, tri03))
        {
            smatch m;
            auto ret = regex_match(s, m, tri03);
            cout << *(m.begin() + 1) << " := " << *(m.begin() + 2) << " + " << *(m.begin() + 3) << "\n";
        }
        else if (regex_match(s, tri04))
        {
            smatch m;
            auto ret = regex_match(s, m, tri04);
            cout << *(m.begin() + 1) << " := " << *(m.begin() + 2) << " - " << *(m.begin() + 3) << "\n";
        }
        else if (regex_match(s, tri05))
        {
            smatch m;
            auto ret = regex_match(s, m, tri05);
            cout << *(m.begin() + 1) << " := " << *(m.begin() + 2) << " * " << *(m.begin() + 3) << "\n";
        }
        else if (regex_match(s, tri06))
        {
            smatch m;
            auto ret = regex_match(s, m, tri06);
            cout << *(m.begin() + 1) << " := " << *(m.begin() + 2) << " / " << *(m.begin() + 3) << "\n";
        }
        else if (regex_match(s, tri07))
        {
            smatch m;
            auto ret = regex_match(s, m, tri07);
            cout << *(m.begin() + 1) << " := " << *(m.begin() + 2) << " % " << *(m.begin() + 3) << "\n";
        }
        else if (regex_match(s, tri08))
        {
            smatch m;
            auto ret = regex_match(s, m, tri08);
            cout << *(m.begin() + 1) << "[" << *(m.begin() + 2) << "] := " << *(m.begin() + 3) << "\n";
        }
        else if (regex_match(s, tri09))
        {
            smatch m;
            auto ret = regex_match(s, m, tri09);
            cout << *(m.begin() + 1) << " := " << *(m.begin() + 2) << "[" << *(m.begin() + 3) << "]\n";
        }
        else if (regex_match(s, tri10))
        {
            smatch m;
            auto ret = regex_match(s, m, tri10);
            cout << *(m.begin() + 1) << " := ADDR(" << *(m.begin() + 2) << ")\n";
        }
        else if (regex_match(s, tri11))
        {
            smatch m;
            auto ret = regex_match(s, m, tri11);
            cout << "GOTO " << *(m.begin() + 1) << "\n";
        }
        else if (regex_match(s, tri12))
        {
            smatch m;
            auto ret = regex_match(s, m, tri12);
            cout << "IF " << *(m.begin() + 1) << " > " << *(m.begin() + 2) << " GOTO " << *(m.begin() + 3) << "\n";
        }
        else if (regex_match(s, tri13))
        {
            smatch m;
            auto ret = regex_match(s, m, tri13);
            cout << "IF " << *(m.begin() + 1) << " < " << *(m.begin() + 2) << " GOTO " << *(m.begin() + 3) << "\n";
        }
        else if (regex_match(s, tri14))
        {
            smatch m;
            auto ret = regex_match(s, m, tri14);
            cout << "IF " << *(m.begin() + 1) << " = " << *(m.begin() + 2) << " GOTO " << *(m.begin() + 3) << "\n";
        }
        else if (regex_match(s, tri15))
        {
            smatch m;
            auto ret = regex_match(s, m, tri15);
            cout << "L: " << *(m.begin() + 1) << "\n";
        }
        else if (regex_match(s, tri16))
        {
            cout << "HALT\n";
        }
        else
        {
            cout << s << "\n";
            cout << "Unknown\n";
        };
    };
    return 0;
}