#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    vector<int> l(n, -1), r(n, n), st;
    for (int i = 0; i < n; i++) {
        while (!st.empty() && a[st.back()] >= a[i]) st.pop_back();
        if (!st.empty()) l[i] = st.back();
        st.push_back(i);
    }
    st.clear();
    for (int i = n - 1; i >= 0; i--) {
        while (!st.empty() && a[st.back()] >= a[i]) st.pop_back();
        if (!st.empty()) r[i] = st.back();
        st.push_back(i);
    }
    ll ans = 0;
    for (int i = 0; i < n; i++) {
        ll width = r[i] - l[i] - 1;
        ans = max(ans, a[i] * width);
    }
    cout << ans << '\n';
}
