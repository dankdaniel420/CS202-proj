#!/bin/bash

test_dir="example_testcases"
output_dir="outputs/output_$(date +%Y%m%d%H%M)"

mkdir -p "$output_dir"

for infile in $test_dir/*.in; do
    base_name=$(basename "$infile" .in)

    python3 vrp.py < "$infile" > "$output_dir/$base_name.out"

done

echo "All test cases have been processed and saved in $output_dir."