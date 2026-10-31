#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Query {
    int mask;
    ll value;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<Query> queries;
    for (int i = 0; i < q; ++i) {
        int x, y, z;
        ll w;
        cin >> x >> y >> z >> w;
        queries.push_back({(1 << (x - 1)) | (1 << (y - 1)) | (1 << (z - 1)), w});
    }
    const ll mod = 1000000007;
    ll ans = 1;
    for (int bit = 0; bit < 60; ++bit) {
        int count = 0;
        for (int mask = 0; mask < (1 << n); ++mask) {
            bool ok = true;
            for (const auto &query : queries) {
                if (bool(mask & query.mask) != bool(query.value >> bit & 1LL)) {
                    ok = false;
                    break;
                }
            }
            if (ok) ++count;
        }
        ans = ans * count % mod;
    }
    cout << ans << '\n';
}
