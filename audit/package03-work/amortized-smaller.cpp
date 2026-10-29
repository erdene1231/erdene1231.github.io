#include <bits/stdc++.h>
using namespace std;

vector<int> nearest_smaller(const vector<int>& a) {
    int n = a.size();
    vector<int> st, ans(n, -1);
    st.reserve(n);
    for (int i = 0; i < n; i++) {
        while (!st.empty() && a[st.back()] >= a[i]) st.pop_back();
        if (!st.empty()) ans[i] = st.back();
        st.push_back(i);
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<int> a(n);
    for (int& x : a) cin >> x;
    vector<int> ans = nearest_smaller(a);
    for (int i : ans) cout << i + 1 << ' ';
    cout << '\n';
    for (int i : ans) {
        if (i == -1) cout << "NONE ";
        else cout << a[i] << ' ';
    }
    cout << '\n';
}
