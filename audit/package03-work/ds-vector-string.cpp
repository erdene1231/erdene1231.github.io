#include <bits/stdc++.h>
using namespace std;

int main() {
    vector<int> v;
    v.push_back(3);
    v.push_back(2);
    v.push_back(5);
    cout << v[0] << " " << v[1] << " " << v[2] << "\n";
    for (int i = 0; i < (int)v.size(); i++) cout << v[i] << " ";
    cout << "\n";
    for (int x : v) cout << x << " ";
    cout << "\n";
    v = {5, 2};
    cout << v.back() << "\n";
    v.pop_back();
    cout << v.back() << "\n";
    vector<int> a = {2, 4, 2, 5, 1};
    vector<int> zeros(10);
    vector<int> fives(10, 5);
    cout << a.size() << " " << zeros[0] << " " << fives[0] << "\n";
    string s = "hatti";
    string t = s + s;
    cout << t << "\n";
    t[5] = 'v';
    cout << t << "\n";
    string part = t.substr(3, 4);
    cout << part << "\n";
    auto pos = t.find("vatti");
    if (pos != string::npos) cout << pos << "\n";
    return 0;
}
