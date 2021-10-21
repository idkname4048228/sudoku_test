class sudoku:
    
    check_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    def __init__( self, sudoku_list ):
        self.can_solve = False
        self.Dic = {}
        
        self.cloumn_list = sudoku_list#橫
        self.row_list = [ [], [], [], [], [], [], [], [], [] ]#直
        self.block_list = [ [], [], [], [], [], [], [], [], [] ]#宮
        
        for i, cloumn in enumerate( self.cloumn_list ):
            for j in range( 9 ):
                self.row_list[ j ].append( cloumn[ j ] )
                self.block_list[ ( i//3 )*3 + j//3 ].append( cloumn[ j ] )

    def can_be_solve( self ):
        more_num = False
        how_many_number = 0
        for i in range( 9 ):#數數字多少
            for j in range( 9 ):
                if self.cloumn_list[ i ][ j ] != 0:
                    how_many_number = how_many_number + 1
                else:#順便建字典
                    self.Dic[ i*9 + j ] = []
                        
        while more_num == False:#數字重複?
            for i in range( 9 ):
                for j in range( 9 ):
                    if ( ( list( self.cloumn_list[ i ] ).count( self.check_numbers[ j ] ) > 1 )
                    or ( list( self.row_list[ i ] ).count( self.check_numbers[ j ] ) > 1 )
                    or ( list( self.block_list[ i ] ).count( self.check_numbers[ j ] ) > 1 ) ):
                        more_num = True
            break

        if how_many_number >= 17 and more_num == False:
            self.can_solve = True
            
        if self.can_solve:#可解就執行
            for i in range( 9 ):
                for j in range( 9 ):
                    try:
                        if self.Dic[ i*9 + j ] == []:#先看有沒有創建，不然會自動創建
                            
                            self.Dic[ i*9 + j ] = self.cloumn_list[ i ] + self.row_list[ j ] + self.block_list[ ( i//3 )*3 + j//3 ]
                            self.Dic[ i*9 + j ] = list( set( self.check_numbers ) - set( self.Dic[ i*9 + j ] ) )
                    except:
                        continue
        return self.can_solve


def main():
    S = sudoku( [[1, 2, 0, 0, 0, 0, 0, 0, 0],
                 [8, 0, 0, 0, 0, 0, 5, 0, 0],
                 [0, 0, 6, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 8, 0, 5],
                 [4, 0, 0, 6, 0, 0, 0, 0, 0],
                 [0, 5, 0, 0, 0, 0, 0, 3, 0],
                 [0, 0, 7, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 7, 0, 0, 0, 0, 0],
                 [0, 8, 0, 0, 0, 9, 0, 0, 4]
                 ])

    S.can_be_solve()
    print( len(S.Dic.keys()) )

if __name__ == "__main__":
    main()