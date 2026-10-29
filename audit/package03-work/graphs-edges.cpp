#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, dir, q;
    cin >> n >> m >> dir >> q;
    vector<pair<int, int>> edges;
    for (int i = 0, a, b; i < m; i++) {
        cin >> a >> b;
        edges.push_back({a, b});
    }
    for (auto [a, b] : edges) cout << a << ' ' << b << '\n';
    while (q--) {
        int s;
        cin >> s;
        cout << s << ':';
        for (auto [a, b] : edges) {
            if (a == s) cout << ' ' << b;
            if (!dir && b == s) cout << ' ' << a;
        }
        cout << '\n';
    }
}
