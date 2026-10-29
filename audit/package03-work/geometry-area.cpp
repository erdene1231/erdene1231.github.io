#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Point {
    ll x, y;
};
using i128 = __int128_t;

string decimal(i128 x) {
    if (x == 0) return "0";
    string s;
    while (x > 0) {
        s += char('0' + x % 10);
        x /= 10;
    }
    reverse(s.begin(), s.end());
    return s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<Point> a(n);
    for (Point &p : a) cin >> p.x >> p.y;
    i128 area2 = 0;
    ll boundary = 0;
    for (int i = 0; i < n; i++) {
        Point p = a[i], q = a[(i + 1) % n];
        area2 += (i128) p.x * q.y - (i128) q.x * p.y;
        boundary += gcd(abs(q.x - p.x), abs(q.y - p.y));
    }
    if (area2 < 0) area2 = -area2;
    if (n < 3 || area2 == 0) cout << "DEGENERATE\n";
    else {
        i128 interior = (area2 - boundary + 2) / 2;
        cout << decimal(area2) << ' ' << decimal(interior) << ' ' << boundary << '\n';
    }
}
