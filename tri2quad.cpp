#include <bits/stdc++.h>

using namespace std;

const regex tri00("^READ:([A-Za-z]+[A-Za-z0-9]*)");
const regex tri01("^WRITE:([A-Za-z]+[A-Za-z0-9]*)");
const regex tri02("^([A-Za-z]+[A-Za-z0-9]*):=([A-Za-z0-9.]+)");
const regex tri03("^([A-Za-z]+[A-Za-z0-9]*):=([A-Za-z0-9.]+)\\+([A-Za-z0-9.]+)");
const regex tri04("^([A-Za-z]+[A-Za-z0-9]*):=([A-Za-z0-9.]+)-([A-Za-z0-9.]+)");
const regex tri05("^([A-Za-z]+[A-Za-z0-9]*):=([A-Za-z0-9.]+)\\*([A-Za-z0-9.]+)");
const regex tri06("^([A-Za-z]+[A-Za-z0-9]*):=([A-Za-z0-9.]+)/([A-Za-z0-9.]+)");
const regex tri07("^([A-Za-z]+[A-Za-z0-9]*):=([A-Za-z0-9.]+)%([A-Za-z0-9.]+)");
const regex tri08("^([A-Za-z]+[A-Za-z0-9]*)\\[([A-Za-z0-9.]+)\\]:=([A-Za-z0-9.]+)");
const regex tri09("^([A-Za-z]+[A-Za-z0-9]*):=([A-Za-z]+[A-Za-z0-9]*)\\[([A-Za-z0-9.]+)\\]");
const regex tri10("^([A-Za-z]+[A-Za-z0-9]*):=ADDR\\(([A-Za-z]+[A-Za-z0-9]*)\\)");
const regex tri11("^:->([A-Za-z]+[A-Za-z0-9]*)");
const regex tri12("^\\?([A-Za-z0-9.]+)>([A-Za-z0-9.]+):->([A-Za-z]+[A-Za-z0-9]*)");
const regex tri13("^\\?([A-Za-z0-9.]+)<([A-Za-z0-9.]+):->([A-Za-z]+[A-Za-z0-9]*)");
const regex tri14("^\\?([A-Za-z0-9.]+)=([A-Za-z0-9.]+):->([A-Za-z]+[A-Za-z0-9]*)");
const regex tri15("^L:([A-Za-z0-9.]+)");
const regex tri16("^HALT");

int main()
{
    std::string s;
    while (std::cin >> s)
    {
        if (regex_match(s, tri00))
        {
            smatch m;
            auto ret = regex_match(s, m, tri00);
            cout << "READ ";
            for (auto pos = m.begin() + 1; pos != m.end(); ++pos)
            {
                cout << *pos << " ";
            };
            cout << "- -\n";
        }
        else if (regex_match(s, tri01))
        {
            smatch m;
            auto ret = regex_match(s, m, tri01);
            cout << "WRITE ";
            for (auto pos = m.begin() + 1; pos != m.end(); ++pos)
            {
                cout << *pos << " ";
            };
            cout << "- -\n";
        }
        else if (regex_match(s, tri02))
        {
            smatch m;
            auto ret = regex_match(s, m, tri02);
            cout << "SET ";
            for (auto pos = m.begin() + 1; pos != m.end(); ++pos)
            {
                cout << *pos << " ";
            };
            cout << "-\n";
        }
        else if (regex_match(s, tri03))
        {
            smatch m;
            auto ret = regex_match(s, m, tri03);
            cout << "ADD ";
            for (auto pos = m.begin() + 1; pos != m.end(); ++pos)
            {
                cout << *pos << " ";
            };
            cout << endl;
        }
        else if (regex_match(s, tri04))
        {
            smatch m;
            auto ret = regex_match(s, m, tri04);
            cout << "SUB ";
            for (auto pos = m.begin() + 1; pos != m.end(); ++pos)
            {
                cout << *pos << " ";
            };
            cout << endl;
        }
        else if (regex_match(s, tri05))
        {
            smatch m;
            auto ret = regex_match(s, m, tri05);
            cout << "MUL ";
            for (auto pos = m.begin() + 1; pos != m.end(); ++pos)
            {
                cout << *pos << " ";
            };
            cout << endl;
        }
        else if (regex_match(s, tri06))
        {
            smatch m;
            auto ret = regex_match(s, m, tri06);
            cout << "DIV ";
            for (auto pos = m.begin() + 1; pos != m.end(); ++pos)
            {
                cout << *pos << " ";
            };
            cout << endl;
        }
        else if (regex_match(s, tri07))
        {
            smatch m;
            auto ret = regex_match(s, m, tri07);
            cout << "MOD ";
            for (auto pos = m.begin() + 1; pos != m.end(); ++pos)
            {
                cout << *pos << " ";
            };
            cout << endl;
        }
        else if (regex_match(s, tri08))
        {
            smatch m;
            auto ret = regex_match(s, m, tri08);
            cout << "TAR ";
            for (auto pos = m.begin() + 1; pos != m.end(); ++pos)
            {
                cout << *pos << " ";
            };
            cout << endl;
        }
        else if (regex_match(s, tri09))
        {
            smatch m;
            auto ret = regex_match(s, m, tri09);
            cout << "FAR ";
            for (auto pos = m.begin() + 1; pos != m.end(); ++pos)
            {
                cout << *pos << " ";
            };
            cout << endl;
        }
        else if (regex_match(s, tri10))
        {
            smatch m;
            auto ret = regex_match(s, m, tri10);
            cout << "ADDR ";
            for (auto pos = m.begin() + 1; pos != m.end(); ++pos)
            {
                cout << *pos << " ";
            };
            cout << "-\n";
        }
        else if (regex_match(s, tri11))
        {
            smatch m;
            auto ret = regex_match(s, m, tri11);
            cout << "JMP ";
            for (auto pos = m.begin() + 1; pos != m.end(); ++pos)
            {
                cout << *pos << " ";
            };
            cout << "- -\n";
        }
        else if (regex_match(s, tri12))
        {
            smatch m;
            auto ret = regex_match(s, m, tri12);
            cout << "JGT ";
            for (auto pos = m.begin() + 1; pos != m.end(); ++pos)
            {
                cout << *pos << " ";
            };
            cout << endl;
        }
        else if (regex_match(s, tri13))
        {
            smatch m;
            auto ret = regex_match(s, m, tri13);
            cout << "JLT ";
            for (auto pos = m.begin() + 1; pos != m.end(); ++pos)
            {
                cout << *pos << " ";
            };
            cout << endl;
        }
        else if (regex_match(s, tri14))
        {
            smatch m;
            auto ret = regex_match(s, m, tri14);
            cout << "JEQ ";
            for (auto pos = m.begin() + 1; pos != m.end(); ++pos)
            {
                cout << *pos << " ";
            };
            cout << endl;
        }
        else if (regex_match(s, tri15))
        {
            smatch m;
            auto ret = regex_match(s, m, tri15);
            cout << "LABLE ";
            for (auto pos = m.begin() + 1; pos != m.end(); ++pos)
            {
                cout << *pos << " ";
            };
            cout << "- -\n";
        }
        else if (regex_match(s, tri16))
        {
            cout << "HALT - - -\n";
        }
        else
        {
            cout << s << endl;
            cout << "Unknown\n";
        };
    };
    return 0;
}