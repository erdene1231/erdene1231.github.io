#include <bits/stdc++.h>
using namespace std;

constexpr long long INF = numeric_limits<long long>::max() / 4;

void all_pairs_distances(vector<vector<long long>>& distance) {
    int count = static_cast<int>(distance.size());
    for (int middle = 0; middle < count; ++middle) {
        for (int from = 0; from < count; ++from) {
            if (distance[from][middle] == INF) {
                continue;
            }
            for (int to = 0; to < count; ++to) {
                if (distance[middle][to] == INF) {
                    continue;
                }
                distance[from][to] = min(distance[from][to],
                    distance[from][middle] + distance[middle][to]);
            }
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int vertex_count, edge_count, query_count;
    cin >> vertex_count >> edge_count >> query_count;
    vector<vector<long long>> distance(vertex_count,
                                      vector<long long>(vertex_count, INF));
    for (int vertex = 0; vertex < vertex_count; ++vertex) {
        distance[vertex][vertex] = 0;
    }
    for (int index = 0; index < edge_count; ++index) {
        int first, second;
        long long weight;
        cin >> first >> second >> weight;
        --first;
        --second;
        distance[first][second] = min(distance[first][second], weight);
        distance[second][first] = min(distance[second][first], weight);
    }
    all_pairs_distances(distance);
    for (int query = 0; query < query_count; ++query) {
        int from, to;
        cin >> from >> to;
        long long answer = distance[from - 1][to - 1];
        cout << (answer == INF ? -1 : answer) << '\n';
    }
}
