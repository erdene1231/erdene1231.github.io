#include <bits/stdc++.h>
using namespace std;

int common_brute(const vector<int>& a, const vector<int>& b) {
    int ans = 0;
    for (int j = 0; j < (int)b.size(); j++) {
        bool seen = false;
        for (int k = 0; k < j; k++) {
            if (b[k] == b[j]) seen = true;
        }
        if (seen) continue;
        for (int x : a) {
            if (x == b[j]) {
                ans++;
                break;
            }
        }
    }
    return ans;
}

int common_set(const vector<int>& a, const vector<int>& b) {
    set<int> s(a.begin(), a.end()), seen;
    int ans = 0;
    for (int x : b) {
        if (seen.insert(x).second && s.count(x)) ans++;
    }
    return ans;
}

int common_hash(const vector<int>& a, const vector<int>& b) {
    unordered_set<int> s(a.begin(), a.end()), seen;
    int ans = 0;
    for (int x : b) {
        if (seen.insert(x).second && s.count(x)) ans++;
    }
    return ans;
}

int common_sort(vector<int> a, vector<int> b) {
    sort(a.begin(), a.end());
    sort(b.begin(), b.end());
    int i = 0, j = 0, ans = 0;
    while (i < (int)a.size() && j < (int)b.size()) {
        int x = a[i], y = b[j];
        if (x == y) ans++;
        if (x <= y) while (i < (int)a.size() && a[i] == x) i++;
        if (y <= x) while (j < (int)b.size() && b[j] == y) j++;
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<int> a(n), b(m);
    for (int& x : a) cin >> x;
    for (int& x : b) cin >> x;
    cout << common_set(a, b) << " " << common_hash(a, b) << " "
         << common_sort(a, b) << "\n";
    return 0;
}
