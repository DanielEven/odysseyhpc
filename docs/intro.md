# Introduction to parallel computing

The basic concept of parallel computing is simple to understand: we divide our job in tasks that can be executed at the same time, so that we finish the job in a fraction of the time that it would have taken if the tasks are executed one by one.
There are a lot of different ways of parallelizing things however - we need to cover these concepts before running our workflows in parallel.

Let's start with an analogy: suppose that we want to paint the four walls in a room. This is our problem.
We can divide our problem in 4 different tasks: paint each of the walls.
In principle, our 4 tasks are independent from each other in the sense that we don’t need to finish one to start another.
However, this does not mean that the tasks can be executed simultaneously or in parallel.
It all depends on the amount of resources that we have for the tasks.

## Terminology

### Concurrent vs. parallel execution

If there is only one painter, they could work for a while in one wall, then start painting another one, then work for a little bit in the third one, and so on.
**The tasks are being executed concurrently but not in parallel.**
Only one task is being performed at a time.
If we have 2 or more painters for the job, then the tasks can be performed in parallel.

In our analogy, the painters represent CPU cores in your computer.
The number of CPU cores available determines the maximum number of tasks that can be performed in parallel.
The number of concurrent tasks that can be started at the same time, however, is unlimited.

### Synchronous vs. asynchronous execution

Now imagine that all workers have to obtain their paint form a central dispenser located at the middle of the room.
If each worker is using a different color, then they can work asynchronously.
However, if they use the same color, and two of them run out of paint at the same time, then they have to synchronize to use the dispenser -  one should wait while the other is being serviced.

In our analogy, the paint dispenser represents access to the memory in your computer.
Depending on how a program is written, access to data in memory can be synchronous or asynchronous.

### Distributed vs. shared memory

Finally, imagine that we have 4 paint dispensers, one for each worker.
In this scenario, each worker can complete its task totally on their own.
They don’t even have to be in the same room, they could be painting walls of different rooms in the house, on different houses in the city, and different cities in the country.
In many cases, however, we need a communication system in place.
Suppose that worker A, needs a color that is only available in the dispenser of worker B - worker A should request the paint to worker B, and worker B should respond by sending the required color.

Think of the memory distributed on each node/computer of a cluster as the
different dispensers for your workers.
A *fine-grained* parallel program needs lots of communication/synchronization between tasks, in contrast with a *course-grained* one that barely communicates at all.
An embarrassingly/massively parallel problem is one where all tasks can be executed completely independent from each other (no communications required).

### Processes vs. threads

Our example painters have two arms, and could potentially paint with both arms at the same time.
Technically, the work being done by each arm is the work of a single painter.

In this example, each painter would be a process (an individual instance of a program).
The painters' arms represent a "thread" of a program.
Threads are separate points of execution within a single program, and can be executed either synchronously or asynchronously.

---

## How does parallelization work in practice?

These concepts translate into several different types of parallel computing, each good at certain types of tasks:

### Asynchronous programming

Often times, certain computations involve a lot of waiting.
Perhaps you sent some information to a webserver on the internet and are waiting back on a response.
In this case, if you needed to make lots of requests over the internet, your program would spend ages just waiting to hear back.
In this scenario, it would be very advantageous to fire off a bunch of requests to the internet, and then instead of waiting on each one, check back periodically to see if the request has completed before processing each request individually.

This is an example of asynchronous programming.
One thread executes many tasks at the same time, periodically checking on each one, and only taking an action once some external task has completed.
Asynchronous programming is very important when programming for the web, where lots of waiting around happens.
It's not very useful for scientific programming, because only one core/thread is typically doing any work - a normal program that doesn't run in parallel at all would be just as fast!

### Shared memory programming

Shared memory programming means using the resources on a single computer, and having multiple threads or processes work together on a single copy of a dataset in memory.
This is the most common form of parallel programming and is relatively easy to do.

### Distributed memory programming

Shared memory programming, although very useful, has one major limitation: we can only use the number of CPU cores present on a single computer.
If we want to increase speed any more, we need a better computer.
Big computers cost lots and lots of money.
Wouldn't it be more efficient to just use a lot of smaller, cheap computers instead?

This is the rationale behind distributed memory programming -  a task is farmed out to a large number of computers, each of which tackle an individual portion of a problem.
Results are communicated back and forth between compute nodes.

This is most advantageous when a dataset is too large to fit into a computer's memory (depending on the hardware you have access to this can be anything from several dozen gigabytes, to several terabytes).
Frameworks like [MPI](https://www.open-mpi.org/), [Hadoop](http://hadoop.apache.org/), and [Spark](https://spark.apache.org/) see widespread use for these types of problems.

### Serial farming

In many cases, we'll need to repeat the same computation multiple times.
Maybe we need to run the same set of steps on 10 different samples.
There doesn't need to be any communication at all, and each task is completely independent of the others.

In this scenario, why bother with all of these fancy parallel programming techniques, let's just start the same program 10 times on 10 different datasets on 10 different computers.
The work is still happening in parallel, and we didn't need to change anything about our program to achieve this.
As an extra benefit, this works the same for every program, regardless of what it does or what language it was written in.

This technique is known as serial farming.
