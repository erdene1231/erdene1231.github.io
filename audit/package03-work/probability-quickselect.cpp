#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll select_k(vector<ll> &a, int k, mt19937_64 &rng) {
    int l = 0, r = (int)a.size() - 1;
    while (true) {
        ll x = a[uniform_int_distribution<int>(l, r)(rng)];
        int lt = l, i = l, gt = r;
        while (i <= gt) {
            if (a[i] < x) swap(a[lt++], a[i++]);
            else if (a[i] > x) swap(a[i], a[gt--]);
            else i++;
        }
        if (k < lt) r = lt - 1;
        else if (k > gt) l = gt + 1;
        else return x;
    }
}

int main() {
    int n, k;
    unsigned long long seed;
    cin >> n >> k >> seed;
    vector<ll> a(n);
    for (auto &x : a) cin >> x;
    mt19937_64 rng(seed);
    cout << select_k(a, k - 1, rng) << '\n';
}
