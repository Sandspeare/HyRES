<h1 align="center">HyRES: Recovering Data Structures in Binaries via Semantic-Enhanced Hybrid Reasoning</h1>

<h4 align="center">
<p>
<a href=#about>About</a> |
<a href=#new>New</a> |
<a href=#details>Details</a> |
<a href=#data>Data</a>
<p>
</h4>

## About

HyRES is an innovative hybrid reasoning technique that combines static analysis, large language model (LLM), and heuristic methods to recover data structures from stripped binaries. 

![1](./img/overview.jpg)

## News

- [2024/7/10] Paper is ready for review.

## Details

We present description for each file.

### Label
Extract ground truth from binaries.
```Shell
/path/to/idat64 -A -S"label.py [output]" /path/to/binary
```

### Transformation
Transform LLVM Intermediate Representation into IDA microcode.
```Shell
/path/to/idat64 -A -S"ida2llvm.py [output]" /path/to/binary
```

### Facts
Extract initial facts from LLVM IR for static analysis
```Shell
cd ./pass && make output
```
```Shell
./pass/bin/fact intput.ll ./facts
```

### Normailization

### Semantics

### Static analysis

### Heuristic aggregation

## Data

