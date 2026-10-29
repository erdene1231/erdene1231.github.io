#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    set<int> seen;
    map<int, int> freq;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        seen.insert(x);
        freq[x]++;
    }
    while (q--) {
        int x;
        cin >> x;
        auto it = freq.find(x);
        cout << (it == freq.end() ? 0 : it->second) << "\n";
    }
    cout << seen.size() << "\n";
    for (int x : seen) cout << x << " " << freq.at(x) << "\n";
    return 0;
}
