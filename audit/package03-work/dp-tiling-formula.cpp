#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, m;
    if (!(cin >> n >> m)) return 0;
    if ((n * m) % 2) {
        cout << 0 << '\n';
        return 0;
    }
    const long double pi = acosl(-1.0L);
    long double ans = 1;
    for (int a = 1; a <= (n + 1) / 2; a++) {
        for (int b = 1; b <= (m + 1) / 2; b++) {
            long double x = cosl(pi * a / (n + 1));
            long double y = cosl(pi * b / (m + 1));
            ans *= 4 * (x * x + y * y);
        }
    }
    cout << setprecision(18) << ans << '\n';
}
