#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Point {
    ll x, y;
    int id;
    bool operator<(const Point &p) const {
        return tie(x, y, id) < tie(p.x, p.y, p.id);
    }
};

ll distance2(Point a, Point b) {
    ll dx = a.x - b.x, dy = a.y - b.y;
    return dx * dx + dy * dy;
}

ll isqrt(ll x) {
    ll l = 0, r = 3000000000LL;
    while (l < r) {
        ll mid = (l + r + 1) / 2;
        if (mid <= x / mid) l = mid;
        else r = mid - 1;
    }
    return l;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<Point> p(n);
    for (int i = 0; i < n; i++) {
        cin >> p[i].x >> p[i].y;
        p[i].id = i;
    }
    if (n < 2) {
        cout << "NONE\n";
        return 0;
    }
    sort(p.begin(), p.end());
    for (int i = 1; i < n; i++) {
        if (p[i].x == p[i - 1].x && p[i].y == p[i - 1].y) {
            cout << 0 << ' ' << p[i - 1].id << ' ' << p[i].id << '\n';
            return 0;
        }
    }
    ll best = distance2(p[0], p[1]);
    int a = p[0].id, b = p[1].id, left = 0;
    set<tuple<ll, ll, int>> active;
    active.insert({p[0].y, p[0].x, p[0].id});
    active.insert({p[1].y, p[1].x, p[1].id});
    for (int i = 2; i < n; i++) {
        ll x = p[i].x, y = p[i].y;
        while (left < i) {
            ll dx = x - p[left].x;
            if (dx * dx <= best) break;
            active.erase({p[left].y, p[left].x, p[left].id});
            left++;
        }
        ll d = isqrt(best);
        auto it = active.lower_bound({y - d, LLONG_MIN, -1});
        while (it != active.end() && get<0>(*it) <= y + d) {
            auto [py, px, id] = *it;
            ll value = distance2(p[i], {px, py, id});
            if (value < best) {
                best = value;
                a = id;
                b = p[i].id;
            }
            it++;
        }
        active.insert({y, x, p[i].id});
    }
    cout << best << ' ' << a << ' ' << b << '\n';
}
