#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;

typedef pair<int,int> pii;
struct possibleMoves
{
    int cellrow,cellcol;
    int flag;
};

class Board
{
    public:
        int row;
        int col;
        int totMines;
        int curMines;

        vector<vector<int>> grid;

        // Constructor
        Board( int r, int c, int tot, int cur )
        {
            row = r;
            col = c;
            totMines = tot;
            curMines = cur;
            grid.resize(row,vector<int>(col,-2));
        }
};

int main()
{
    bool flag = true;
    bool strt = false;
    vector<Board> moves;
    while( flag == true )
    {
        // Read input of board state from python code

        // Solver function ---> solver(myBoard)

        // Terminate if game ends
    }
    return 0;
}