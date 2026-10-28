#include <bits/stdc++.h>
using namespace std;

constexpr long long MOD = 1000000007;

long long power_mod(long long base, long long exponent) {
    long long result = 1;
    while (exponent > 0) {
        if (exponent & 1) {
            result = result * base % MOD;
        }
        base = base * base % MOD;
        exponent >>= 1;
    }
    return result;
}

struct Combinations {
    vector<long long> factorial;
    vector<long long> inverse_factorial;

    explicit Combinations(int maximum) : factorial(maximum + 1, 1), inverse_factorial(maximum + 1, 1) {
        for (int value = 1; value <= maximum; ++value) {
            factorial[value] = factorial[value - 1] * value % MOD;
        }
        inverse_factorial[maximum] = power_mod(factorial[maximum], MOD - 2);
        for (int value = maximum; value >= 1; --value) {
            inverse_factorial[value - 1] = inverse_factorial[value] * value % MOD;
        }
    }

    long long choose(int count, int selected) const {
        if (selected < 0 || selected > count) {
            return 0;
        }
        return factorial[count] * inverse_factorial[selected] % MOD * inverse_factorial[count - selected] % MOD;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int maximum, query_count;
    cin >> maximum >> query_count;
    Combinations combinations(maximum);
    for (int query = 0; query < query_count; ++query) {
        int count, selected;
        cin >> count >> selected;
        cout << combinations.choose(count, selected) << '\n';
    }
}
