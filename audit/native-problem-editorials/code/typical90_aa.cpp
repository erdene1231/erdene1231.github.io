#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    set<string> seen;
    for (int day = 1; day <= n; ++day) {
        string s;
        cin >> s;
        if (seen.insert(s).second) cout << day << '\n';
    }
}
