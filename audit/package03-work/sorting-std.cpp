#include <bits/stdc++.h>
using namespace std;

struct P {
    int x, y;
    bool operator<(const P& p) const {
        if (x != p.x) return x < p.x;
        return y < p.y;
    }
};

bool comp(const string& a, const string& b) {
    if (a.size() != b.size()) return a.size() < b.size();
    return a < b;
}

int main() {
    vector<int> v = {4, 2, 5, 3, 5, 8, 3};
    sort(v.begin(), v.end());
    for (int x : v) cout << x << " ";
    cout << "\n";
    sort(v.rbegin(), v.rend());
    for (int x : v) cout << x << " ";
    cout << "\n";

    int a[] = {4, 2, 5, 3, 5, 8, 3};
    sort(a, a + 7);
    for (int x : a) cout << x << " ";
    cout << "\n";
    string s = "monkey";
    sort(s.begin(), s.end());
    cout << s << "\n";

    vector<pair<int, int>> p = {{1, 5}, {2, 3}, {1, 2}};
    sort(p.begin(), p.end());
    for (auto [x, y] : p) cout << x << "," << y << " ";
    cout << "\n";
    vector<tuple<int, int, int>> t = {{2, 1, 4}, {1, 5, 3}, {2, 1, 3}};
    sort(t.begin(), t.end());
    for (auto [x, y, z] : t) cout << x << "," << y << "," << z << " ";
    cout << "\n";
    vector<P> points = {{1, 5}, {2, 3}, {1, 2}};
    sort(points.begin(), points.end());
    for (auto p : points) cout << p.x << "," << p.y << " ";
    cout << "\n";

    vector<string> words = {"book", "a", "cat", "dog"};
    sort(words.begin(), words.end(), comp);
    for (const string& s : words) cout << s << " ";
    cout << "\n";
    vector<pair<int, int>> students = {{3, 80}, {1, 90}, {2, 80}};
    sort(students.begin(), students.end(), [](const auto& a, const auto& b) {
        if (a.second != b.second) return a.second > b.second;
        return a.first < b.first;
    });
    for (auto [id, score] : students) cout << id << "," << score << " ";
    cout << "\n";
    return 0;
}
