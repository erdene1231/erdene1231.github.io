#include <bits/stdc++.h>
using namespace std;
using ld = long double;
using P = complex<ld>;

bool close(ld a, ld b) {
    return abs(a - b) <= 1e-9L + 1e-12L * max(abs(a), abs(b));
}
ld heron(ld a, ld b, ld c) {
    ld s = (a + b + c) / 2;
    return sqrtl(max(0.0L, s * (s - a) * (s - b) * (s - c)));
}
int main() {
    cout << setprecision(6);
    P p = {4, 2};
    cout << p.real() << ' ' << p.imag() << '\n';
    P v = {3, 1}, u = {2, 2};
    P s = v + u;
    cout << s.real() << ' ' << s.imag() << '\n';
    P a = {4, 2}, b = {3, -1};
    cout << abs(b - a) << '\n';
    v = {4, 2};
    cout << arg(v) << '\n';
    v *= polar(1.0L, 0.5L);
    cout << arg(v) << '\n';
    P x = {4, 2}, y = {1, 2};
    cout << (conj(x) * y).imag() << '\n';
    cout << close(0.1L + 0.2L, 0.3L) << '\n';
    cout << heron(3, 4, 5) << '\n';
}
