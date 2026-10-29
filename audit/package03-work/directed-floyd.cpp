#include <bits/stdc++.h>
using namespace std;
using ll = long long;

tuple<int, int, int> seenCycle(const vector<int> &succ, int x) {
    vector<int> seen(succ.size(), -1);
    int t = 0;
    while (seen[x] == -1) {
        seen[x] = t++;
        x = succ[x];
    }
    return {x, seen[x], t - seen[x]};
}

tuple<int, int, int> floyd(const vector<int> &succ, int x) {
    int a = succ[x], b = succ[succ[x]];
    while (a != b) {
        a = succ[a];
        b = succ[succ[b]];
    }
    a = x;
    int mu = 0;
    while (a != b) {
        a = succ[a];
        b = succ[b];
        mu++;
    }
    int first = a, len = 1;
    b = succ[a];
    while (a != b) {
        b = succ[b];
        len++;
    }
    return {first, mu, len};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, x;
    cin >> n >> x;
    vector<int> succ(n + 1);
    for (int u = 1; u <= n; u++) cin >> succ[u];
    auto [a, mu, len] = floyd(succ, x);
    cout << a << ' ' << mu << ' ' << len << '\n';
    auto [b, pre, size] = seenCycle(succ, x);
    cout << b << ' ' << pre << ' ' << size << '\n';
}
