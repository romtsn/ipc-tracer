# ipc-tracer

A simple script to parse, aggregate and filter data from [trace-ipc](https://developer.android.com/topic/performance/vitals/render#scheduling-delays).


You can use it as follows:

```bash
λ pip3 install click
λ python3 ipc-trace-tool.py --help

Usage: ipc-trace-tool.py [OPTIONS]

Options:
  --input-file PATH           Path to the input trace file.  [required]
  --output-file PATH          Path to the output file for filtered traces. [required]
  --filter TEXT               Glob pattern to filter stack frames, e.g. 'io.sentry.*' will ouput all IPC calls containing the Sentry frames. Use "*" to show all stackframes from all processes 
  --main-thread-only BOOLEAN  Filter IPC calls originating from the main thread.
  --help                      Show this message and exit.
```
