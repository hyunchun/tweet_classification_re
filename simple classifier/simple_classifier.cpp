#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

int main() {
	vector<vector<string> > wordBank;
	wordBank.resize(6);

	// train
		fstream trainFile("sample_wordBank.txt");

		string line;
		int i = 0;
		while (getline(trainFile, line)) {
			stringstream input(line);
			string word;
			while (input >> word) {
				wordBank[i].push_back(word);
			}
			++i;
		}

		for (int k = 0; k < wordBank.size(); ++k) {
			for (int j = 0; j < wordBank[k].size(); ++j) {
				//cout << "k: " << k << " j: " << j << endl;
				cout << wordBank[k][j] << " ";
			}
			cout << endl;
		}

		trainFile.close();

	// test
		fstream testFile("samples.txt");	

		while (getline(testFile, line)) {
			vector<vector<int> > count;
			count.resize(6);

			for (int k = 0; k < wordBank.size(); ++k) {
				count[k].resize(wordBank[k].size());
			}

			stringstream input(line);
			string word;
			while (input >> word) {
				for (int k = 0; k < wordBank.size(); ++k) { 
					for (int j = 0; j < wordBank[k].size(); ++j) {
						if (word == wordBank[k][j])	{
							++count[k][j];
						}
					} // end j for
				} // end k for
			} // end while word
			
			int row_num = 0;
			int highest_sum = 0;
			for (int k = 0; k < count.size(); ++k) {
				int current_sum = 0;
				for (int j = 0; j < count[k].size(); ++j) {
					current_sum += count[k][j];
				}

				if (highest_sum < current_sum) {
					highest_sum = current_sum;
					row_num = k;	
				}
			}

			// cout output
			cout << wordBank[row_num][0] << endl;
		} // end while getline

	testFile.close();
}

