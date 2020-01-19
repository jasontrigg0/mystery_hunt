board = [
    [None,"D","A","R","D","T","A"],
    ["Y","L","B","O","N","N"],
    [None,"M","A","M","S","H","A"],
    ["N","N","B","D","W","A"],
    [None,"I","N","G","A","R","B"]
]

def load_words():
    words = set()
    prefixes = set()
    with open("/usr/share/dict/words") as f_in:
        for w in f_in:
            words.add(w.lower().strip())
            for i in range(len(w)):
                prefixes.add(w[:i].lower())
    return words,prefixes

def to_xy(i,j):
    y = i
    x = j + 0.5 if i%2 == 1 else j
    return (x,y)

def to_ij(x,y):
    i = y
    j = x - 0.5 if y%2 == 1 else x
    return (int(i),int(j))

def next_ij_steps(i,j):
    # print("i,j")
    # print(i,j)
    x,y = to_xy(i,j)
    # print("x,y")
    # print(x,y)
    for dy,dx in [(0,1),(0,-1),(1,0.5),(1,-0.5),(-1,0.5),(-1,-0.5)]:
        i,j = to_ij(x+dx,y+dy)
        # print("next i,j")
        # print(i,j)
        if i < 0 or i >= len(board): continue
        if j < 0 or j >= len(board[i]): continue
        if board[i][j] is None: continue
        yield to_ij(x+dx,y+dy)

def solve_boggle(words, prefixes, path):
    letters = "".join(board[i][j] for i,j in path).lower()
    if letters in words:
        yield letters
    if letters in prefixes:
        i,j = path[-1]
        for next_i, next_j in next_ij_steps(i,j):
            # print('here')
            # print(next_i,next_j)
            if (next_i,next_j) in path:
                continue
            for sol in solve_boggle(words, prefixes, path[:] + [(next_i,next_j)]):
                yield sol

if __name__ == "__main__":
    words, prefixes = load_words()
    all_sol = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None: continue
            row_cnt = i
            col_cnt = j
            for sol in solve_boggle(words, prefixes, [(i,j)]):
                all_sol.append(sol)

    print(sorted(all_sol,key=lambda x: -1*len(x)))
