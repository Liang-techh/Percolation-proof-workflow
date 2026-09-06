Cancelled after the user's instruction to finish only the cached comparator
attempt and avoid toolchain rebuilding. The local-exporter script process was
sent SIGTERM before exporter-source extraction/build or comparator execution.
Strict mathematics compilation and the dependency audit had passed.
The EXIT trap printed RUN_EXIT_CODE=0 during termination; this is not a
completed run or comparator acceptance. No tool rebuild was performed.
