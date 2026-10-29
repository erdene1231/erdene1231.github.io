#include <bits/stdc++.h>
using namespace std;
using ll = long long;

array<int, 4> squares(int n) {
    vector<pair<int, int>> pos(n + 1, {-1, -1});
    for (int a = 0; a * a <= n; a++) {
        for (int b = 0; a * a + b * b <= n; b++) {
            pos[a * a + b * b] = {a, b};
        }
    }
    for (int s = 0; s <= n; s++) {
        auto [a, b] = pos[s];
        auto [c, d] = pos[n - s];
        if (a != -1 && c != -1) return {a, b, c, d};
    }
    return {-1, -1, -1, -1};
}

vector<ll> zeckendorf(ll n) {
    vector<ll> f = {1, 2}, res;
    while (f.back() <= n) {
        int k = f.size();
        f.push_back(f[k - 1] + f[k - 2]);
    }
    for (int i = (int)f.size() - 1; i >= 0; i--) {
        if (f[i] <= n) {
            res.push_back(f[i]);
            n -= f[i];
        }
    }
    return res;
}

vector<array<ll, 3>> triples(int cmax) {
    vector<array<ll, 3>> res;
    for (ll n = 2; n * n + 1 <= cmax; n++) {
        for (ll m = 1; m < n && n * n + m * m <= cmax; m++) {
            if (gcd(n, m) != 1 || (n - m) % 2 == 0) continue;
            ll a = n * n - m * m, b = 2 * n * m, c = n * n + m * m;
            if (a > b) swap(a, b);
            res.push_back({a, b, c});
        }
    }
    sort(res.begin(), res.end());
    return res;
}

bool wilson(int n) {
    if (n < 2) return false;
    ll f = 1;
    for (int x = 1; x < n; x++) f = f * x % n;
    return f == n - 1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    char mode;
    ll n;
    cin >> mode >> n;
    if (mode == 'S') { // 0 <= n <= 10000
        auto a = squares((int)n);
        for (int x : a) cout << x << ' ';
        cout << "\n";
    } else if (mode == 'Z') { // 1 <= n <= 10^18
        auto a = zeckendorf(n);
        cout << a.size();
        for (ll x : a) cout << ' ' << x;
        cout << "\n";
    } else if (mode == 'P') { // 1 <= n <= 10^6; primitive triples only
        auto a = triples((int)n);
        cout << a.size() << "\n";
        for (auto [x, y, z] : a) cout << x << ' ' << y << ' ' << z << "\n";
    } else { // Wilson: 0 <= n <= 10000
        cout << wilson((int)n) << "\n";
    }
}
