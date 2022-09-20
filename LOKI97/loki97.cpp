//#include<vector>
//#include<iostream>
//#include<string>
//#include<bitset>
//
//typedef unsigned long long ULL;
//
//using namespace std;
//
//
//const ULL delta = 0x9E3779B97F4A7C15;
//
//ULL kp(ULL block, ULL key)
//{
//	ULL permutated_block = 0;
//	for (size_t i = 0; i < 32; i++)
//	{
//		if (key & (1ll << (31 - i)))
//		{
//			permutated_block += ((block & (1ll << (31 - i))) << 32);
//			permutated_block += ((block & (1ll << (63 - i))) >> 32);
//		}
//		else
//		{
//			permutated_block += (block & (1ll << (31 - i)));
//			permutated_block += (block & (1ll << (63 - i)));
//		}
//	}
//	return permutated_block;
//}
//
//
//bitset<96> E(ULL block)
//{
//	vector<pair<int, int>> sequence = { {4,0}, {63,56}, {58,48}, {52,40}, {42,32}, {34,24}, {28,16}, {18,8}, {12,0} };
//	bitset<96> b;
//	int j = 95;
//	for (size_t i = 0; i < sequence.size(); i++)
//	{
//		for (int k = sequence[i].first; k >= sequence[i].second; k--, j--)
//		{
//			b[j] = (1ll << k) & block;
//		}
//	}
//	return b;
//}
//
//
////returns 8 bits
//ULL S1(ULL x)
//{
//	ULL y = x ^ 8191; //(0x1FFF)
//	return ((y * y * y) % 10513) & 255; //(0x2911) (0xFF)
//}
//
//
//ULL S2(ULL x)
//{
//	ULL y = x ^ 2047; //(0x7FF)
//	return ((y * y * y) % 2727) & 255; //(0xAA7) (0xFF)
//}
//
//
//vector<int> createP()
//{
//	vector<int> p = {};
//	for (int i = 56; i != -1; i -= 8)
//	{
//		if (i < 0)
//		{
//			i += 65;
//		}
//		p.push_back(i % 64);
//	}
//	return p;
//}
//
//
//ULL P(ULL block)
//{
//	ULL result = 0;
//	vector<int> p = createP();
//	for (size_t i = 0; i < 64; i++)
//	{
//		if (block & (1ll << i))
//		{
//			result += 1ll << (63 - p[i]);
//		}
//	}
//	return result;
//}
//
//
//
//ULL f(ULL block, ULL key)
//{
//	block = kp(block, key);
//	key >>= 32;
//	bitset<96> b = E(block);
//	int j = 95;
//	block = 0;
//	for (size_t i = 0; i < 4; i++)
//	{
//		ULL block1 = 0;
//		ULL block2 = 0;
//		for (int k = 12; k >= 0; k--, j--)
//		{
//			block1 += ULL(b[j]) << k;
//		}
//		for (int k = 10; k >= 0; k--, j--)
//		{
//			block2 += ULL(b[j]) << k;
//		}
//		block1 = S1(block1);
//		block2 = S2(block2);
//		block += block1 << (55 - 16 * i);
//		block += block2 << (47 - 16 * i);
//	}
//	block = P(block);
//	ULL ans = 0;
//	ans += S2(((key & 0b11100000000000000000000000000000) >> 21) + (block >> 56)) << 56;
//	ans += S2(((key & 0b00011100000000000000000000000000) >> 18) + ((block >> 48) & 0xFF)) << 48;
//	ans += S1(((key & 0b00000011111000000000000000000000) >> 13) + ((block >> 40) & 0xFF)) << 40;
//	ans += S1(((key & 0b00000000000111110000000000000000) >> 8) + ((block >> 32) & 0xFF)) << 32;
//	ans += S2(((key & 0b00000000000000001110000000000000) >> 5) + ((block >> 24) & 0xFF)) << 24;
//	ans += S2(((key & 0b00000000000000000001110000000000) >> 2) + ((block >> 16) & 0xFF)) << 16;
//	ans += S1(((key & 0b00000000000000000000001111100000) << 3) + ((block >> 8) & 0xFF)) << 8;
//	ans += S1(((key & 0b00000000000000000000000000011111) << 8) + (block & 0xFF));
//	return ans;
//}
//
//ULL g(ULL a, ULL b, ULL c, ULL i)
//{
//	return f(a + b + delta * i, c);
//}
//
//vector<ULL> generator(string s) // 32 letters
//{
//	ULL a = 0, b = 0, c = 0, d = 0;
//	for (int i = 0; i < 8; i++)
//	{
//		a += ULL(s[i]) << ((7 - i) * 8);
//		b += ULL(s[i + 8]) << ((7 - i) * 8);
//		c += ULL(s[i + 16]) << ((7 - i) * 8);
//		d += ULL(s[i + 24]) << ((7 - i) * 8);
//	}
//	vector<ULL> keys;
//	for (int i = 0; i < 48; i++)
//	{
//		ULL key = a ^ g(c, b, d, i);
//		keys.push_back(key);
//		a = b;
//		b = c;
//		c = d;
//		d = key;
//	}
//	return keys;
//}
//
//vector<ULL> loki(string text, vector<ULL> keys)
//{
//	ULL block_a = 0;
//	ULL block_b = 0;
//	for (size_t i = 0; i < 8; i++)
//	{
//		block_a += ULL(text[i]) << ((7 - i) * 8);
//		block_b += ULL(text[i+8]) << ((7 - i) * 8);
//	}
//	for (size_t i = 0; i < 16; i++)
//	{
//		block_b += keys[i * 3];
//		block_a ^= f(block_b, keys[i * 3 + 1]);
//		block_b += keys[i * 3 + 2];
//
//		swap(block_a, block_b);
//	}
//	return vector<ULL> {block_a, block_b};
//}
//
//string decode(vector<ULL> vec, vector<ULL> keys)
//{
//	ULL block_a = vec[0];
//	ULL block_b = vec[1];
//	for (int i = 15; i >= 0; i--)
//	{
//		swap(block_a, block_b);
//
//
//		block_b -= keys[i * 3 + 2];
//		block_a ^= f(block_b, keys[i * 3 + 1]);
//		block_b -= keys[i * 3];
//	}
//	string text = "";
//	for (int i = 7; i >= 0; i--)
//	{
//		text += char((block_a >> (i * 8)) & 0xFF);
//	}
//	for (int i = 7; i >= 0; i--)
//	{
//		text += char((block_b >> (i * 8)) & 0xFF);
//	}
//	return text;
//}
//
//void print_binary(ULL x)
//{
//	for (int i = 63; i != 0; i--)
//	{
//		cout << ((x >> i) & 1);
//	}
//	cout << endl;
//}
//
//int main()
//{
//	string text = "You are my love!";
//	string key = "qweasdzxcvbnfghrtym,.jkluiozaqxs";
//	auto keys = generator(key);
//	auto res = loki(text, keys);
//	//cout << res[0] << " " << res[1] << endl;
//	print_binary(res[0]);
//	print_binary(res[1]);
//	cout << decode(res, keys) << endl;
//	return 0;
//}