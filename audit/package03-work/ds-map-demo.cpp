#include <bits/stdc++.h>
using namespace std;

int main() {
    map<string, int> m;
    m["monkey"] = 4;
    m["banana"] = 3;
    m["harpsichord"] = 9;
    cout << m["banana"] << "\n";
    cout << m["aybabtu"] << "\n";
    cout << m.count("aybabtu") << "\n";
    auto it = m.find("missing");
    cout << (it == m.end() ? 0 : it->second) << "\n";
    cout << m.size() << "\n";
    for (const auto& [key, value] : m) {
        cout << key << " " << value << "\n";
    }
    return 0;
}
