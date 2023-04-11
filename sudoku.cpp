#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <stdlib.h>
#include <algorithm>
#include <iterator>

using namespace std;

std::vector<std::vector<int>> string_to_board(const std::string& board){
    std::vector<std::vector<int>> vector_board;
    int board_size = static_cast<int>(sqrt(board.size()));
    for (int i=0;i < board_size; i++){
        std::vector<int> row;
        for (int j=0;j< board_size; j++){
            char c = board[i*board_size + j];
            int x = c - 48;
            row.push_back(x);
        }
        vector_board.push_back(row);
    }
    return vector_board;
}

std::ostream& operator<<(std::ostream& oss, std::vector<int>& v){
    std::copy(v.begin(), v.end(), std::ostream_iterator<int>(oss, " "));
    return oss;
}

std::ostream& operator<<(std::ostream& oss, std::vector<std::vector<int>>& v){
    for(auto i: v){
        oss << i << std::endl;
    }
    
    return oss;
}

class SudokuSolver{

    private:
    std::vector<std::vector<int>> board;
    int size;
    int square_size;
    std::vector<std::pair<int, int>> empty_cells;
    std::vector<std::pair<int, int>> visited;
    std::pair<int, int> no_cell;
   
    std::pair<int, int> next_cell(){
        for(auto cell: this->empty_cells){
            if(std::find(this->visited.begin(), this->visited.end(), cell) == this->visited.end()){
                return cell;
            }
        }
        return no_cell;
    }

    friend std::ostream& operator<<(std::ostream& oss, const SudokuSolver& s);

    std::vector<std::vector<int>> square(int row, int col){
        int x = col * this->square_size;
        int y = row * this->square_size;
        std::vector<std::vector<int>> result_square;
        for(int i=y; i< (y+this->square_size); i++){
            std::vector<int> current_row;
            for(int j=x; j < (x+this->square_size); j++){
                current_row.push_back(this->board[i][j]);
            }
            result_square.push_back(current_row);
        }
        return result_square;
    }
    std::pair<int, int> center_of_square_containing(int row, int col){
        int center_row = static_cast<int>(row / this->square_size) * this->square_size + 1;
        int center_col = static_cast<int>(col / this->square_size) * this->square_size + 1;
        return std::make_pair(center_row, center_col);
    }

    bool feasible(int r, int c, int value){
        auto row = this->board[r];
        bool row_feasible = std::find(row.begin(), row.end(), value) == row.end();
        bool col_feasible = true;
        for(int i=0; i < this->size; i++){
            if(this->board[i][c] == value){
                col_feasible = false;
                break;
            }
        }

        int x = this->center_of_square_containing(r, c).first;
        int y = this->center_of_square_containing(r, c).second;
        bool square_feasible = true;
        for(int i=-1; i <= 1; i++){
            for(int j=-1; j<=1; j++){
                if(this->board[x+i][y+j] == value){
                    square_feasible = false;
                }
            }
        }

        return row_feasible && col_feasible && square_feasible;
    }

    bool backtracking_solve(){
        if (this->visited.size() == this->empty_cells.size()){
            //no cell left to visit
            return true;
        }

        auto next_cell = this->next_cell();
        while(next_cell != this->no_cell){
            int i = next_cell.first;
            int j = next_cell.second;
            for(int value = 1; value <= 9; value++){
                if(this->feasible(i, j, value)){
                    this->board[i][j] = value;
                    this->visited.push_back(std::make_pair(i,j));
                    if(this->backtracking_solve()){
                        return true;
                    }else{
                        this->board[i][j] = 0;
                        auto pos = std::find(this->visited.begin(), this->visited.end(), std::make_pair(i,j));
                        this->visited.erase(pos);
                    }
                }
            }
            return false;
        }
        return true;
    }

    public:
    SudokuSolver(const std::vector<std::vector<int>>& _board):board(_board),
    size(_board.size()),square_size(0),
    empty_cells(), visited(),no_cell()
    {
        this->square_size = static_cast<int>(sqrt(this->size));
        for(int i=0; i < this->size; i++){
            for(int j=0; j < this->size; j++){
                if(this->board[i][j] == 0){
                    empty_cells.push_back(std::make_pair(i, j));
                }
            }
        }
        no_cell = std::make_pair(0,0);
    }
    SudokuSolver(const SudokuSolver& other):board(other.board), size(other.size),
     square_size(other.square_size),empty_cells(other.empty_cells),
     visited(other.visited),no_cell(other.no_cell){

    }

    bool solve(){
        return this->backtracking_solve();
    }

    bool is_solution(){
        std::vector<int> must_match = {1,2,3,4,5,6,7,8,9};

        // check rows
        for(auto row: this->board){
            std::vector<int> sorted_row(row);
            std::sort(sorted_row.begin(), sorted_row.end());
            if (sorted_row != must_match){
                std::cout << "Row " << row << " no solution." << std::endl;
                return false;
            }
        }

        //check columns
        for(int col = 0 ; col < this->size; col++){
            std::vector<int> column;
            for(int row=0; row < this->size; row++){
                column.push_back(this->board[row][col]);
            }
            std::sort(column.begin(), column.end());
            if (column != must_match){
                std::cout << "Col "<<col <<", "<< column << " no solution." <<std::endl;
                return false;
            }
        }

        //check squares
        for(int r=0; r < this->square_size; r++){
            for (int c=0; c < this->square_size; c++){
                auto sqr = this->square(r, c);
                std::vector<int> flattened;
                for(auto v: sqr){
                    for(int i: v){
                        flattened.push_back(i);
                    }
                }
                std::sort(flattened.begin(), flattened.end());
                if(flattened != must_match){
                    std::cout << "Square "<<r<<","<<c<<" no solution" << std::endl;
                    return false;
                }
            }
        }

        return true;
    }  


};

    std::ostream& operator<<(std::ostream& oss, const SudokuSolver& s){
        auto b = s.board;
        oss << b;
        return oss;
    }

int main()
{

    std::string sudoku_1 = "400701003005000200060003040078600900000050000004002180010800020002000300800205004";
    std::string sudoku_2 = "759462813463518297128973645697184532584236971231795486345821769912647358876359124";
    auto sudoku_board_2 = string_to_board(sudoku_2);
    auto sudoku_board_1 = string_to_board(sudoku_1);
    std::cout << sudoku_board_1 << std::endl;
    SudokuSolver s(sudoku_board_2);
    SudokuSolver s_1(sudoku_board_1);
    s_1.solve();
    std::cout << s_1 << std::endl;
    std::cout << sudoku_board_2 << std::endl << "is solution:"<<(s.is_solution()?"YES":"NO") << std::endl;
}