#include <bits/stdc++.h>
using namespace std;

long long brute(const vector<long long>& a) {
    long long best = LLONG_MIN;
    for (int l = 0; l < (int)a.size(); l++) {
        long long sum = 0;
        for (int r = l; r < (int)a.size(); r++) {
            sum += a[r];
            best = max(best, sum);
        }
    }
    return best;
}

long long candidate(const vector<long long>& a) {
    long long best = LLONG_MIN;
    long long sum = 0;
    for (long long x : a) {
        sum = max(x, sum + x);
        best = max(best, sum);
    }
    return best;
}

int main() {
    mt19937 rng(1234567);
    vector<vector<long long>> tests = {{-5, -2}, {7}, {0, 0, 0}};
    for (int test = 0; test < 1000; test++) {
        int n = uniform_int_distribution<int>(1, 8)(rng);
        vector<long long> a(n);
        for (auto& x : a) {
            x = uniform_int_distribution<int>(-10, 10)(rng);
        }
        tests.push_back(a);
    }

    for (const auto& a : tests) {
        long long expected = brute(a);
        long long actual = candidate(a);
        if (expected != actual) {
            cout << "Mismatch\n";
            for (long long x : a) {
                cout << x << ' ';
            }
            cout << "\nExpected: " << expected << "\nActual: " << actual << '\n';
            return 0;
        }
    }
    cout << "All tests passed\n";
    return 0;
}
