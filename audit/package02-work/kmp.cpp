#include <bits/stdc++.h>
using namespace std;

vector<int> prefix_function(const string& pattern) {
    int count = static_cast<int>(pattern.size());
    vector<int> border(count);
    for (int index = 1; index < count; ++index) {
        int length = border[index - 1];
        while (length > 0 && pattern[index] != pattern[length]) {
            length = border[length - 1];
        }
        if (pattern[index] == pattern[length]) {
            ++length;
        }
        border[index] = length;
    }
    return border;
}

vector<int> find_occurrences(const string& text, const string& pattern) {
    vector<int> border = prefix_function(pattern), positions;
    int matched = 0;
    for (int index = 0; index < static_cast<int>(text.size()); ++index) {
        while (matched > 0 && text[index] != pattern[matched]) {
            matched = border[matched - 1];
        }
        if (text[index] == pattern[matched]) {
            ++matched;
        }
        if (matched == static_cast<int>(pattern.size())) {
            positions.push_back(index - matched + 2);
            matched = border[matched - 1];
        }
    }
    return positions;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string pattern, text;
    cin >> text >> pattern;
    vector<int> positions = find_occurrences(text, pattern);
    cout << positions.size() << '\n';
    for (int index = 0; index < static_cast<int>(positions.size()); ++index) {
        cout << positions[index] << (index + 1 == static_cast<int>(positions.size()) ? '\n' : ' ');
    }
    if (positions.empty()) {
        cout << '\n';
    }
}
