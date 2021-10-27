class sudoku:
    
    check_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    def __init__( self, sudoku_list ):
        self.can_solve = False
        self.had_insert = False
        self.Dic = {}
        
        
        self.itself = sudoku_list
        self.cloumn_list = [ [], [], [], [], [], [], [], [], [] ]#橫
        self.row_list = [ [], [], [], [], [], [], [], [], [] ]#直
        self.block_list = [ [], [], [], [], [], [], [], [], [] ]#宮, ( key//27 )*3 + ( key%9 )//3 ][ ( ( key//9 )%3 )*3 + ( key%9 )%3
        
        for i, cloumn in enumerate( self.itself ):
            for j in range( 9 ):
                self.cloumn_list[ i ].append( cloumn[ j ] )
                self.row_list[ j ].append( cloumn[ j ] )
                self.block_list[ ( i//3 )*3 + j//3 ].append( cloumn[ j ] )

    def dic_renew( self ):
        self.Dic = {}
        
        for i in range( 9 ):
            for j in range( 9 ):
                if self.itself[ i ][ j ] == 0:
                    self.Dic[ i*9 + j ] = self.cloumn_list[ i ] + self.row_list[ j ] + self.block_list[ ( i//3 )*3 + j//3 ]
                    self.Dic[ i*9 + j ] = list( set( self.check_numbers ) - set( self.Dic[ i*9 + j ] ) )
                    
                    
    
    def sudo_renew( self ):
        self.cloumn_list = [ [], [], [], [], [], [], [], [], [] ]#橫
        self.row_list = [ [], [], [], [], [], [], [], [], [] ]#直
        self.block_list = [ [], [], [], [], [], [], [], [], [] ]#宮
        for i, cloumn in enumerate( self.itself ):
            for j in range( 9 ):
                self.cloumn_list[ i ].append( cloumn[ j ] )
                self.row_list[ j ].append( cloumn[ j ] )
                self.block_list[ ( i//3 )*3 + j//3 ].append( cloumn[ j ] )
    
    def can_be_solve( self ):
        more_num = False
        how_many_number = 0
        for i in range( 9 ):#數數字多少
            for j in range( 9 ):
                if self.itself[ i ][ j ] != 0:
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
        for key in self.Dic.keys():
            if len( self.Dic[ key ] ) == 1:
                self.itself[ key//9 ][ key%9 ] = self.Dic[ key ][ 0 ]
                
        self.sudo_renew()
        self.dic_renew()
        
        
    def complex_insert( self ):
        self.had_insert = False
        for key in self.Dic.keys():
            cloumn_test = []
            row_test = []
            block_test = []
            
            for i in range( 9 ):
                try:
                    if ( key//9 )*9 + i == key:
                        continue
                    else:
                        cloumn_test.extend( self.Dic[ key ] )
                        
                        row_test.extend( self.Dic[ key ] )
                        
                        block_test.extend( self.Dic[ key ] )
                        
                except:
                    continue
            cloumn_test = list( set( cloumn_test ) )
            row_test = list( set( row_test ) )
            block_test = list( set( block_test ) )
            
            if len( set( self.Dic[ key ] ) - set( cloumn_test ) ) == 1:
                self.itself[ key//9 ][ key%9 ]  = list( set( self.Dic[ key ] ) - set( cloumn_test ) )[ 0 ]
                
                self.had_insert = True
                self.sudo_renew()
                self.dic_renew()
                break
            
            elif len( set( self.Dic[ key ] ) - set( row_test ) ) == 1:
                self.itself[ key//9 ][ key%9 ]  = list( set( self.Dic[ key ] ) - set( row_test ) )[ 0 ]
                
                self.had_insert = True
                self.sudo_renew()
                self.dic_renew()
                
                break
            
            elif len( set( self.Dic[ key ] ) - set( block_test ) ) == 1:
                self.itself[ key//9 ][ key%9 ]  = list( set( self.Dic[ key ] ) - set( block_test ) )[ 0 ]
                
                self.had_insert = True
                self.sudo_renew()
                self.dic_renew()
                
            
def fix( my_sudo : sudoku ):
    while ( my_sudo.can_be_solve() ):
        
        my_sudo.simple_insert()
        my_sudo.complex_insert()
        
        if not( my_sudo.had_insert ):
            break
        
    return my_sudo

def main():
    S = sudoku( [[8, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 3, 6, 0, 0, 0, 0, 0],
                 [0, 7, 0, 0, 9, 0, 2, 0, 0],
                 [0, 5, 0, 0, 0, 7, 0, 0, 0],
                 [0, 0, 0, 0, 4, 5, 7, 0, 0],
                 [0, 0, 0, 1, 0, 0, 0, 3, 0],
                 [0, 0, 1, 0, 0, 0, 0, 6, 8],
                 [0, 0, 8, 5, 0, 0, 0, 1, 0],
                 [0, 9, 0, 0, 0, 0, 4, 0, 0]
                 ])

    S.can_be_solve()
    
    S = fix(S)
    
    print(S.can_be_solve())
    for i in range( 9 ):
        print( S.itself[ i ] )
        
    
        
    
main()