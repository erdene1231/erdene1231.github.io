#include <bits/stdc++.h>
using namespace std;
using ll = long long;

pair<int, ll> move(const vector<ll> &a, bool misere) {
    ll s = 0;
    int ones = 0, big = 0, pos = -1;
    for (int i = 0; i < (int)a.size(); i++) {
        s ^= a[i];
        ones += a[i] == 1;
        if (a[i] > 1) big++, pos = i;
    }
    if (misere && big == 0) {
        if (ones % 2 == 0) {
            for (int i = 0; i < (int)a.size(); i++) if (a[i]) return {i, 1};
        }
        return {-1, 0};
    }
    if (misere && big == 1) {
        ll target = ones % 2 == 0 ? 1 : 0;
        return {pos, a[pos] - target};
    }
    if (s == 0) return {-1, 0};
    for (int i = 0; i < (int)a.size(); i++) {
        ll target = a[i] ^ s;
        if (target < a[i]) return {i, a[i] - target};
    }
    return {-1, 0};
}

int main() {
    char mode;
    int n;
    cin >> mode >> n;
    vector<ll> a(n);
    bool empty = true;
    for (ll &x : a) {
        cin >> x;
        if (x) empty = false;
    }
    bool misere = mode == 'M';
    if (empty) {
        cout << (misere ? "TERMINAL WIN\n" : "TERMINAL LOSE\n");
        return 0;
    }
    auto [i, take] = move(a, misere);
    if (i == -1) cout << "LOSE\n";
    else cout << "WIN " << i + 1 << ' ' << take << '\n';
}
