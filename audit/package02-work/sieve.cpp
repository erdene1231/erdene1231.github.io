#include <iostream>
#include <vector>
using namespace std;

vector<int> build_smallest_factor(int limit) {
    vector<int> smallest(limit + 1, 0);
    for (int prime = 2; prime <= limit; ++prime) {
        if (smallest[prime] != 0) {
            continue;
        }
        smallest[prime] = prime;
        if (prime > limit / prime) {
            continue;
        }
        for (int multiple = prime * prime; multiple <= limit; multiple += prime) {
            if (smallest[multiple] == 0) {
                smallest[multiple] = prime;
            }
        }
    }
    return smallest;
}

int count_divisors(int value, const vector<int>& smallest) {
    int answer = 1;
    while (value > 1) {
        int prime = smallest[value];
        int exponent = 0;
        while (value % prime == 0) {
            value /= prime;
            ++exponent;
        }
        answer *= exponent + 1;
    }
    return answer;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int limit, query_count;
    cin >> limit >> query_count;
    vector<int> smallest = build_smallest_factor(limit);

    for (int query = 0; query < query_count; ++query) {
        int value;
        cin >> value;
        bool is_prime = value >= 2 && smallest[value] == value;
        cout << is_prime << ' ' << count_divisors(value, smallest) << '\n';
    }
    return 0;
}
