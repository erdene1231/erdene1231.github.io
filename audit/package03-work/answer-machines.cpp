#include <bits/stdc++.h>
using namespace std;
using ll = long long;

bool machineOk(const vector<ll> &a, ll goal, ll t) {
    if (goal == 0) return true;
    ll need = goal;
    for (ll v : a) {
        ll made = t / v;
        if (made >= need) return true;
        need -= made;
    }
    return false;
}

ll firstTime(const vector<ll> &a, ll goal, ll cap) {
    if (!machineOk(a, goal, cap)) return -1;
    ll l = 0, r = cap;
    while (l < r) {
        ll mid = l + (r - l) / 2;
        if (machineOk(a, goal, mid)) r = mid;
        else l = mid + 1;
    }
    return l;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    ll goal, cap;
    cin >> n >> goal >> cap;
    vector<ll> a(n);
    for (ll &v : a) cin >> v;
    cout << firstTime(a, goal, cap) << '\n';
}
