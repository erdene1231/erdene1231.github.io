#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll fast(const vector<ll> &a) {
    int n = (int)a.size();
    assert(n > 0);
    vector<ll> f(n, 0);
    f[0] = 1;
    ll s = 0, ans = 0;
    for (ll x : a) {
        s = (s + x) % n;
        if (s < 0) s += n;
        assert(0 <= s && s < n);
        ans += f[s];
        f[s]++;
    }
    return ans;
}

ll brute(const vector<ll> &a) {
    int n = (int)a.size();
    ll ans = 0;
    for (int l = 0; l < n; l++) {
        ll s = 0;
        for (int r = l; r < n; r++) {
            s += a[r];
            if (s % n == 0) ans++;
        }
    }
    return ans;
}

// Deliberately wrong: used only to demonstrate a reproducible failure.
ll broken(const vector<ll> &a) {
    int n = (int)a.size();
    vector<ll> f(n, 0);
    ll s = 0, ans = 0;
    for (ll x : a) {
        s = (s + x) % n;
        if (s < 0) s += n;
        ans += f[s];
        f[s]++;
    }
    return ans;
}

bool fails(const vector<ll> &a) {
    return brute(a) != broken(a);
}
vector<ll> shrink(vector<ll> a) {
    bool changed = true;
    while (changed && a.size() > 1) {
        changed = false;
        for (int i = 0; i < (int)a.size(); i++) {
            auto b = a;
            b.erase(b.begin() + i);
            if (fails(b)) {
                a = move(b);
                changed = true;
                break;
            }
        }
    }
    for (int i = 0; i < (int)a.size(); i++) {
        auto b = a;
        b[i] = 0;
        if (fails(b)) a = move(b);
    }
    return a;
}

bool check(const vector<ll> &a) {
    ll want = brute(a), got = fast(a);
    if (want == got) return true;
    cerr << "input:\n" << a.size() << '\n';
    for (ll x : a) cerr << x << ' ';
    cerr << "\nexpected " << want << " actual " << got << '\n';
    return false;
}

int main() {
    unsigned seed;
    int rounds;
    cin >> seed >> rounds;
    assert(0 <= rounds && rounds <= 10000);
    auto small = shrink({3, 0, -3});
    cout << "broken example:\n" << small.size() << '\n';
    for (ll x : small) cout << x << ' ';
    cout << "\nexpected " << brute(small) << " actual " << broken(small) << '\n';
    int tested = 0;
    for (int n = 1; n <= 6; n++) {
        int total = 1;
        for (int i = 0; i < n; i++) total *= 5;
        for (int mask = 0; mask < total; mask++) {
            int z = mask;
            vector<ll> a(n);
            for (ll &x : a) {
                x = z % 5 - 2;
                z /= 5;
            }
            if (!check(a)) return 1;
            tested++;
        }
    }
    mt19937 rng(seed);
    for (int t = 0; t < rounds; t++) {
        int n = uniform_int_distribution<int>(1, 30)(rng);
        vector<ll> a(n);
        for (ll &x : a) x = uniform_int_distribution<int>(-100, 100)(rng);
        if (!check(a)) {
            cerr << "seed " << seed << " round " << t << '\n';
            return 1;
        }
        tested++;
    }
    cout << "checked " << tested << '\n';
}
