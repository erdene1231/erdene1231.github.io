#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const int M1 = 1000000007, M2 = 1000000009, B = 911382323;
const int MOD = 1000000007;

struct Hash {
    vector<ll> h1, h2, p1, p2;

    Hash(const string &s) {
        int n = (int) s.size();
        h1.assign(n + 1, 0);
        h2.assign(n + 1, 0);
        p1.assign(n + 1, 1);
        p2.assign(n + 1, 1);
        for (int i = 0; i < n; i++) {
            int x = (unsigned char) s[i] + 1;
            h1[i + 1] = (h1[i] * B + x) % M1;
            h2[i + 1] = (h2[i] * B + x) % M2;
            p1[i + 1] = p1[i] * B % M1;
            p2[i + 1] = p2[i] * B % M2;
        }
    }

    ll get(int l, int r) const {
        ll x = (h1[r] - h1[l] * p1[r - l] % M1 + M1) % M1;
        ll y = (h2[r] - h2[l] * p2[r - l] % M2 + M2) % M2;
        return x * M2 + y;
    }
};
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string mode, s;
    getline(cin, mode);
    getline(cin, s);
    int d;
    cin >> d;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    unordered_map<int, unordered_map<ll, vector<string>>> dict;
    unordered_set<string> seen;
    while (d--) {
        string w;
        getline(cin, w);
        if (w.empty()) return 1;
        if (!seen.insert(w).second) continue;
        Hash h(w);
        dict[(int) w.size()][h.get(0, (int) w.size())].push_back(w);
    }
    vector<int> lengths;
    for (const auto &[len, words] : dict) lengths.push_back(len);
    sort(lengths.begin(), lengths.end());
    Hash h(s);
    int n = (int) s.size();
    vector<int> dp(n + 1);
    dp[0] = 1;
    for (int r = 1; r <= n; r++) {
        for (int len : lengths) {
            if (len > r) break;
            auto &words = dict[len];
            auto it = words.find(h.get(r - len, r));
            if (it == words.end()) continue;
            bool match = mode == "HASH";
            if (!match) {
                for (const string &w : it->second) {
                    if (s.compare(r - len, len, w) == 0) {
                        match = true;
                        break;
                    }
                }
            }
            if (match) dp[r] = (dp[r] + dp[r - len]) % MOD;
        }
    }
    cout << dp[n] << '\n';
}
