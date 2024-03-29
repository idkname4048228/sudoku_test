import copy
import time
import sys
sys.setrecursionlimit(100)

class sudoku:
    
    check_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    def __init__( self, sudoku_list ):
        self.can_solve = False  #數獨能不能解
        self.need_solve = True  #數獨需不需要解
        self.had_insert = False  #數獨是否有新增數字
        self.Dic = {}  #數獨每一個空格所能放的數字
        self.the_possible_place = -1  #數獨裡選擇最少的格子
        
        self.itself = sudoku_list  #數獨本身( 主要拿來更改 )
        #下面三個變數都是拿來判斷可放數自
        self.cloumn_list = [ [], [], [], [], [], [], [], [], [] ]#橫
        self.row_list = [ [], [], [], [], [], [], [], [], [] ]#直
        self.block_list = [ [], [], [], [], [], [], [], [], [] ]#宮, ( key//27 )*3 + ( key%9 )//3 ][ ( ( key//9 )%3 )*3 + ( key%9 )%3
        
        for i, cloumn in enumerate( self.itself ):  #初始時，把數獨本體更新到其他的變數
            for j in range( 9 ):
                self.cloumn_list[ i ].append( cloumn[ j ] )
                self.row_list[ j ].append( cloumn[ j ] )
                self.block_list[ ( i//3 )*3 + j//3 ].append( cloumn[ j ] )

    def dic_renew( self ):  #字典更新，每當有一個數字填入時，就更新一次
        self.Dic = {}
        
        for i in range( 9 ):
            for j in range( 9 ):
                if self.itself[ i ][ j ] == 0:
                    self.Dic[ i*9 + j ] = self.cloumn_list[ i ] + self.row_list[ j ] + self.block_list[ ( i//3 )*3 + j//3 ]
                    self.Dic[ i*9 + j ] = list( set( self.check_numbers ) - set( self.Dic[ i*9 + j ] ) )

    def sudo_renew( self ):  #數獨更新，每當有新的數字填入時，拿來判斷的變數要更新
        self.cloumn_list = [ [], [], [], [], [], [], [], [], [] ]#橫
        self.row_list = [ [], [], [], [], [], [], [], [], [] ]#直
        self.block_list = [ [], [], [], [], [], [], [], [], [] ]#宮
        for i, cloumn in enumerate( self.itself ):
            for j in range( 9 ):
                self.cloumn_list[ i ].append( cloumn[ j ] )
                self.row_list[ j ].append( cloumn[ j ] )
                self.block_list[ ( i//3 )*3 + j//3 ].append( cloumn[ j ] )


    def need_to_solve( self ):  #更改數獨需不需要解的方法，需要解回傳True，不需要則回傳False
        self.need_solve = True
        the_amount_of_zeroes = 0
        
        for i in range( 9 ):#數數字多少
            for j in range( 9 ):
                if self.itself[ i ][ j ] == 0:
                    the_amount_of_zeroes = the_amount_of_zeroes + 1
        
        if the_amount_of_zeroes == 0:
            self.need_solve = False
            
        return self.need_solve

    def can_be_solve( self ):  #看數獨能不能解，初始填的數字超過17個才有唯一解。如果填滿，就不需要解。如果初始數字有重複，不需要解
        self.can_solve = False
        more_num = False
        the_amount_of_numbers = 0
        
        for i in range( 9 ):#數數字多少
            for j in range( 9 ):
                if self.itself[ i ][ j ] != 0:
                    the_amount_of_numbers = the_amount_of_numbers + 1
                        
        while more_num == False:#數字重複?
            for i in range( 9 ):
                for j in range( 9 ):
                    if ( ( list( self.cloumn_list[ i ] ).count( self.check_numbers[ j ] ) > 1 )
                    or ( list( self.row_list[ i ] ).count( self.check_numbers[ j ] ) > 1 )
                    or ( list( self.block_list[ i ] ).count( self.check_numbers[ j ] ) > 1 ) ):
                        more_num = True
            break
        
        if the_amount_of_numbers >= 17 and the_amount_of_numbers < 81 and more_num == False:
            
            self.can_solve = True
            
        if self.can_solve:#可解就執行
            self.dic_renew()
            
        if self.the_min_of_dic() == 0:
            self.can_solve = False
        
        return self.can_solve

    def the_min_of_dic( self ):  #數獨字典裡最少的可放數字有幾個，會順便更改the_possible_place
        min_number = 9
        for key in self.Dic:
            if len( self.Dic[ key ] ) < min_number:
               min_number = len( self.Dic[ key ] )
               self.the_possible_place = key
        return min_number


    def simple_insert( self ):  #最簡單的填入，如果可放數列只有一個數字，填入
        for key in self.Dic.keys():
            if len( self.Dic[ key ] ) == 1:
                self.itself[ key//9 ][ key%9 ] = self.Dic[ key ][ 0 ]
                
        self.sudo_renew()
        self.dic_renew()

    def complex_insert( self ):  #較複雜的填入，判斷附近是否只有某一格可以填某個數字
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
            cloumn_test = list( set( self.Dic[ key ] ) - set( cloumn_test ) )
            row_test = list( set( self.Dic[ key ] ) - set( row_test ) )
            block_test = list( set( self.Dic[ key ] ) - set( block_test ) )
            
            if len( cloumn_test ) == 1:
                self.itself[ key//9 ][ key%9 ]  = cloumn_test[ 0 ]
                self.had_insert = True
            
            elif len( row_test ) == 1:
                self.itself[ key//9 ][ key%9 ]  = row_test[ 0 ]
                self.had_insert = True
            
            elif len( block_test ) == 1:
                self.itself[ key//9 ][ key%9 ]  = block_test[ 0 ]
                self.had_insert = True
        self.sudo_renew()
        self.dic_renew()


def print_sudo_which_is( my_sudo : sudoku ):  #把數獨print出來
    for i in my_sudo.itself:
        print( i )


def fix( my_sudo : sudoku ):  #重複簡單和複雜填入，直到複雜填入沒有再填新的數字，以及最短可放數列長度大於1
    while ( my_sudo.can_be_solve() ):
        my_sudo.simple_insert()
        my_sudo.complex_insert()
        
        if ( not( my_sudo.had_insert ) and my_sudo.the_min_of_dic() > 1):
            break 
    
    return my_sudo

def assume_number_from( my_sudo : sudoku ):  #假設the_possible_place的第一項是答案，填入，並開始解，如果不是，則下一個，全部都不是，回傳無解
    global answer_of_my_sudo
    
    my_sudo.sudo_renew()
    my_sudo.dic_renew()
    my_sudo.the_min_of_dic()
    place = my_sudo.the_possible_place
    
    for i in range( len( my_sudo.Dic[ place ] ) ):
        
        my_clone_sudo = copy.deepcopy( my_sudo )
        my_clone_sudo.itself[ place // 9][ place % 9 ] = my_sudo.Dic[ place ][ i ]
        
        my_clone_sudo.sudo_renew()
        my_clone_sudo.dic_renew()
        
        my_assume_sudo = copy.deepcopy( fix( my_clone_sudo ) )
        
        if my_assume_sudo.need_to_solve():
            
            if my_assume_sudo.can_be_solve():
                
                if assume_number_from( my_assume_sudo ):
                    return True
                
            else:
                if i == len( my_sudo.Dic[ place ] ):
                    return False
        else:
            answer_of_my_sudo = my_assume_sudo
            return True
    return False
     
def main():
    my_sudo = sudoku( [[8, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 3, 6, 0, 0, 0, 0, 0],
                       [0, 7, 0, 0, 9, 0, 2, 0, 0],
                       [0, 5, 0, 0, 0, 7, 0, 0, 0],
                       [0, 0, 0, 0, 4, 5, 7, 0, 0],
                       [0, 0, 0, 1, 0, 0, 0, 3, 0],
                       [0, 0, 1, 0, 0, 0, 0, 6, 8],
                       [0, 0, 8, 5, 0, 0, 0, 1, 0],
                       [0, 9, 0, 0, 0, 0, 4, 0, 0]
                       ])
    if my_sudo.need_to_solve():
        my_sudo = fix( my_sudo ) 
        
        if my_sudo.can_be_solve() :
            answer = assume_number_from( my_sudo )
            print( "answer:", answer )
            
            if answer:
                my_sudo = answer_of_my_sudo
                print( "my_sudo.can_be_solve()", my_sudo.can_be_solve() )
                print_sudo_which_is( my_sudo )
                
            else:
                print( "answer:", answer )
        else:
            print( my_sudo.can_be_solve() )
            print_sudo_which_is( my_sudo )
    else:
        print_sudo_which_is( my_sudo )
    
         
if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print( end - start )