#include <bits/stdc++.h>
using namespace std;

void bubble_sort(vector<int>& a) {
    int n = a.size();
    for (int i = 0; i < n; i++) {
        for (int j = 0; j + 1 < n; j++) {
            if (a[j] > a[j + 1]) swap(a[j], a[j + 1]);
        }
    }
}

void merge_sort(vector<int>& a, vector<int>& tmp, int l, int r) {
    if (l >= r) return;
    int mid = l + (r - l) / 2;
    merge_sort(a, tmp, l, mid);
    merge_sort(a, tmp, mid + 1, r);

    int i = l, j = mid + 1, k = l;
    while (i <= mid && j <= r) {
        if (a[i] <= a[j]) tmp[k++] = a[i++];
        else tmp[k++] = a[j++];
    }
    while (i <= mid) tmp[k++] = a[i++];
    while (j <= r) tmp[k++] = a[j++];
    for (int pos = l; pos <= r; pos++) a[pos] = tmp[pos];
}

void count_sort(vector<int>& a, int c) {
    vector<int> cnt(c + 1);
    for (int x : a) cnt[x]++;
    int pos = 0;
    for (int x = 0; x <= c; x++) {
        for (int k = 0; k < cnt[x]; k++) a[pos++] = x;
    }
}

int distinct_count(const vector<int>& a) {
    int ans = 0;
    for (int i = 0; i < (int)a.size(); i++) {
        if (i == 0 || a[i] != a[i - 1]) ans++;
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> a(n), tmp(n);
    for (int& x : a) cin >> x;
    merge_sort(a, tmp, 0, n - 1);
    cout << distinct_count(a) << "\n";
    return 0;
}
