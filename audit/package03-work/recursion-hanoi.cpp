#include <bits/stdc++.h>
using namespace std;

int moves(int n) {
    if (n == 0) return 0;
    return 2 * moves(n - 1) + 1;
}

void hanoi(int n, int from, int to, int aux) {
    if (n == 0) return;
    hanoi(n - 1, from, aux, to);
    cout << from << ' ' << to << '\n';
    hanoi(n - 1, aux, to, from);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    cout << moves(n) << '\n';
    hanoi(n, 1, 3, 2);
}
