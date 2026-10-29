#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Point {
    ll x, y;
    bool operator==(Point p) const {
        return x == p.x && y == p.y;
    }
};
ll cross(Point a, Point b, Point p) {
    return (b.x - a.x) * (p.y - a.y) - (b.y - a.y) * (p.x - a.x);
}

using ld = long double;

ld distance(Point a, Point b) {
    return hypotl((ld) b.x - a.x, (ld) b.y - a.y);
}

ld lineDistance(Point a, Point b, Point p) {
    return fabsl((ld) cross(a, b, p)) / distance(a, b);
}

ld segmentDistance(Point a, Point b, Point p) {
    if (a == b) return distance(a, p);
    ll dx = b.x - a.x, dy = b.y - a.y;
    ll dot = (p.x - a.x) * dx + (p.y - a.y) * dy;
    ll len2 = dx * dx + dy * dy;
    if (dot <= 0) return distance(a, p);
    if (dot >= len2) return distance(b, p);
    return lineDistance(a, b, p);
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    cout << fixed << setprecision(12);
    while (q--) {
        Point a, b, p;
        cin >> a.x >> a.y >> b.x >> b.y >> p.x >> p.y;
        if (a == b) cout << "DEGENERATE ";
        else cout << lineDistance(a, b, p) << ' ';
        cout << segmentDistance(a, b, p) << '\n';
    }
}
