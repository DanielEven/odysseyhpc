# perf - Performance Analysis Tool

Perf, also known as `perf_events`, is a powerful performance counter for Linux systems that gathers data about hardware events such as instructions executed, branches mispredicted or cache-misses suffered.

It also provides very low overhead profiling of applications to trace dynamic control flow and identify hotspots, per task, per CPU and per-workload counters, sampling and source code event annotation, dynamic creation of tracepoints using the kprobes and uprobes frameworks, for kernel and userspace dynamic tracing respectively.

## Using perf

The basic synopsis of the perf command is;
```bash
perf [--version] [--help] [OPTIONS] COMMAND [ARGS]
```

To obtain a comprehensive list of sub-commands that can be used with `perf` command, pass the --help option to `perf`. To obtain help about a specific sub-command, just execute;
```bash
perf help SUB-COMMAND
```

Common sub-commands include:

* `stat`: runs a command and gathers performance counter statistics from it.
* `top`: generates and displays a performance counter profile in real time.
* `record`: runs a command and gathers a performance counter profile from it. The gathered data is saved into `perf.data` without displaying anything.
* `report`: It reads `perf.data` to display the performance counter profile information recorded via perf record sub-command.
* `list`: displays the symbolic event types which can be selected in the various perf commands with the -e option.


## Examples

Let us go over a few example usage of the perf command;

Stating `ls`:
```bash
$ perf stat ls -ld /etc/
drwxr-xr-x 87 root root 4096 Feb 21 18:10 /etc/

 Performance counter stats for 'ls -ld /etc/':

          2.485653      task-clock (msec)         #    0.649 CPUs utilized          
                 2      context-switches          #    0.805 K/sec                  
                 0      cpu-migrations            #    0.000 K/sec                  
               127      page-faults               #    0.051 M/sec                  
   <not supported>      cycles                                                      
   <not supported>      instructions                                                
   <not supported>      branches                                                    
   <not supported>      branch-misses                                               

       0.003827501 seconds time elapsed
```

To run a command and record its profile into perf.data, use the record sub-command. The basic syntax of using record command is stated on `man perf-record`.

```bash
perf record [-e <EVENT> | --event=EVENT] [-a] <command>
```

For example:
```bash
$ perf record -e cpu-clock -a -g -- sleep 3
[ perf record: Woken up 5 times to write data ]
[ perf record: Captured and wrote 1.329 MB perf.data (8755 samples) ]
```

To read the performance record, use the report sub-command. The command syntax is:

```bash
perf report [-i <file> | --input=file]
```

In our example, we should run:
```bash
$ perf report -i perf.data
Samples: 8K of event 'cpu-clock', Event count (approx.): 2188750000                                                                                            
  Children      Self  Command       Shared Object       Symbol                                                                                                 
+   99.94%     0.00%  swapper       [kernel.kallsyms]   [k] secondary_startup_64
+   99.94%     0.00%  swapper       [kernel.kallsyms]   [k] x86_64_start_kernel
+   99.94%     0.00%  swapper       [kernel.kallsyms]   [k] x86_64_start_reservations
+   99.94%     0.00%  swapper       [kernel.kallsyms]   [k] start_kernel
+   99.94%     0.00%  swapper       [kernel.kallsyms]   [k] rest_init
+   99.94%     0.00%  swapper       [kernel.kallsyms]   [k] cpu_startup_entry
+   99.94%     0.00%  swapper       [kernel.kallsyms]   [k] do_idle
+   99.93%    99.93%  swapper       [kernel.kallsyms]   [k] mwait_idle
+   99.93%     0.00%  swapper       [kernel.kallsyms]   [k] default_idle_call
+   99.93%     0.00%  swapper       [kernel.kallsyms]   [k] arch_cpu_idle
     0.03%     0.00%  kworker/0:1   [kernel.kallsyms]   [k] ret_from_fork
     0.03%     0.00%  kworker/0:1   [kernel.kallsyms]   [k] kthread
     0.03%     0.00%  kworker/0:1   [kernel.kallsyms]   [k] worker_thread
...
```

For more examples visit https://www.brendangregg.com/perf.html.

## FlameGraph

Flame graphs are a visualization of profiled software, allowing the most frequent code-paths to be identified quickly and accurately. They can be generated using [this open source repo](https://github.com/brendangregg/FlameGraph), which create interactive SVGs.

A common practice is to use FlameGraph to visualize data recorded with `perf record`.

For example:
```bash
# step 1: record stats for your program
perf record -F 99 -a -g -- sleep 60
perf script > out.perf
# step 2: fold stacks to single lines
./stackcollapse-perf.pl out.perf > out.folded
# step 3: render SVG
./flamegraph.pl out.perf-folded > perf-kernel.svg
```

See more options and output examples the [repo](https://github.com/brendangregg/FlameGraph).
