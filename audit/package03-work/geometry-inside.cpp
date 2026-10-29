#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Point {
    ll x, y;
};
ll cross(Point a, Point b, Point p) {
    return (b.x - a.x) * (p.y - a.y) - (b.y - a.y) * (p.x - a.x);
}

bool onSegment(Point a, Point b, Point p) {
    return cross(a, b, p) == 0 &&
        min(a.x, b.x) <= p.x && p.x <= max(a.x, b.x) &&
        min(a.y, b.y) <= p.y && p.y <= max(a.y, b.y);
}
string locate(const vector<Point> &a, Point p) {
    bool inside = false;
    int n = (int) a.size();
    for (int i = 0; i < n; i++) {
        Point u = a[i], v = a[(i + 1) % n];
        if (onSegment(u, v, p)) return "BOUNDARY";
        if ((u.y > p.y) != (v.y > p.y)) {
            ll c = cross(u, v, p);
            if ((c > 0) == (v.y > u.y)) inside = !inside;
        }
    }
    return inside ? "INSIDE" : "OUTSIDE";
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<Point> a(n);
    for (Point &p : a) cin >> p.x >> p.y;
    while (q--) {
        Point p;
        cin >> p.x >> p.y;
        cout << locate(a, p) << '\n';
    }
}
