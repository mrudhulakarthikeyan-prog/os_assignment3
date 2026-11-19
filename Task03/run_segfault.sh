#!/usr/bin/env bash
set +e
./segfault_demo
status=$?
echo "Exit status: $status (a non-zero status is expected for this deliberate fault)"
