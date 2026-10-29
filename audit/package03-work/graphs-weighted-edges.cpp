#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, dir, q;
    cin >> n >> m >> dir >> q;
    vector<tuple<int, int, ll>> edges;
    for (int i = 0; i < m; i++) {
        int a, b;
        ll w;
        cin >> a >> b >> w;
        edges.push_back({a, b, w});
    }
    for (auto [a, b, w] : edges) cout << a << ' ' << b << ' ' << w << '\n';
    while (q--) {
        int s;
        cin >> s;
        cout << s << ':';
        for (auto [a, b, w] : edges) {
            if (a == s) cout << ' ' << b << ':' << w;
            if (!dir && b == s) cout << ' ' << a << ':' << w;
        }
        cout << '\n';
    }
}
