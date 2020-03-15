Cache Simulator
A generic cache simulator written in python. (INTEL i5 4TH GEN PROCESSOR -WINDOWS 10)

*Use the 3 python files: cache_sim.py, cache.py and trace_parse.py*

Running the simulator
usage: cache_sim.py <BLOCKSIZE> <SIZE> <ASSOC> <REPLACEMENT_POLICY> <WRITE_POLICY> <TRACE_FILE>

<BLOCKSIZE>          Block size in bytes. Positive Integer, Power of two
<SIZE>               Total CACHE size in bytes. Positive Integer
<ASSOC>              Associativity, 1 if direct mapped, N if fully associative
<REPLACEMENT_POLICY> 0 for LRU
<WRITE_POLICY>       1 
  
Example
$ python cache_sim.py 32 16384 4 0 1 gcc_trace.txt.
16KB 4-way set-associative cache with 32B block size, LRU replacement policy, Write policy, and gcc_trace.txt as input file.
 
Interpreting the result
Simulator prints cache statistics, hit rate and miss rates.

          Simulator configuration
  L1_BLOCKSIZE:                    32
  L1_SIZE:                      16384
  L1_ASSOC:                         4
  L1_REPLACEMENT_POLICY:            0
  L1_WRITE_POLICY:                  1
  trace_file:               gcc_trace.txt
  ===================================

          Simulation results
  a. number of fetches            100000
  b. number of L1 reads:           63640
  c. number of L1 read misses:      1266
  d. number of L1 writes:          36360
  e. number of L1 write misses:    17563
  f. L1 miss rate:                0.1883
  g. L1 hit rate:                99.8117

            Simulation results (performance)
  1. average access time:          4.4322 ns
