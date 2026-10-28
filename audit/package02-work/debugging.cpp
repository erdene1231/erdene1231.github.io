#include <bits/stdc++.h>
using namespace std;

long long count_brute(const vector<long long>& values) {
    int count = static_cast<int>(values.size());
    long long answer = 0;
    for (int left = 0; left < count; ++left) {
        long long sum = 0;
        for (int right = left; right < count; ++right) {
            sum += values[right];
            if (sum % count == 0) {
                ++answer;
            }
        }
    }
    return answer;
}

long long count_fast(const vector<long long>& values) {
    int count = static_cast<int>(values.size());
    if (count == 0) {
        return 0;
    }
    vector<long long> frequency(count, 0);
    frequency[0] = 1;
    long long prefix = 0;
    long long answer = 0;
    for (long long value : values) {
        prefix = (prefix + value % count + count) % count;
        answer += frequency[prefix];
        ++frequency[prefix];
    }
    return answer;
}

// Deliberately incorrect: missing the empty prefix, for the lesson's counterexample only.
long long count_buggy_demo(const vector<long long>& values) {
    int count = static_cast<int>(values.size());
    vector<long long> frequency(count, 0);
    long long prefix = 0;
    long long answer = 0;
    for (long long value : values) {
        prefix = (prefix + value % count + count) % count;
        answer += frequency[prefix];
        ++frequency[prefix];
    }
    return answer;
}

bool check_case(const vector<long long>& values) {
    long long expected = count_brute(values);
    long long actual = count_fast(values);
    if (expected == actual) {
        return true;
    }
    cerr << values.size() << '\n';
    for (long long value : values) {
        cerr << value << ' ';
    }
    cerr << '\n' << expected << ' ' << actual << '\n';
    return false;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int random_cases;
    cin >> random_cases;
    vector<long long> counterexample = {0};
    cout << "COUNTEREXAMPLE\n1\n0\n";
    cout << count_brute(counterexample) << ' ' << count_buggy_demo(counterexample) << '\n';
    int checked = 0;
    int possibilities = 1;
    for (int count = 1; count <= 6; ++count) {
        possibilities *= 5;
        for (int mask = 0; mask < possibilities; ++mask) {
            int remaining = mask;
            vector<long long> values(count);
            for (long long& value : values) {
                value = remaining % 5 - 2;
                remaining /= 5;
            }
            if (!check_case(values)) {
                return 1;
            }
            ++checked;
        }
    }
    mt19937 random(2026);
    for (int test = 0; test < random_cases; ++test) {
        int count = 1 + static_cast<int>(random() % 30);
        vector<long long> values(count);
        for (long long& value : values) {
            value = static_cast<int>(random() % 21) - 10;
        }
        if (!check_case(values)) {
            return 1;
        }
        ++checked;
    }
    cout << "OK " << checked << '\n';
}
