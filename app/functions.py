def conversion(xs, ys):
    data = []
    if isinstance(xs, int):
        for y in ys:
            data.append(10*(y+1)+xs+1)
    elif isinstance(ys, int):
        for x in xs:
            data.append(10*(ys+1)+x+1)
    else:
        for i in range(len(xs)):
            data.append(10*(ys[i]+1)+(xs[i]+1))
    return tuple(sorted(data))

def pencilSum(x, y, sudokuBoard):
    sum = 0
    for c in range(9):
        sum += sudokuBoard[y][x][c] * (2**c)
    return sum

def optionsSum(number, shape, sudokuBoard, n):
    sum = 0
    if shape == "row": # y = number
        for x in range(9):
            sum += sudokuBoard[number][x][n] * (2**x)
    elif shape == "col": # x = number
        for y in range(9):
            sum += sudokuBoard[y][number][n] * (2**y)
    else:
        X = (number%3)*3
        Y = (number//3)*3
        for i in range(9):
            y = i // 3
            x = i % 3
            sum += sudokuBoard[Y+y][X+x][n] * (2**i)
    return sum

def numBits(n):
    count = 0
    while n > 0:
        count += (n&1)
        n >>= 1
    return count

def nPerRow(sudokuBoard, pencil, n, x = None, y = None): # but like, 2 = 2 and 3 = (3 or 2)
    if x == None: # given y, indicating a row
        index = 0
        for X in range(9):
            if sudokuBoard[y][X][pencil]:
                index = index*10 + (X+1)
        if index > 10 and index < 10**n:
            return index
    if y == None: # given x, indicating a column
        index = 0
        for Y in range(9):
            if sudokuBoard[Y][x][pencil]:
                index = index*10 + (Y+1)
        if index > 10 and index < 10**n:
            return index
    return -1

def toBinFormat(n):
    ans = 0
    for i in range(2):
        digit = n%10
        ans += 2**(digit-1)
        n //= 10
    return ans

def binToList(n):
    ans = []
    i = 0
    while n > 0:
        if n&1:
            ans.append(i)
        i += 1
        n >>= 1
    return ans

def test(sudoku):
    print("start")
    data = []
    for i in range(9):
        for j in range(9):
            if sudoku[i][j][0] == 1:
                data.append(10*(i+1)+j+1)
    return data

def obvious(sudokuBoard, check): # every option in a row is in the same square, or other way around
    # check a row
    for y in range(9):
        sum = 0
        for x in range(0, 7, 3):
            if sudokuBoard[y][x][check] or sudokuBoard[y][x+1][check] or sudokuBoard[y][x+2][check]:
                sum += 2**(x//3)
        if sum == 1 or sum == 2 or sum == 4:
            x = list(filter(lambda e: sudokuBoard[y][e][check], [e for e in range(9)]))
            return conversion(x, y)
    # check a column
    for x in range(9):
        sum = 0
        for y in range(0, 7, 3):
            if sudokuBoard[y][x][check] or sudokuBoard[y+1][x][check] or sudokuBoard[y+2][x][check]:
                sum += 2**(y//3)
        if sum == 1 or sum == 2 or sum == 4:
            y = list(filter(lambda e: sudokuBoard[e][x][check], [e for e in range(9)]))
            return conversion(x, y)
    # check a square
    for square in range( 9):
        X = square % 3
        Y = square // 3
        rowsum = 0
        for y in range(3*Y, 3*Y+3):
            if sudokuBoard[y][3*X][check] or sudokuBoard[y][3*X+1][check] or sudokuBoard[y][3*X+2][check]:
                rowsum += 2**(y-3*Y)
        if rowsum == 1 or rowsum == 2 or rowsum == 4:
            x = []
            y = []
            for xx in range(3*X, 3*X+3):
                for yy in range(3*Y, 3*Y+3):
                    if sudokuBoard[yy][xx][check]:
                        x.append(xx)
                        y.append(yy)
            return conversion(x, y)
        
        columnsum = 0
        for x in range(3*X, 3*X+3):
            if sudokuBoard[3*Y][x][check] or sudokuBoard[3*Y+1][x][check] or sudokuBoard[3*Y+2][x][check]:
                columnsum += 2**(x-3*X)
        if columnsum == 1 or rowsum == 2 or rowsum == 4:
            x = []
            y = []
            for xx in range(3*X, 3*X+3):
                for yy in range(3*Y, 3*Y+3):
                    if sudokuBoard[yy][xx][check]:
                        x.append(xx)
                        y.append(yy)
            return conversion(x, y)
    return []

def pairs(sudokuBoard): # but generalized to not just pairs
    # row
    for y in range(9):
        counter = {}
        for x in range(9):
            pencil = pencilSum(x,y, sudokuBoard)
            if pencil != 0 and pencil not in counter.keys():
                counter[pencil] = []
            if pencil != 0:
                counter[pencil].append(x)
        keys = counter.keys()
        for c in keys:
            subsetSum = 0
            x = []
            for cc in keys:
                if cc!= 0 and c&cc == cc: # subset
                    subsetSum += len(counter[cc])
                    x += counter[cc]
            if subsetSum == numBits(c):
                possibility = conversion(x,y)
                if possibility not in memory:
                    memory.add(possibility)
                    return possibility
        
        # 12 23 31 pattern
        for num in c3:
            x = []
            subsetSum = 0
            for subset in [num//10, 10*(num//100)+num%10, num%100]:
                s = toBinFormat(subset)
                if s in keys:
                    subsetSum += 1
                    x += counter[s]
            if subsetSum == 3:
                possibility = conversion(x,y)
                if possibility not in memory:
                    memory.add(possibility)
                    return possibility
        # same thing but for subsets of 4
        for num in c4: # already in that binary format
            x = []
            subsetSum = 0
            union = 0
            for cc in keys:
                if cc != 0 and num&cc == cc:
                    subsetSum += len(counter[cc])
                    x += counter[cc]
                    union |= cc
            if subsetSum == 4 and numBits(union) == 4:
                possibility = conversion(x,y)
                if possibility not in memory:
                    memory.add(possibility)
                    return possibility

    # column
    for x in range(9):
        counter = {}
        for y in range(9):
            pencil = pencilSum(x,y, sudokuBoard)
            if pencil != 0 and pencil not in counter.keys():
                counter[pencil] = []
            if pencil != 0:
                counter[pencil].append(y)
        keys = counter.keys()
        for c in keys:
            subsetSum = 0
            y = []
            for cc in keys:
                if cc!= 0 and c&cc == cc: # subset
                    subsetSum += len(counter[cc])
                    y += counter[cc]
            if subsetSum == numBits(c):
                possibility = conversion(x,y)
                if possibility not in memory:
                    memory.add(possibility)
                    return possibility
       
        # 12 23 31 pattern
        for num in c3:
            y = []
            subsetSum = 0
            for subset in [num//10, 10*(num//100)+num%10, num%100]:
                s = toBinFormat(subset)
                if s in keys:
                    subsetSum += 1
                    y += counter[s]
            if subsetSum == 3:
                possibility = conversion(x,y)
                if possibility not in memory:
                    memory.add(possibility)
                    return possibility
        
        # same thing but for subsets of 4
        for num in c4: # already in that binary format
            y = []
            subsetSum = 0
            union = 0
            for cc in keys:
                if cc != 0 and num&cc == cc:
                    subsetSum += len(counter[cc])
                    y += counter[cc]
                    union |= cc
            if subsetSum == 4 and numBits(union) == 4:
                possibility = conversion(x,y)
                if possibility not in memory:
                    memory.add(possibility)
                    return possibility
            
    # square
    for square in range(9):
        X = square % 3
        Y = square // 3
        counter = {}
        for x in range(3*X, 3*X+3):
            for y in range(3*Y, 3*Y+3):
                pencil = pencilSum(x,y, sudokuBoard)
                if pencil != 0 and pencil not in counter.keys():
                    counter[pencil] = []
                if pencil != 0:
                    counter[pencil].append(10*(y+1)+x+1)
        keys = counter.keys()
        for c in keys:
            data = []
            subsetSum = 0
            for cc in keys:
                if cc != 0 and c&cc == cc:
                    subsetSum += len(counter[cc])
                    data += counter[cc]
            if subsetSum == numBits(c):
                possibility = tuple(sorted(data))
                if possibility not in memory:
                    memory.add(possibility)
                    return possibility

        # 12 23 31 pattern
        for num in c3:
            data = []
            subsetSum = 0
            for subset in [num//10, 10*(num//100)+num%10, num%100]:
                s = toBinFormat(subset)
                if s in keys:
                    subsetSum += 1
                    data += counter[s]
            if subsetSum == 3:
                possibility = tuple(sorted(data))
                if possibility not in memory:
                    memory.add(possibility)
                    return possibility
        
        # same thing but for subsets of 4
        for num in c4: # already in that binary format
            data = []
            subsetSum = 0
            union = 0
            for cc in keys:
                if cc != 0 and num&cc == cc:
                    subsetSum += len(counter[cc])
                    data += counter[cc]
                    union |= cc
            if subsetSum == 4 and numBits(union) == 4:
                possibility = tuple(sorted(data))
                if possibility not in memory:
                    memory.add(possibility)
                    return possibility
    return []

def hiddenSubset(sudokuBoard): # there is a number than can go only in two places, there is another with same property
    # row
    for y in range(9):
        counter = {}
        for n in range(9):
            options = optionsSum(y, "row", sudokuBoard, n)
            if options != 0 and options not in counter.keys():
                counter[options] = []
            if options != 0:
                counter[options].append(n)
        keys = counter.keys()
        for c in keys:
            subsetSum = 0
            for cc in keys:
                if cc!= 0 and c&cc == cc: # subset
                    subsetSum += len(counter[cc])
            if subsetSum == numBits(c):
                ans = []
                xs = binToList(c)
                for x in xs:
                    ans.append(10*(y+1)+x+1)
                possibility = tuple(sorted(ans))
                if possibility not in memory:
                    memory.add(possibility)
                    return possibility
        
        # 12 23 31 pattern
        for num in c3:
            subsetSum = 0
            for subset in [num//10, 10*(num//100)+num%10, num%100]:
                s = toBinFormat(subset)
                if s in keys:
                    subsetSum += 1
            if subsetSum == 3:
                ans = []
                num = str(num)
                for x in num:
                    ans.append(10*(y+1)+int(x))
                possibility = tuple(sorted(ans))
                if possibility not in memory:
                    memory.add(possibility)
                    return possibility
        # same thing but for subsets of 4
        for num in c4: # already in that binary format
            subsetSum = 0
            union = 0
            for cc in keys:
                if cc != 0 and num&cc == cc:
                    subsetSum += len(counter[cc])
                    union |= cc
            if subsetSum == 4 and numBits(union) == 4:
                ans = []
                xs = binToList(num)
                for x in xs:
                    ans.append(10*(y+1)+x+1)
                possibility = tuple(sorted(ans))
                if possibility not in memory:
                    memory.add(possibility)
                    return possibility 
   
    # column
    for x in range(9):
        counter = {}
        for n in range(9):
            options = optionsSum(x, "col", sudokuBoard, n)
            if options != 0 and options not in counter.keys():
                counter[options] = []
            if options != 0:
                counter[options].append(n)
        keys = counter.keys()
        for c in keys:
            subsetSum = 0
            for cc in keys:
                if cc!= 0 and c&cc == cc: # subset
                    subsetSum += len(counter[cc])
            if subsetSum == numBits(c):
                ans = []
                ys = binToList(c)
                for y in ys:
                    ans.append(10*(y+1)+x+1)
                possibility = tuple(sorted(ans))
                if possibility not in memory:
                    memory.add(possibility)
                    return possibility
        
        # 12 23 31 pattern
        for num in c3:
            subsetSum = 0
            for subset in [num//10, 10*(num//100)+num%10, num%100]:
                s = toBinFormat(subset)
                if s in keys:
                    subsetSum += 1
            if subsetSum == 3:
                ans = []
                num = str(num)
                for y in num:
                    ans.append(10*int(y)+x+1)
                possibility = tuple(sorted(ans))
                if possibility not in memory:
                    memory.add(possibility)
                    return possibility
        # same thing but for subsets of 4
        for num in c4: # already in that binary format
            subsetSum = 0
            union = 0
            for cc in keys:
                if cc != 0 and num&cc == cc:
                    subsetSum += len(counter[cc])
                    union |= cc
            if subsetSum == 4 and numBits(union) == 4:
                ans = []
                ys = binToList(num)
                for y in ys:
                    ans.append(10*(y+1)+x+1)
                possibility = tuple(sorted(ans))
                if possibility not in memory:
                    memory.add(possibility)
                    return possibility

    # square
    for square in range(9):
        X = (square%3)*3
        Y = (square//3)*3
        counter = {}
        for n in range(9):
            options = optionsSum(square, "sq", sudokuBoard, n)
            if options != 0 and options not in counter.keys():
                counter[options] = []
            if options != 0:
                counter[options].append(n)
        keys = counter.keys()
        for c in keys:
            subsetSum = 0
            for cc in keys:
                if cc != 0 and c&cc == cc:
                    subsetSum += len(counter[cc])
            if subsetSum == numBits(c):
                ans = []
                sq = binToList(c)
                for s in sq:
                    ans.append(10*(Y+1+s//3) + (X+1+s%3))
                possibility = tuple(sorted(ans))
                if possibility not in memory:
                    memory.add(possibility)
                    return possibility

        # 12 23 31 pattern
        for num in c3:
            subsetSum = 0
            for subset in [num//10, 10*(num//100)+num%10, num%100]:
                s = toBinFormat(subset)
                if s in keys:
                    subsetSum += 1
            if subsetSum == 3:
                ans = []
                num = str(num)
                for s in num:
                    ans.append(10*(Y+1+(int(s)-1)//3) + (X+1+(int(s)-1)%3))
                possibility = tuple(sorted(ans))
                if possibility not in memory:
                    memory.add(possibility)
                    return possibility
        # same thing but for subsets of 4
        for num in c4: # already in that binary format
            subsetSum = 0
            union = 0
            for cc in keys:
                if cc != 0 and num&cc == cc:
                    subsetSum += len(counter[cc])
                    union |= cc
            if subsetSum == 4 and numBits(union) == 4:
                ans = []
                sq = binToList(num)
                for s in sq:
                    ans.append(10*(Y+1+s//3) + (X+1+(s%3)))
                possibility = tuple(sorted(ans))
                if possibility not in memory:
                    memory.add(possibility)
                    return possibility
    return []

def XWing(sudokuBoard, check):
    # row
    counter = {}
    for y in range(9):
        index = nPerRow(sudokuBoard, check, 2, y=y)-11
        if index != -12:
            if index in counter.keys():
                counter[index].append(y)
            else:
                counter[index] = [y]
    for c in counter.keys():
        if len(counter[c]) == 2:
            x = [c//10, c//10, c%10, c%10]
            y = counter[c]*2
            return conversion(x, y)
    
    # column
    counter = {}
    for x in range(9):
        index = nPerRow(sudokuBoard, check, 2, x)-11
        if index != -12:
            if index in counter.keys():
                counter[index].append(x)
            else:
                counter[index] = [x]
    for c in counter.keys():
        if len(counter[c]) == 2:
            y = [c//10, c//10, c%10, c%10]
            x = counter[c]*2
            return conversion(x, y)
    return []

def swordfish(sudokuBoard, check):
    # row
    counter = {}
    for y in range(9):
        index = nPerRow(sudokuBoard, check, 3, y=y)
        if index != -1:
            if index in counter.keys():
                counter[index].append(y)
            else:
                counter[index] = [y]
    keys = counter.keys()
    for c in keys:
        if c < 100: # want 3 digits
            continue
        x = []
        y = []
        rows = len(counter[c])
        for r in counter[c]:
            y.extend([r, r, r])
            x.extend([c//100-1, (c//10)%10-1, c%10-1])
        for subset in [c//10, c%100, 10*(c//100)+(c%10)]:
            if subset in keys:
                rows += len(counter[subset])
                if rows > 3:
                    break
                for r in counter[subset]:
                    y.extend([r, r])
                    x.extend([subset//10-1, subset%10-1])
        if rows == 3:
            return conversion(x, y)
    
    # 12 23 31 pattern
    for num in c3:
        subsets = [num//10, 10*(num//100)+num%10, num%100]
        x = []
        y = []
        found = True
        for s in subsets:
            if s in keys and len(counter[s])==1:
                y.extend(counter[s]*2)
                x.extend([s//10-1, s%10-1])
            else:
                found = False
                break
        if found:
            return conversion(x, y)
        
    # column
    counter = {}
    for x in range(9):
        index = nPerRow(sudokuBoard, check, 3, x=x)
        if index != -1:
            if index in counter.keys():
                counter[index].append(x)
            else:
                counter[index] = [x]
    keys = counter.keys()
    for c in keys:
        if c < 100: # want 3 digits
            continue
        x = []
        y = []
        rows = len(counter[c])
        for r in counter[c]:
            x.extend([r, r, r])
            y.extend([c//100-1, (c//10)%10-1, c%10-1])
        for subset in [c//10, c%100, 10*(c//100)+(c%10)]:
            if subset in keys:
                rows += len(counter[subset])
                if rows > 3:
                    break
                for r in counter[subset]:
                    x.extend([r, r])
                    y.extend([subset//10-1, subset%10-1])
        if rows == 3:
            return conversion(x, y)
    
    # 12 23 31 pattern
    for num in c3:
        subsets = [num//10, 10*(num//100)+num%10, num%100]
        x = []
        y = []
        found = True
        for s in subsets:
            if s in keys and len(counter[s])==1:
                x.extend(counter[s]*2)
                y.extend([s//10-1, s%10-1])
            else:
                found = False
                break
        if found:
            return conversion(x, y)
    return []  

def obviousUsable(sudokuBoard): # iterates over all 9 pencil values
    for check in range(9):
        res = obvious(sudokuBoard, check)
        if res and res not in memory: # not empty
            memory.add(res)
            return res
    return []

def XWingUsable(sudokuBoard):
    for check in range(9):
        res = XWing(sudokuBoard, check)
        if res and res not in memory: # not empty
            memory.add(res)
            return res
    return []

def swordfishUsable(sudokuBoard):
    for check in range(9):
        res = swordfish(sudokuBoard, check)
        if res and res not in memory: # not empty
            memory.add(res)
            return res
    return []

c3 = [None]*84 # short for 9 choose 3
index = 0
for i in range(9):
    for j in range(i+1, 9):
        for k in range(j+1, 9):
            c3[index] = 100*(i+1) + 10*(j+1) + (k+1)
            index += 1
c4 = [None]*126 # only need for generalized pairs, not for swordfish
index = 0
for i in range(9):
    for j in range(i+1, 9):
        for k in range(j+1, 9):
            for l in range(k+1, 9):
                c4[index] = 2**i + 2**j + 2**k + 2**l
                index += 1

memory = set()
def clearMemory():
    memory.clear()

functionsDict = {"Obvious":obviousUsable, 
                 "Subsets":pairs, 
                 "X-Wing":XWingUsable, 
                 "Swordfish":swordfishUsable,
                 "Hidden Subsets":hiddenSubset}