#include <bits/stdc++.h>
using namespace std;

int n;
vector<int> perm, chosen;
void print_perm() {
    cout << "(";
    for (int i = 0; i < n; i++) {
        if (i) cout << " ";
        cout << perm[i];
    }
    cout << ")\n";
}
void search() {
    if ((int)perm.size() == n) {
        print_perm();
        return;
    }
    for (int i = 0; i < n; i++) {
        if (chosen[i]) continue;
        chosen[i] = true;
        perm.push_back(i);
        search();
        perm.pop_back();
        chosen[i] = false;
    }
}
int main() {
    cin >> n; // 0 <= n <= 9; output itself grows as n!.
    chosen.assign(n, false);
    cout << "REC\n";
    search();
    perm.resize(n);
    iota(perm.begin(), perm.end(), 0);
    cout << "NEXT\n";
    do {
        print_perm();
    } while (next_permutation(perm.begin(), perm.end()));
    return 0;
}
