#include <bits/stdc++.h>
using namespace std;
using ll = long long;

vector<int> grundy(int n) {
    vector<int> g(n + 1), seen(n + 1, -1);
    for (int k = 1; k <= n; k++) {
        int d = (k - 1) / 2;
        for (int a = 1; a < k - a; a++) {
            int x = g[a] ^ g[k - a];
            if (x <= d) seen[x] = k;
        }
        while (g[k] <= d && seen[g[k]] == k) g[k]++;
    }
    return g;
}

int main() {
    int q, n = 0;
    cin >> q;
    vector<int> a(q);
    for (int &x : a) {
        cin >> x;
        n = max(n, x);
    }
    auto g = grundy(n);
    int s = 0;
    for (int x : a) s ^= g[x];
    for (int k = 1; k <= n; k++) cout << g[k] << ' ';
    cout << '\n';
    if (s == 0) cout << "LOSE\n";
    else {
        for (int i = 0; i < q; i++) {
            int target = g[a[i]] ^ s;
            if (target >= g[a[i]]) continue;
            for (int x = 1; x < a[i] - x; x++) {
                if ((g[x] ^ g[a[i] - x]) == target) {
                    cout << "WIN " << i + 1 << ' ' << x << ' ' << a[i] - x << '\n';
                    return 0;
                }
            }
        }
    }
}
