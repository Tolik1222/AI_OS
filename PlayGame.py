def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("---------")

def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    return None

def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    player = "X"
    for _ in range(9):
        print_board(board)
        try:
            move = input(f"Гравець {player}, введіть рядок та стовпчик (0-2) через пробіл: ").split()
            r, c = int(move[0]), int(move[1])
            if board[r][c] == " ":
                board[r][c] = player
                winner = check_winner(board)
                if winner:
                    print_board(board)
                    print(f"Вітаємо! Гравець {winner} переміг!")
                    return
                player = "O" if player == "X" else "X"
            else:
                print("Ця клітинка вже зайнята!")
        except (ValueError, IndexError):
            print("Некоректне введення. Спробуйте ще раз.")
    print_board(board)
    print("Нічия!")

if __name__ == '__main__':
    main()