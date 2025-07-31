from math import inf as infinity
from random import choice
import platform
import time
from os import system

def get_game_settings():
    """ Nhập kích thước bảng và số lượng ô liên tiếp cần để thắng """
    while True:
        try:
            # Nhập kích thước bảng và điều kiện thắng
            size = int(input("Nhập kích thước bảng (ví dụ: 10 cho 10x10): "))
            win_condition = int(input(f"Nhập số ô liên tiếp cần để thắng (tối đa {size}): "))
            
            # Kiểm tra thông tin nhập vào
            if size < 3 or win_condition > size or win_condition < 3:
                print("Thông tin không hợp lệ! Hãy nhập lại.")
                continue
                
            return size, win_condition
        
        except ValueError:
            print("Vui lòng nhập số nguyên hợp lệ!")

# Lấy thông tin từ người chơi
BOARD_SIZE, WIN_CONDITION = get_game_settings()
HUMAN = -1
COMP = +1

# Cập nhật trạng thái ban đầu theo bảng dynamic
def get_initial_board(size):
    """
    Nhập trạng thái ban đầu của bảng từ người dùng.
    Người dùng nhập `size * size` số (0: trống, 1: máy, -1: người) theo từng hàng.
    """
    print(f"Nhập trạng thái ban đầu của bảng ({size * size} số, cách nhau bởi dấu cách):")
    print("0: Ô trống, 1: Máy (O/X), -1: Người (X/O)")

    while True:
        try:
            # Nhập toàn bộ trạng thái bàn cờ
            values = list(map(int, input().split()))

            # Kiểm tra số lượng ô nhập vào có khớp với kích thước bảng không
            if len(values) != size * size or not all(v in [-1, 0, 1] for v in values):
                raise ValueError

            # Chuyển danh sách thành ma trận `size x size`
            return [values[i * size:(i + 1) * size] for i in range(size)]
        
        except ValueError:
            print(f"Dữ liệu không hợp lệ! Vui lòng nhập đúng {size * size} số (0, 1, -1) cách nhau bởi dấu cách.")

# Khai báo board game
board = get_initial_board(BOARD_SIZE)

def evaluate(state):
    """ Đánh giá trạng thái trò chơi """
    if wins(state, COMP):
        score = +1  # Máy thắng
    elif wins(state, HUMAN):
        score = -1  # Người thắng
    else:
        score = 0  # Hòa

    return score

# Cập nhật luật thắng cho bảng lớn
def wins(state, player):
    """ Kiểm tra người chơi có thắng không với điều kiện WIN_CONDITION """
    size = len(state)

    # Kiểm tra theo hàng ngang
    for row in state:
        for i in range(size - WIN_CONDITION + 1):
            if all(cell == player for cell in row[i:i + WIN_CONDITION]):
                return True

    # Kiểm tra theo cột dọc
    for col in range(size):
        for i in range(size - WIN_CONDITION + 1):
            if all(state[i + j][col] == player for j in range(WIN_CONDITION)):
                return True

    # Kiểm tra đường chéo chính \
    for i in range(size - WIN_CONDITION + 1):
        for j in range(size - WIN_CONDITION + 1):
            if all(state[i + k][j + k] == player for k in range(WIN_CONDITION)):
                return True

    # Kiểm tra đường chéo phụ /
    for i in range(size - WIN_CONDITION + 1):
        for j in range(WIN_CONDITION - 1, size):
            if all(state[i + k][j - k] == player for k in range(WIN_CONDITION)):
                return True

    return False

def game_over(state):
    """ Kiểm tra trò chơi đã kết thúc chưa """
    return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(state):
    """ Tìm các ô trống trên bàn cờ """
    cells = []
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    """ Kiểm tra nước đi hợp lệ """
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    """ Thực hiện nước đi của người chơi hoặc máy """
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False

