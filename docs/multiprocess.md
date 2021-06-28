# Parallelization in Python

Python does not thread very well.
Specifically, Python has a very nasty drawback known as a Global Interpreter
Lock (GIL).
The GIL ensures that only one compute thread can run at a time.
This makes multithreaded processing very difficult.
Instead, the best way to go about doing things is to use multiple independent processes to perform the computations.
This method skips the GIL, as each individual process has it's own GIL that does not block the others.
This is typically done using the `multiprocessing` module.

Before we start, we will need the number of CPU cores in our computer.
To get the number of cores in our computer, we can use the `psutil` module.
We are using `psutil` instead of `multiprocessing` because `psutil` counts cores instead of threads.
Long story short, cores are the actual computation units, threads allow additional multitasking using the cores you have.
For heavy compute jobs, you are generally interested in cores.

```python
import psutil
# logical=True counts threads, but we are interested in cores
psutil.cpu_count(logical=False)
# example output: 8
```

Using this number, we can create a pool of worker processes with which to parallelize our jobs:

```python
from multiprocessing import Pool
pool = Pool(psutil.cpu_count(logical=False))
```

The `pool` object gives us a set of parallel workers we can use to parallelize our calculations.
In particular, there is a map function (with identical syntax to the `map()` function used earlier), that runs a workflow in parallel.

Let's try `map()` out with a test function that just runs sleep.

```python
import time

def sleeping(arg):
    time.sleep(0.1)

%timeit list(map(sleeping, range(24)))
```

will output:
```
1 loop, best of 3: 2.4 s per loop
```

Now let's try it in parallel:

```python
from multiprocessing import Pool

with Pool(2) as pool:
    %timeit pool.map(sleeping, range(24))
```

will output:
```
1 loop, best of 3: 309 ms per loop
```

This is a general purpose parallelization recipe that you can use for your Python projects.
Parallel workers (with their own copy of everything) are created, data are sent to these workers, and then results are combined back together again.
