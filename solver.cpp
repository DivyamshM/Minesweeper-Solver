#include "game.h"

// -1 ---> flag
// -2 ---> unopened cell
void nbrcheck( vector<vector<int>> &a, int n, int m, int i, int j, vector<pii> &unopenedCells, vector<pii> &nbrFlags, vector<pii> &openedSafe )
{
    if ( i+1 < n && j+1 < m ) 
    {
        if ( a[i+1][j+1] == -1 ) nbrFlags.push_back({i+1,j+1});
        else if ( a[i+1][j+1] == -2 ) unopenedCells.push_back({i+1,j+1});
        else openedSafe.push_back({i+1,j+1});
    }
    if ( i+1 < n )
    {
        if ( a[i+1][j] == -1 ) nbrFlags.push_back({i+1,j});
        else if ( a[i+1][j] == -2 ) unopenedCells.push_back({i+1,j});
        else openedSafe.push_back({i+1,j});
    }
    if ( i+1 < n && j-1 >= 0 )
    {
        if ( a[i+1][j-1] == -1 ) nbrFlags.push_back({i+1,j-1});
        else if ( a[i+1][j-1] == -2 ) unopenedCells.push_back({i+1,j-1});
        else openedSafe.push_back({i+1,j-1});
    }
    if ( j-1 >= 0 )
    {
        if ( a[i][j-1] == -1 ) nbrFlags.push_back({i,j-1});
        else if ( a[i][j-1] == -2 ) unopenedCells.push_back({i,j-1});
        else openedSafe.push_back({i,j-1});
    }
    if ( i-1 >= 0 && j-1 >= 0 )
    {
        if ( a[i-1][j-1] == -1 ) nbrFlags.push_back({i-1,j-1});
        else if ( a[i-1][j-1] == -2 ) unopenedCells.push_back({i-1,j-1});
        else openedSafe.push_back({i-1,j-1});
    }
    if ( i-1 >= 0  )
    {
        if ( a[i-1][j] == -1 ) nbrFlags.push_back({i-1,j});
        else if ( a[i-1][j] == -2 ) unopenedCells.push_back({i-1,j});
        else openedSafe.push_back({i-1,j});
    }
    if ( i-1 >= 0 && j+1 < m )
    {
        if ( a[i-1][j+1] == -1 ) nbrFlags.push_back({i-1,j+1});
        else if ( a[i-1][j+1] == -2 ) unopenedCells.push_back({i-1,j+1});
        else openedSafe.push_back({i-1,j+1});
    }
    if ( j+1 < m ) 
    {
        if ( a[i][j+1] == -1 ) nbrFlags.push_back({i,j+1});
        else if ( a[i][j+1] == -2 ) unopenedCells.push_back({i,j+1});
        else openedSafe.push_back({i,j+1});
    }
    return;
}

vector<possibleMoves> solver( Board &myBoard, bool &flag, bool &isBoardStart )
{
    vector<possibleMoves> wrongans;
    possibleMoves wrongmv;
    wrongmv.flag = 0;
    wrongmv.cellrow = -1;
    wrongmv.cellcol = -1;
    wrongans[0] = wrongmv;
    if ( flag == false )
    {
        return wrongans;
    }
    if ( isBoardStart == true )
    {
        return wrongans;
    }

    vector<vector<int>> a = myBoard.grid;
    int n = myBoard.row;
    int m = myBoard.col;
    int totMines = myBoard.totMines;
    int curMines = myBoard.curMines;

    if ( n != a.size() && m != a[0].size() )
    {
        flag = false;
        return wrongans;
    }   
    if ( curMines > totMines )
    {
        flag = false;
        return wrongans;
    }
    
    // check if it is starting position or not
    bool start = true;
    for ( int i = 0; i < n; i++ )
    {
        for ( int j = 0; j < m; j++ )
        {
            if ( a[i][j] != -2 )
            {
                start = false;
            }
        }
    }

    if ( start == true )
    {
        isBoardStart = true;
        return wrongans;
    }
    else
    {
        // check that board is correct or not
        int cur = 0;
        for ( int i = 0; i < n; i++ )
        {
            for ( int j = 0; j < m; j++ )
            {
                if ( a[i][j] == -1 )
                {
                    cur++;
                }
                else if ( a[i][j] == -2 )
                {
                    continue;
                }
                else
                {
                    int num = a[i][j];
                    int nbr = 0;
                    if ( i+1 < n && j+1 < m && a[i+1][j+1] == -1 ) nbr++;
                    if ( i+1 < n && a[i+1][j] == -1 ) nbr++;
                    if ( i+1 < n && j-1 >= 0 && a[i+1][j-1] == -1 ) nbr++;
                    if ( j-1 >= 0 && a[i][j-1] == -1 ) nbr++;
                    if ( i-1 >= 0 && j-1 >= 0 && a[i-1][j-1] == -1 ) nbr++;
                    if ( i-1 >= 0 && a[i-1][j] == -1 ) nbr++;
                    if ( i-1 >= 0 && j+1 < m && a[i-1][j+1] == -1 ) nbr++;
                    if ( j+1 < m && a[i][j+1] == -1 ) nbr++;
                    if ( nbr != num )
                    {
                        flag = false;
                        return wrongans;
                    }
                }
            }
        }
        if ( cur != curMines )
        {
            flag = false;
            return wrongans;
        }

        // now board is correct, we have to solve now
        vector<possibleMoves> mv;
        bool BoardUpdate = false;
        for ( int i = 0; i < n; i++ )
        {
            for ( int j = 0; j < m; j++ )
            {
                if ( a[i][j] != -1 && a[i][j] != -2 )
                {
                    int num = a[i][j];
                    vector<pii> unopenedCells;
                    vector<pii> nbrFlags;
                    vector<pii> openedSafe;
                    nbrcheck(a,n,m,i,j,unopenedCells,nbrFlags,openedSafe);
                }
            }
        }
    }
}