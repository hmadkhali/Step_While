#!/usr/bin/env bash

check() {
    run sh -c "echo '$1' | ./while-ss"
    echo "$1 \n= \n$2\nYour code outputs \n$output"
    [ "$output" = "$2" ]
}

checkOr() {
    run sh -c "echo '$1' | ./while-ss"
    echo "$1 \n= \n$2\nOR \n$3\nYour code outputs \n$output"
    [ "$output" = "$2" ] || [ "$output" = "$3" ]
}
