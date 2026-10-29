#include <bits/stdc++.h>
using namespace std;
using ll = long long;

vector<int> prevSmaller(const vector<ll> &a, bool strict) {
    int n = a.size();
    vector<int> ans(n), st;
    for (int i = 0; i < n; i++) {
        while (!st.empty() && (strict ? a[st.back()] >= a[i] : a[st.back()] > a[i])) {
            st.pop_back();
        }
        if (!st.empty()) ans[i] = st.back() + 1;
        st.push_back(i);
    }
    return ans;
}

vector<int> nextGreater(const vector<ll> &a, bool strict) {
    int n = a.size();
    vector<int> ans(n), st;
    for (int i = n - 1; i >= 0; i--) {
        while (!st.empty() && (strict ? a[st.back()] <= a[i] : a[st.back()] < a[i])) {
            st.pop_back();
        }
        if (!st.empty()) ans[i] = st.back() + 1;
        st.push_back(i);
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    vector<vector<int>> ans = {
        prevSmaller(a, true), prevSmaller(a, false),
        nextGreater(a, true), nextGreater(a, false)
    };
    for (const auto &row : ans) {
        for (int i : row) cout << i << ' ';
        cout << '\n';
    }
}
