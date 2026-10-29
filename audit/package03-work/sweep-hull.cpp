#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Point {
    ll x, y;
    bool operator<(Point p) const {
        return tie(x, y) < tie(p.x, p.y);
    }
    bool operator==(Point p) const {
        return x == p.x && y == p.y;
    }
};

ll cross(Point a, Point b, Point c) {
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
}
vector<Point> hull(vector<Point> a, bool keep) {
    sort(a.begin(), a.end());
    a.erase(unique(a.begin(), a.end()), a.end());
    int n = (int) a.size();
    if (n <= 1) return a;
    bool line = true;
    for (int i = 1; i + 1 < n; i++) {
        if (cross(a.front(), a.back(), a[i]) != 0) line = false;
    }
    if (line) return keep ? a : vector<Point>{a.front(), a.back()};
    auto chain = [&](const vector<Point> &p) {
        vector<Point> h;
        for (Point q : p) {
            while (h.size() >= 2) {
                ll c = cross(h[h.size() - 2], h.back(), q);
                if (keep ? c >= 0 : c > 0) break;
                h.pop_back();
            }
            h.push_back(q);
        }
        return h;
    };
    vector<Point> lower = chain(a);
    reverse(a.begin(), a.end());
    vector<Point> upper = chain(a);
    lower.pop_back();
    upper.pop_back();
    lower.insert(lower.end(), upper.begin(), upper.end());
    return lower;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string mode;
    int n;
    cin >> mode >> n;
    vector<Point> a(n);
    for (Point &p : a) cin >> p.x >> p.y;
    vector<Point> h = hull(a, mode == "BOUNDARY");
    cout << h.size() << '\n';
    for (Point p : h) cout << p.x << ' ' << p.y << '\n';
}
