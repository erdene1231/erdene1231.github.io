#include <bits/stdc++.h>
using namespace std;

using ull = unsigned long long;

struct MaskSet {
    int n;
    ull mask, limit;
    MaskSet(int _n) {
        n = _n;
        mask = 0;
        limit = (1ULL << n) - 1;
    }
    void add(int k) { mask |= 1ULL << k; }
    void erase(int k) { mask &= ~(1ULL << k); }
    bool contains(int k) const { return mask & (1ULL << k); }
    int size() const { return __builtin_popcountll(mask); }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, a, b, k;
    cin >> n >> a >> b >> k;
    MaskSet x(n), y(n);
    for (int i = 0, v; i < a; i++) {
        cin >> v;
        x.add(v);
    }
    for (int i = 0, v; i < b; i++) {
        cin >> v;
        y.add(v);
    }
    cout << x.mask << ' ' << x.size() << '\n';
    for (int i = 0; i < n; i++) if (x.contains(i)) cout << i << ' ';
    cout << '\n';
    cout << (x.mask & y.mask) << ' ' << (x.mask | y.mask) << ' ' << ((~x.mask) & x.limit) << ' ' << (x.mask & ~y.mask) << '\n';
    for (ull s = 0; s <= x.limit; s++) cout << s << ' ';
    cout << '\n';
    for (ull s = 0; s <= x.limit; s++) {
        if (__builtin_popcountll(s) == k) cout << s << ' ';
    }
    cout << '\n';
    ull s = 0;
    do {
        cout << s << ' ';
        s = (s - x.mask) & x.mask;
    } while (s != 0);
    cout << '\n';
}
