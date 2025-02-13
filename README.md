# ipc-tracer

A simple script to parse, aggregate and filter data from [trace-ipc](https://developer.android.com/topic/performance/vitals/render#scheduling-delays).

First, use the `trace-ipc` tool from adb:

```bash
$ adb shell am trace-ipc start
… use the app - scroll/animate ...
$ adb shell am trace-ipc stop --dump-file /data/local/tmp/ipc-trace.txt
$ adb pull /data/local/tmp/ipc-trace.txt
```

Then you can use the tool as follows:

```bash
$ pip3 install click
$ python3 ipc-tracer.py --help

Usage: ipc-tracer.py [OPTIONS]

Options:
  --input-file PATH           Path to the input trace file.  [required]
  --output-file PATH          Path to the output file for filtered traces. [required]
  --filter TEXT               Glob pattern to filter stack frames, e.g. 'io.sentry.*' will ouput all IPC calls containing the Sentry frames. Use "*" to show all stackframes from all processes.
  --main-thread-only BOOLEAN  Filter IPC calls originating from the main thread.
  --help                      Show this message and exit.
```
