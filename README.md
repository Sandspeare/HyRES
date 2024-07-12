<h1 align="center">HyRES: Recovering Data Structures in Binaries via Semantic-Enhanced Hybrid Reasoning</h1>

<h4 align="center">
<p>
<a href=#about>About</a> |
<a href=#new>New</a> |
<a href=#details>Details</a> |
<a href=#data>Data</a> |
<a href=#acknowledgement>Acknowledgement</a>
<p>
</h4>

## About

HyRES is an innovative hybrid reasoning technique that combines static analysis, large language model (LLM), and heuristic methods to recover data structures from stripped binaries. We present part of code. The full implementation will be public after publication.

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
Extract initial facts from LLVM IR for static analysis.
```Shell
cd ./pass && make output

./pass/bin/fact intput.ll ./facts
```

### Static analysis
Datalog rules for static structure analysis.
```Shell
python ./datalog/run.py
```

### Semantics
We use Qwen2 and the following prompt to recover semantics, details in paper.
```
You are a professional reverse engineer, analyze the following C functions: \textcolor{red}{CODE}. If you have better structure filed \textcolor{blue}{(names, types)}, suggest to complete the following JSON dictionary, if not, preserve the original field \textcolor{blue}{(names, types)}. \textcolor{red}{FIELD}. Reply with a JSON dictionary where keys are the original filed names and values are the proposed \textcolor{blue}{(names, types)}. \textcolor{gray}{The field type can only be chosen from "bool, char, word, dword, qword, float, funcptr, structptr and arrayptr"}. Do not explain anything, only print the JSON dictionary.
```

We generate GTE-large for text embedding generation.
```Shell
python encode.py
```


## Data

Vulnerabilities related to structure in ./binaries. The other will be public in google driver after publication due to storage limitation. 

| Vulnerability | Structure Name   | Access Method | Layout    |
| ------------- | ---------------- | ------------- | --------- |
| CVE-2022-1851 | window\_S        | global        | 158 / 162 |
| CVE-2022-0554 | file\_buffer     | indirect      | 147 / 240 |
| CVE-2022-1619 | cmdline\_info\_T | global        | 6 / 14    |
| CVE-2021-3974 | regexec\_T       | global        | 0 / 25    |
| CVE-2021-3984 | pos\_T           | stack         | 3 / 3     |
| CVE-2021-3875 | undoline\_T      | indirect      | 2 / 2     |
| CVE-2022-0407 | block\_def       | indirect      | 14 / 14   |
| CVE-2021-3927 | file\_buffer     | global        | 147 / 240 |
| CVE-2022-0408 | trystate\_T      | indirect      | 20 / 20   |
| CVE-2022-1160 | garray\_T        | stack         | 5 / 5     |
| CVE-2022-1769 | garray\_T        | stack         | 5 / 5     |
| CVE-2022-0213 | window\_S        | indirect      | 158 / 162 |
| CVE-2022-0368 | data\_block      | indirect      | 6 / 6     |
| CVE-2021-4166 | exarg            | indirect      | 24 / 30   |
| CVE-2022-0392 | garray\_T        | stack         | 5 / 5     |
| CVE-2021-3903 | pos\_T           | indirect      | 3 / 3     |
| CVE-2022-0359 | cmdline\_info\_T | global        | 6 / 14    |

## Acknowledgement

- [Qwen2](https://github.com/QwenLM/Qwen2): the inference LLM in HyRES that has the amazing language capabilities!
- [GTE](https://huggingface.co/thenlper/gte-large): the encoder for text embeddings generation.
- [vandalir](https://github.com/vandaltool/vandalir): the code base for datalog-based analysis.