# Tối ưu Minimax với tỉa nhánh Alpha-Beta
def minimax(state, depth, player, alpha, beta):
    """ Thuật toán Minimax tối ưu với tỉa nhánh Alpha-Beta """
    if depth == 0 or game_over(state):
        return [-1, -1, evaluate(state)]  # Trả về điểm đánh giá nếu đã đến độ sâu tối thiểu hoặc kết thúc trò chơi
    
    best = [-1, -1, -infinity] if player == COMP else [-1, -1, +infinity]

    for x, y in empty_cells(state):
        state[x][y] = player
        score = minimax(state, depth - 1, -player, alpha, beta)
        state[x][y] = 0
        score[0], score[1] = x, y  # Lưu lại vị trí nước đi

        if player == COMP:
            if score[2] > best[2]:
                best = score
            alpha = max(alpha, score[2])  # Cập nhật alpha
        else:
            if score[2] < best[2]:
                best = score
            beta = min(beta, score[2])  # Cập nhật beta

        if beta <= alpha:
            break  # Cắt nhánh nếu alpha >= beta

    return best


def clean():
    """ Clear console """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')

# Cập nhật console để hiển thị bảng lớn hơn
def render(state):
    """ Hiển thị bàn cờ với kích thước linh hoạt """
    size = len(state)
    print("\n" + "   " + " ".join([str(i) for i in range(size)]))

    for i, row in enumerate(state):
        row_str = f"{i}  " + " | ".join(["X" if cell == HUMAN else "O" if cell == COMP else " " for cell in row])
        print(row_str)
        print("  " + "-" * (size * 4 - 1))  # In dấu "-" để phân cách các hàng


def ai_turn():
    """ Lượt đi của máy """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print("Lượt của Máy!")
    render(board)

    # Nếu bàn cờ toàn trống, máy chọn ngẫu nhiên
    if depth == BOARD_SIZE * BOARD_SIZE:
        x, y = choice(range(BOARD_SIZE)), choice(range(BOARD_SIZE))
    else:
        move = minimax(board, depth, COMP, -infinity, infinity)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    time.sleep(1)


def human_turn():
    """ Lượt đi của người chơi """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print("Lượt của Bạn!")
    render(board)

    # Người chơi nhập tọa độ để đánh
    while True:
        try:
            x, y = map(int, input("Nhập tọa độ (dạng: dòng cột): ").split())
            if set_move(x, y, HUMAN):
                break
            else:
                print("Nước đi không hợp lệ, thử lại.")
        except ValueError:
            print("Vui lòng nhập số hợp lệ!")

def main():
    """ Chạy trò chơi """
    clean()

    # Nhập trạng thái ban đầu của bảng từ người dùng
    global board
    board = get_initial_board(BOARD_SIZE)

    # Xác định số lượt đi còn lại
    depth = len(empty_cells(board))

    # Kiểm tra nếu trò chơi đã kết thúc
    if game_over(board) or depth == 0:
        render(board)  # Hiển thị trạng thái bảng
        if wins(board, HUMAN):
            print("Trò chơi đã kết thúc: Người chơi THẮNG!")
        elif wins(board, COMP):
            print("Trò chơi đã kết thúc: Máy TÍNH THẮNG!")
        else:
            print("Trò chơi đã kết thúc: HÒA!")
        exit()
        
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if human is the first

    # Người chơi chọn X hoặc O
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Chọn lựa của máy
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Người chơi có thể bắt đầu trước
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Main loop của trò chơi
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn()
            first = ''

        human_turn()
        ai_turn()

    # Thông báo kết quả khi trò chơi kết thúc
    if wins(board, HUMAN):
        clean()
        print(f'Human turn [{h_choice}]')
        render(board)
        print('YOU WIN!')
    elif wins(board, COMP):
        clean()
        print(f'Computer turn [{c_choice}]')
        render(board)
        print('YOU LOSE!')
    else:
        clean()
        render(board)
        print('DRAW!')

    exit()


if __name__ == '__main__':
    main()
