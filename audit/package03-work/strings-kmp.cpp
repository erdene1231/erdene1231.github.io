#include <bits/stdc++.h>
using namespace std;
using ll = long long;

vector<int> prefix_function(const string &s) {
    int n = (int)s.size();
    vector<int> pi(n);
    for (int i = 1; i < n; i++) {
        int j = pi[i - 1];
        while (j && s[i] != s[j]) j = pi[j - 1];
        if (s[i] == s[j]) j++;
        pi[i] = j;
    }
    return pi;
}

vector<int> matches(const string &s, const string &p) {
    int n = (int)s.size(), m = (int)p.size();
    vector<int> ans;
    if (m == 0) {
        for (int i = 0; i <= n; i++) ans.push_back(i);
        return ans;
    }
    auto pi = prefix_function(p);
    int j = 0;
    for (int i = 0; i < n; i++) {
        while (j && s[i] != p[j]) j = pi[j - 1];
        if (s[i] == p[j]) j++;
        if (j == m) {
            ans.push_back(i - m + 1);
            j = pi[j - 1];
        }
    }
    return ans;
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
    auto pi = prefix_function(s);
    print(pi);
    print(matches(s, p));
    int n = (int)s.size();
    vector<int> borders;
    for (int k = n; k; k = pi[k - 1]) borders.push_back(k);
    reverse(borders.begin(), borders.end());
    print(borders);
    int partial = n ? n - pi.back() : 0;
    int whole = n && n % partial == 0 ? partial : n;
    cout << partial << ' ' << whole << '\n';
}
