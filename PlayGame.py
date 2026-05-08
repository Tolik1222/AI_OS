import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board, scores):
    size = len(board)
    print(f"\n  Рахунок: X - {scores['X']} | O - {scores['O']}")
    print("    " + "   ".join(map(str, range(size))))
    print("  " + "+" + "---" * size + "--+")
    for i, row in enumerate(board):
        # Кольорове відображення: X - червоний, O - синій
        colored_row = []
        for cell in row:
            if cell == 'X': colored_row.append('\033[91mX\033[0m')
            elif cell == 'O': colored_row.append('\033[94mO\033[0m')
            else: colored_row.append(' ')
        print(f"{i} | {' | '.join(colored_row)} |")
        if i < size - 1:
            print("  | " + "---" * size + " |")
    print("  " + "+" + "---" * size + "--+")

def check_winner(board):
    size = len(board)
    for i in range(size):
        if all(board[i][j] == board[i][0] != " " for j in range(size)): return board[i][0]
        if all(board[j][i] == board[0][i] != " " for j in range(size)): return board[0][i]
    if all(board[i][i] == board[0][0] != " " for i in range(size)): return board[0][0]
    if all(board[i][size - 1 - i] == board[0][size - 1] != " " for i in range(size)): return board[0][size - 1]
    return None

def play_game(scores):
    size = 5
    board = [[" " for _ in range(size)] for _ in range(size)]
    player = "X"
    
    for turn in range(size * size):
        clear_screen()
        print_board(board, scores)
        try:
            move = input(f"\nГравець {player}, твій хід (рядок стовпчик): ").split()
            r, c = int(move[0]), int(move[1])
            
            if 0 <= r < size and 0 <= c < size and board[r][c] == " ":
                board[r][c] = player
                winner = check_winner(board)
                if winner:
                    clear_screen()
                    scores[winner] += 1
                    print_board(board, scores)
                    print(f"\n\033[92mВітаємо! Гравець {winner} переміг!\033[0m")
                    return
                player = "O" if player == "X" else "X"
            else:
                input("Помилка: клітинка зайнята або поза межами! Натисніть Enter...")
        except (ValueError, IndexError):
            input("Помилка: введіть два числа від 0 до 4! Натисніть Enter...")
    
    clear_screen()
    print_board(board, scores)
    print("\nНічия!")

def main():
    scores = {'X': 0, 'O': 0}
    while True:
        play_game(scores)
        again = input("\nБажаєте зіграти ще раз? (так/ні): ").lower()
        if again not in ['так', 'y', 'yes', 'д']:
            print("Дякуємо за гру!")
            break

if __name__ == '__main__':
    main()