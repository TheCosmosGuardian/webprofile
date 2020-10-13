import csv

class ServerOps:
    def possible(self,y, x, n, grid):
        for i in range(0, 9):
            if grid[y][i] == n:
                return False
        for i in range(0, 9):
            if grid[i][x] == n:
                return False
        x0 = (x // 3) * 3
        # print(f'X0 = {x0}')
        y0 = (y // 3) * 3
        # print(f'Y0 = {y0}')
        for i in range(0, 3):
            for j in range(0, 3):
                if grid[y0 + i][x0 + j] == n:
                    return False
        return True

    def solver(self,grid):
        for y in range(9):
            for x in range(9):
                if grid[y][x] == 0:
                    for n in range(1,10):
                        if self.possible(y,x,n,grid):
                            grid[y][x] = n
                            self.solver(grid)
                            if 0 not in grid[8]:
                                return grid
                            grid[y][x] = 0
                    return

    def validate_inputs(self,game):
        for y in range(9):
            for x in range(9):
                if game[y][x] != 0:
                    var = game[y][x]
                    game[y][x] = 0
                    if self.possible(y,x,var,game):
                        game[y][x] = var
                    else:
                        return 'Invalid'
        return 'Valid'

    def wrt_to_csv(self,data):
        with open('database.csv', newline='', mode='a') as database2:
            email = data['email']
            subject = data['subject']
            message = data['message']
            csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([email, subject, message])
