#include <bits/stdc++.h>
using namespace std;

string debruijn(int n, int k) {
    int nodes = 1;
    for (int i = 1; i < n; i++) nodes *= k;
    vector<int> next(nodes), vert = {0}, label = {-1};
    string ans;
    while (!vert.empty()) {
        int u = vert.back();
        if (next[u] < k) {
            int c = next[u]++;
            int v = (u * k + c) % nodes;
            vert.push_back(v);
            label.push_back(c);
        } else {
            int c = label.back();
            label.pop_back();
            vert.pop_back();
            if (c != -1) ans += char('0' + c);
        }
    }
    reverse(ans.begin(), ans.end());
    return string(n - 1, '0') + ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    cout << debruijn(n, k) << '\n';
}
