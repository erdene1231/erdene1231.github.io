#include <bits/stdc++.h>
using namespace std;
using ll = long long;

vector<int> encode(const string &s) {
    vector<int> a;
    for (unsigned char c : s) a.push_back((int)c + 1);
    return a;
}

vector<int> z_function(const vector<int> &s) {
    int n = (int)s.size(), l = 0, r = 0;
    vector<int> z(n);
    for (int i = 1; i < n; i++) {
        if (i < r) z[i] = min(r - i, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) z[i]++;
        if (i + z[i] > r) l = i, r = i + z[i];
    }
    return z;
}

void print(const vector<int> &a) {
    cout << a.size();
    for (int x : a) cout << ' ' << x;
    cout << '\n';
}

int main() {
    string s, p;
    getline(cin, s);
    getline(cin, p);
    print(z_function(encode(s)));
    auto a = encode(p), text = encode(s);
    a.push_back(0);
    a.insert(a.end(), text.begin(), text.end());
    auto z = z_function(a);
    print(z);
    int n = (int)s.size(), m = (int)p.size();
    vector<int> ans;
    if (m == 0) {
        for (int i = 0; i <= n; i++) ans.push_back(i);
    } else {
        for (int i = m + 1; i < (int)a.size(); i++) if (z[i] >= m) ans.push_back(i - m - 1);
    }
    print(ans);
}
