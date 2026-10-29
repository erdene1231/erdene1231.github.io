#include <bits/stdc++.h>
using namespace std;
using ll = long long;

const int MOD = 1000000007;

ll modpow(ll a, int n) {
    ll res = 1;
    while (n) {
        if (n & 1) res = res * a % MOD;
        a = a * a % MOD;
        n >>= 1;
    }
    return res;
}

ll det(vector<vector<ll>> a) {
    int n = a.size();
    ll res = 1;
    for (int i = 0; i < n; i++) {
        int p = i;
        while (p < n && a[p][i] == 0) p++;
        if (p == n) return 0;
        if (p != i) {
            swap(a[p], a[i]);
            res = (MOD - res) % MOD;
        }
        res = res * a[i][i] % MOD;
        ll inv = modpow(a[i][i], MOD - 2);
        for (int r = i + 1; r < n; r++) {
            ll c = a[r][i] * inv % MOD;
            for (int j = i; j < n; j++) {
                a[r][j] = (a[r][j] - c * a[i][j] % MOD + MOD) % MOD;
            }
        }
    }
    return res;
}

int main() {
    int n, m, root;
    cin >> n >> m >> root; // 1 <= n <= 150; m <= 10000; 1 <= root <= n
    --root;
    vector<vector<ll>> l(n, vector<ll>(n));
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        --a;
        --b;
        if (a == b) continue; // self-loops cannot belong to a spanning tree
        l[a][a]++;
        l[b][b]++;
        l[a][b]--;
        l[b][a]--;
    }
    vector<vector<ll>> a;
    for (int i = 0; i < n; i++) {
        if (i == root) continue;
        vector<ll> row;
        for (int j = 0; j < n; j++) {
            if (j != root) row.push_back((l[i][j] % MOD + MOD) % MOD);
        }
        a.push_back(row);
    }
    cout << det(a) << "\n"; // the empty minor for n=1 has determinant1
}
