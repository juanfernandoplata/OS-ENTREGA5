from collections import deque
from random import randint

MM_P = 3
VM_P = 10

class PT:
    def __init__( self, pages, policy = "FIFO" ):
        self.table = [ [ 0, 0 ] for _ in range( pages ) ]
        self.policy = policy
        self.alloc_p = 0
        self.queries = 0
        self.hits = 0

    def get_low( self ):
        ans = None
        low = float( "inf" )
        for i in range( 0, len( self.table ) ):
            if( self.table[ i ][ 0 ] and self.table[ i ][ 1 ]  < low ):
                ans = i
                low = self.table[ i ][ 1 ]
        return ans

    def proc_ref( self, ref ):
        self.queries += 1
        if( self.table[ ref ][ 0 ] ):
            if( self.policy == "LRU" ):
                self.table[ ref ][ 1 ] = self.queries
            self.hits += 1
        else:
            if( self.alloc_p < MM_P ): self.alloc_p += 1
            else:
                i = self.get_low()
                self.table[ i ][ 0 ] = 0
            self.table[ ref ][ 0 ] = 1
            self.table[ ref ][ 1 ] = self.queries

    def proc_ref_str( self, ref_str ):
        for ref in ref_str:
            self.proc_ref( ref )
            #self.print()

    def print( self ):
        i = 0
        print( "| PAGE TABLE |" )
        for entry in self.table:
            print( "PAGE #:", i, "| VALID:", entry[ 0 ], "| TICKS:", entry[ 1 ] )
            i += 1
        print()

    def report( self ):
        print( "| REPORT ON {} POLICY |".format( self.policy ) )
        print( "  * QUERIES:", self.queries )
        print( "  * HITS:", self.hits, "({:.1f}%)".format( self.hits / self.queries * 100.0 ) )
        print( "  * MISSES:", self.queries - self.hits, "({:.1f}%)".format( ( self.queries - self.hits ) / self.queries * 100.0 ) )
        print()

def text_book_example():
    ref_str = [ 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1 ]
    print( "| REFERENCE STRING |" )
    print( ref_str )
    print()
    pt = PT( VM_P )
    pt.proc_ref_str( ref_str )
    pt.report()
    pt = PT( VM_P, "LRU" )
    pt.proc_ref_str( ref_str )
    pt.report()

def random_ref_str():
    ref_str = [ randint( 0,VM_P - 1 ) for _ in range( 10000 ) ]
    pt = PT( VM_P )
    pt.proc_ref_str( ref_str )
    pt.report()
    pt = PT( VM_P, "LRU" )
    pt.proc_ref_str( ref_str )
    pt.report()

def run_trail():
    fifo_avg = 0
    lru_avg = 0
    for _ in range( 1000 ):
        ref_str = [ randint( 0,VM_P - 1 ) for _ in range( 10000 ) ]
        fifo_pt = PT( VM_P )
        lru_pt = PT( VM_P, "LRU" )

        fifo_pt.proc_ref_str( ref_str )
        lru_pt.proc_ref_str( ref_str )
        fifo_avg += fifo_pt.hits / fifo_pt.queries * 100.0 * 1.0 / 1000.0
        lru_avg += lru_pt.hits / lru_pt.queries * 100.0 * 1.0 / 1000.0
    print( "FIFO AVERAGE HIT RATE:", "{:.3f}".format( fifo_avg ) )
    print( "LRU AVERGAE HIT RATE", "{:.3f}".format( lru_avg ) )

text_book_example()
random_ref_str()
run_trail()