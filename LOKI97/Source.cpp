#include <iostream>
#include <vector>
using namespace std;
int main()
{
	string t;
	string s;
	cin >> t >> s;
	int n = t.size(), m = s.size();
	if (n < m) {
		cout << 0;
		return 0;
	}
	vector<vector<int>> v(26, vector<int>(n + 1, 0));
	for (int i = 0; i < n; i++) 
	{
		for (int j = 'a'; j <= 'z'; j++) 
		{
			if (t[i] == j)
			{
				v[j][i + 1] = 1;
			}
		}
	}
	for (int q = 0; q < 26; q++) 
	{
		for (int r; r < n+1; r++) {
			v[q][r] += v[q][r - 1];
		}
	}
	long long ans = 0;
	for (long long i = 0; i < m; i++) {
		ans = (i + 1) * (v[t[i] - 'a'][n - m-i-1 - 'a'][i]);
	}
	cout << ans;
}