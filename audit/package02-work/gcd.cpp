#include <iostream>
using namespace std;
using Integer = unsigned long long;

Integer greatest_divisor(Integer first, Integer second) {
    while (second != 0) {
        Integer remainder = first % second;
        first = second;
        second = remainder;
    }
    return first;
}

Integer least_multiple(Integer first, Integer second) {
    if (first == 0 || second == 0) {
        return 0;
    }
    Integer divisor = greatest_divisor(first, second);
    return (first / divisor) * second;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int query_count;
    cin >> query_count;

    for (int query = 0; query < query_count; ++query) {
        Integer first, second;
        cin >> first >> second;
        cout << greatest_divisor(first, second) << ' '
             << least_multiple(first, second) << '\n';
    }
    return 0;
}
