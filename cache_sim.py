import sys
from cache import Cache
from trace_parse import traceParse
############################
# main simulator for cache
############################


def main():
    if len(sys.argv) != 7:
        print("\n")
        print ('use: cache_sim.py <BLOCKSIZE> <SIZE> <ASSOC> <REPLACEMENT_POLICY> <WRITE_POLICY> <trace_file>')
        print ('Example: 16KB 4-way set-associative cache with 32B block size, LRU replacement policy, Write policy, and gcc_trace.txt as input file')
        print ('Command: $ python cache_sim.py 32 16384 4 0 1 gcc_trace.txt')
        print("\n")
        sys.exit(1)
    else:
        blockSize = int(sys.argv[1])
        cacheSize = int(sys.argv[2])
        associativity = int(sys.argv[3])
        replacementPolicy = int(sys.argv[4])
        writePolicy = int(sys.argv[5])
        fileName = sys.argv[6]

        def printContents(cache):
            print ("\n")
            print (('          Simulator configuration '))
            print ('{: <24}'.format('  L1_BLOCKSIZE:'), '{: >12}'.format(cache.config['blockSize']))
            print ('{: <24}'.format('  L1_SIZE:'), '{: >12}'.format(cache.config['cacheSize']))
            print ('{: <24}'.format('  L1_ASSOC:'), '{: >12}'.format(cache.config['associativity']))
            print ('{: <24}'.format('  L1_REPLACEMENT_POLICY:'), '{: >12}'.format(cache.config['replacementPolicy']))
            print ('{: <24}'.format('  L1_WRITE_POLICY:'), '{: >12}'.format(cache.config['writePolicy']))
            print ('{: <24}'.format('  trace_file:'), '{: >12}'.format(fileName))
            print ('{:=<37}'.format('  '))
            print ("")

            print (('          Simulation results '))
            totalMisses = cache.stats['ReadMisses'] + cache.stats['WriteMisses']
            totalAccesses = cache.stats['Reads'] + cache.stats['Writes']
            print ('{: <31}'.format('  a. number of fetches '), '{: >8}'.format('%d' %totalAccesses))
            print ('{: <31}'.format('  b. number of L1 reads:'), '{: >8}'.format(cache.stats['Reads']))
            print ('{: <31}'.format('  c. number of L1 read misses:'), '{: >8}'.format(cache.stats['ReadMisses']))
            print ('{: <31}'.format('  d. number of L1 writes:'), '{: >8}'.format(cache.stats['Writes']))
            print ('{: <31}'.format('  e. number of L1 write misses:'), '{: >8}'.format(cache.stats['WriteMisses']))
            missRate = totalMisses / (totalAccesses)
            print ('{: <31}'.format('  f. L1 miss rate:'), '{: >8}'.format('%.4f' % missRate))
            hitRate = 100-missRate
            print ('{: <31}'.format('  g. L1 hit rate:'), '{: >8}'.format('%.4f' % hitRate))
            print ("")
            print (('            Simulation results (performance) '))
            # L1 Cache Hit Time(in ns) = 0.25ns + 2.5ns * (L1_Cache Size / 512kB) + 0.025ns * (L1_BLOCKSIZE / 16B) + 0.025ns * L1_SET_ASSOCIATIVITY
            # L1 miss penalty(in ns) = 20 ns + 0.5 * (L1_BLOCKSIZE / 16 B / ns))
            # avg_access_time = (l1_hit_time + (l1_miss_rate * (miss_penalty))
            hitTime = 0.25 + (2.5 * (cache.config['cacheSize'] / (512 * 1024))) + \
                (0.025 * (cache.config['blockSize'] / 16)) + (0.025 * cache.config['associativity'])
            missPenalty = 20 + 0.5 * (cache.config['blockSize'] / 16)
            AAT = hitTime + (missRate * missPenalty)
            print ('{: <23}'.format('  1. average access time:'), '{: >18}'.format('%.4f ns' % AAT))

        # L1 cache instantiation & initialization
        L1 = Cache(blockSize, cacheSize, associativity, replacementPolicy, writePolicy)
        # parsing trace file
        instr_list = traceParse(fileName)
        for i in instr_list:
            if i[0] is 'r':
                L1.readFromAddress(i[1])
            elif i[0] is 'w':
                L1.writeToAddress(i[1])
        printContents(L1)


##################################################################
if __name__ == '__main__':
    main()

##################################################################
# python cache_sim.py 16 16384 1 0 0 gcc_trace.txt > out_run1.txt
# diff - iw out_run1.txt ValidationRun1.txt
# python cache_sim.py 128 2048 8 0 1 go_trace.txt > out_run2.txt
# diff - iw out_run2.txt ValidationRun2.txt
# python cache_sim.py 32 4096 4 0 1 perl_trace.txt > out_run3.txt
# diff - iw out_run3.txt ValidationRun3.txt
# python cache_sim.py 64 8192 2 1 0 gcc_trace.txt > out_run4.txt
# diff - iw out_run4.txt ValidationRun4.txt
# python cache_sim.py 32 1024 4 1 1 go_trace.txt > out_run5.txt
# diff - iw out_run5.txt ValidationRun5.txt
