import re
import fnmatch
import click
from collections import defaultdict

def load_traces(file_path):
    """Load and parse traces from the file."""
    traces = []
    current_trace = None
    current_count = 0

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("Count: "):
                if current_trace is not None:
                    traces.append((current_count, current_trace))
                current_count = int(line.split(": ")[1])
                current_trace = []
            elif line.startswith("Trace: ") or current_trace is not None:
                if line != "Trace:" and line:
                    current_trace.append(line)

        if current_trace is not None:  # Add the last trace
            traces.append((current_count, current_trace))

    return traces

def filter_and_sort_traces(traces, pattern, main_thread_only):
    """Filter traces by stack frame pattern and sort by count."""
    filtered_traces = []

    for count, trace in traces:
        matches_pattern = False
        is_main_thread = False
        for frame in trace:
            clean_frame = frame.split("at ", 1)[-1]  # Remove "at " prefix if present
            if fnmatch.fnmatch(clean_frame, pattern):
                matches_pattern = True
            elif "android.app.ActivityThread.main" in frame:
                is_main_thread = True

        if matches_pattern and (not main_thread_only or is_main_thread):
            filtered_traces.append((count, trace))

    return sorted(filtered_traces, key=lambda x: x[0], reverse=True)

def write_traces_to_file(traces, output_file):
    """Write traces to an output file."""
    content = []
    counter = 0
    for count, trace in traces:
        content.append(f"Count: {count}\n")
        content.append("Trace:\n")
        for frame in trace:
            content.append(f"  {frame}\n")
        content.append("\n")
        counter += count

    with open(output_file, 'w') as file:
        file.write(f"Total Count: {counter}\n\n==================\n" + ''.join(content))

@click.command()
@click.option('--filter', required=False, default='*', help='Glob pattern to filter stack frames.')
@click.option('--input-file', required=True, type=click.Path(exists=True), help='Path to the input trace file.')
@click.option('--output-file', required=True, type=click.Path(), help='Path to the output file for filtered traces.')
@click.option('--main-thread-only', required=False, default=False)
def main(filter, input_file, output_file, main_thread_only):
    traces = load_traces(input_file)
    filtered_traces = filter_and_sort_traces(traces, filter, main_thread_only)

    write_traces_to_file(filtered_traces, output_file)
    print(f"Filtered and sorted traces matching pattern: {filter} have been written to {output_file}")

if __name__ == "__main__":
    main()
