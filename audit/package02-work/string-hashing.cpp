#include <bits/stdc++.h>
using namespace std;

constexpr long long BASE = 31;
constexpr array<long long, 2> MODULI{1000000007, 1000000009};
struct Fingerprint {
    int length;
    array<long long, 2> hash;
};

class StringHash {
    array<vector<long long>, 2> prefix, power;
public:
    explicit StringHash(const string& text) {
        int count = static_cast<int>(text.size());
        for (int part = 0; part < 2; ++part) {
            prefix[part].resize(count + 1);
            power[part].assign(count + 1, 1);
            for (int index = 0; index < count; ++index) {
                int value = text[index] - 'a' + 1;
                prefix[part][index + 1] = (prefix[part][index] * BASE + value) % MODULI[part];
                power[part][index + 1] = power[part][index] * BASE % MODULI[part];
            }
        }
    }
    Fingerprint substring(int left, int right) const {
        Fingerprint result{right - left, {0, 0}};
        for (int part = 0; part < 2; ++part) {
            long long removed = prefix[part][left] * power[part][right - left] % MODULI[part];
            result.hash[part] = (prefix[part][right] - removed + MODULI[part]) % MODULI[part];
        }
        return result;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string text;
    int query_count;
    cin >> text >> query_count;
    StringHash hashes(text);
    for (int query = 0; query < query_count; ++query) {
        int left, right;
        cin >> left >> right;
        Fingerprint result = hashes.substring(left - 1, right);
        cout << result.length << ' ' << result.hash[0] << ' ' << result.hash[1] << '\n';
    }
}
