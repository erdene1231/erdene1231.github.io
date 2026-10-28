#include <bits/stdc++.h>
using namespace std;

vector<pair<long long, int>> factorize(long long number) {
    vector<pair<long long, int>> factors;
    long long remaining = number;
    for (long long divisor = 2; divisor <= remaining / divisor; ++divisor) {
        int exponent = 0;
        while (remaining % divisor == 0) {
            remaining /= divisor;
            ++exponent;
        }
        if (exponent > 0) {
            factors.push_back({divisor, exponent});
        }
    }
    if (remaining > 1) {
        factors.push_back({remaining, 1});
    }
    return factors;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long number;
    cin >> number;
    vector<pair<long long, int>> factors = factorize(number);
    cout << factors.size() << '\n';
    long long divisor_count = 1;
    for (auto [prime, exponent] : factors) {
        cout << prime << ' ' << exponent << '\n';
        divisor_count *= exponent + 1;
    }
    cout << divisor_count << '\n';
}
