class sudoku:
    
    check_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    def __init__( self, sudoku_list ):
        self.can_solve = False
        self.had_insert = False
        self.Dic = {}
        
        self.cloumn_list = sudoku_list#橫
        self.row_list = [ [], [], [], [], [], [], [], [], [] ]#直
        self.block_list = [ [], [], [], [], [], [], [], [], [] ]#宮
        
        for i, cloumn in enumerate( self.cloumn_list ):
            for j in range( 9 ):
                self.row_list[ j ].append( cloumn[ j ] )
                self.block_list[ ( i//3 )*3 + j//3 ].append( cloumn[ j ] )

    def dic_renew( self ):
        self.Dic = {}
        
        for i in range( 9 ):
            for j in range( 9 ):
                if self.cloumn_list[ i ][ j ] == 0:
                    self.Dic[ i*9 + j ] = self.cloumn_list[ i ] + self.row_list[ j ] + self.block_list[ ( i//3 )*3 + j//3 ]
                    
                    self.Dic[ i*9 + j ] = list( set( self.check_numbers ) - set( self.Dic[ i*9 + j ] ) )
    
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
    
    def simple_insert( self ):
        for i in self.Dic.keys():
            if len( self.Dic[ i ] ) == 1:
                self.cloumn_list[ i//9 ][ i%9 ] = self.Dic[ i ][ 0 ]
                
        self.dic_renew()
        
    def complex_insert( self ):
        self.had_insert = False
        for key in self.Dic.keys():
            cloumn_test = []
            row_test = []
            block_test = []
            
            for i in range( 9 ):
                try:
                    if key//9 + i == key:
                        continue
                    else:
                        cloumn_test.append( self.Dic[ key//9 ][ i ] )
                        cloumn_test = list( set( cloumn_test ) )
                        
                        row_test.append( self.Dic[ key%9 ][ i ] )
                        row_test = list( set( row_test ) )
                        
                        block_test.sppend( self.Dic[ ( key//27 )*3 + ( key%9 )//3 ][ i ] )
                        block_test = list( set( block_test ) )
                except:
                    continue
            if len( set( self.Dic[ key ] ) - set( cloumn_test ) ) == 1:
                self.cloumn_list[ key//9 ][ i ]  = list( set( self.Dic[ key ] ) - set( cloumn_test ) )[ 0 ]
                self.had_insert = True
                self.dic_renew()
                break
            
            elif len( set( self.Dic[ key ] ) - set( row_test ) ) == 1:
                self.row_list[ key%9 ][ i ] = list( set( self.Dic[ key ] ) - set( row_test ) )[ 0 ]
                self.had_insert = True
                self.dic_renew()
                break
            
            elif len( set( self.Dic[ key ] ) - set( block_test ) ) == 1:
                self.block_list[ ( key//27 )*3 + ( key%9 )//3 ][ i ]  = list( set( self.Dic[ key ] ) - set( block_test ) )[ 0 ]
                self.had_insert = True
                self.dic_renew()
            
def fix( my_sudo : sudoku ):
    while ( my_sudo.can_be_solve() ):
        
        my_sudo.simple_insert()
        my_sudo.complex_insert()
        
        if my_sudo.had_insert :
            
            break
    return my_sudo

def main():
    S = sudoku( [[5, 3, 0, 0, 7, 0, 0, 0, 0],
                 [6, 0, 0, 1, 9, 5, 0, 0, 0],
                 [0, 9, 8, 0, 0, 0, 0, 6, 0],
                 [8, 0, 0, 0, 6, 0, 0, 0, 3],
                 [4, 0, 0, 8, 0, 3, 0, 0, 1],
                 [7, 0, 0, 0, 2, 0, 0, 0, 6],
                 [0, 6, 0, 0, 0, 0, 2, 8, 0],
                 [0, 0, 0, 4, 1, 9, 0, 0, 5],
                 [0, 0, 0, 0, 8, 0, 0, 7, 9]
                 ])

    S.can_be_solve()
    S = fix(S)
    
    print(S.can_be_solve())
    for i in range( 9 ):
        print( S.cloumn_list[ i ] )
        
    


main()