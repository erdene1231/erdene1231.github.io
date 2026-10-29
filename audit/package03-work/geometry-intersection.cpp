#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Point {
    ll x, y;
    bool operator==(Point p) const {
        return x == p.x && y == p.y;
    }
    bool operator<(Point p) const {
        return tie(x, y) < tie(p.x, p.y);
    }
};

ll cross(Point a, Point b, Point p) {
    return (b.x - a.x) * (p.y - a.y) - (b.y - a.y) * (p.x - a.x);
}

bool onSegment(Point a, Point b, Point p) {
    return cross(a, b, p) == 0 &&
        min(a.x, b.x) <= p.x && p.x <= max(a.x, b.x) &&
        min(a.y, b.y) <= p.y && p.y <= max(a.y, b.y);
}
int sign(ll x) {
    return (x > 0) - (x < 0);
}

string intersect(Point a, Point b, Point c, Point d) {
    if (a == b) return onSegment(c, d, a) ? "POINT" : "NONE";
    if (c == d) return onSegment(a, b, c) ? "POINT" : "NONE";
    ll x = cross(a, b, c), y = cross(a, b, d);
    ll z = cross(c, d, a), w = cross(c, d, b);
    if (x == 0 && y == 0) {
        if (b < a) swap(a, b);
        if (d < c) swap(c, d);
        Point l = max(a, c), r = min(b, d);
        if (r < l) return "NONE";
        return l == r ? "POINT" : "OVERLAP";
    }
    if (onSegment(a, b, c) || onSegment(a, b, d) ||
        onSegment(c, d, a) || onSegment(c, d, b)) return "POINT";
    return sign(x) * sign(y) < 0 && sign(z) * sign(w) < 0 ? "POINT" : "NONE";
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        char type;
        Point a, b, p, d;
        cin >> type >> a.x >> a.y >> b.x >> b.y >> p.x >> p.y;
        if (type == 'O') {
            ll c = cross(a, b, p);
            cout << (a == b ? "DEGENERATE" : c > 0 ? "LEFT" : c < 0 ? "RIGHT" : "TOUCH") << '\n';
        } else {
            cin >> d.x >> d.y;
            cout << intersect(a, b, p, d) << '\n';
        }
    }
}
