#include <iostream>
using namespace std;
using Integer = unsigned long long;

Integer modular_power(Integer base, Integer exponent, Integer modulus) {
    base %= modulus;
    Integer result = Integer{1} % modulus;

    while (exponent != 0) {
        if (exponent % 2 == 1) {
            result = (result * base) % modulus;
        }
        base = (base * base) % modulus;
        exponent /= 2;
    }
    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int query_count;
    cin >> query_count;

    for (int query = 0; query < query_count; ++query) {
        Integer base, exponent, modulus;
        cin >> base >> exponent >> modulus;
        cout << modular_power(base, exponent, modulus) << '\n';
    }
    return 0;
}
