<h1 align="center">HyRES: Hybrid Reasoning For Structure Recovery With Semantic Enhancement</h1>

<h4 align="center">
<p>
<a href=#about>About</a> |
<a href=#new>New</a> |
<a href=#install>Install</a> |
<a href=#train>Train</a> |
<a href=#quickstart>QuickStart</a> |
<a href=#data>Data</a> |
<a href=#acknowledgement>Acknowledgement</a> |
<p>
</h4>

## About

llasm, is a novel framework that fuses encoder-only and decoder-only LLMs, which utilizes their capabilities to better comprehend assembly language and have better generalizability at function naming.

## News

- [2024/3/31] The base model of llasm-encoder is now available on Hugging Face Model Hub (https://huggingface.co/sandspeare/llasm-encoder).
- [2024/3/31] The base model of llasm-decoder is now available on Hugging Face Model Hub (https://huggingface.co/sandspeare/llasm-decoder).

## Install

1. Install Package
```Shell
conda create -n llasm python=3.10 -y
conda activate llasm
pip install --upgrade pip
pip install -e .
```

2. Install additional packages for training cases
```
pip install ninja
pip install flash-attn==1.0.2
```

## Train

### Hyperparameters
We use a similar set of hyperparameters as LLaVA in finetuning.  Both hyperparameters used in pretraining and finetuning are provided below.

1. Pretraining

| Hyperparameter | Global Batch Size | Learning rate | Epochs | Max length | Weight decay |
| --- | ---: | ---: | ---: | ---: | ---: |
| LLasm-13B | 128 | 2e-3 | 1 | 2048 | 0 |

2. Finetuning

| Hyperparameter | Global Batch Size | Learning rate | Epochs | Max length | Weight decay |
| --- | ---: | ---: | ---: | ---: | ---: |
| LLasm-13B | 32 | 2e-5 | 3 | 2048 | 0 |


### Pretrain

Pretrain takes around 24 hours for LLasm-13B on 4x A100 (80G).

```Shell
./scripts/train.sh
```

### Instruction Tuning

Tuning takes around 24 hours for LLasm-13B on 4x A100 (80G).

```Shell
./scripts/test.sh
```


## QuickStart

### Inference

```Shell
python ./eval/eval_binary.py
```

### Evaluation

```Shell
python ./eval/performance.py
```

We will release all evaluation datasets after publication.

## Data
performance across differnet optimization
```
./llasm/eval/save/dataset
```
performance on mirai malware

```
./llasm/eval/save/mirai
```

## Acknowledgement

- [Vicuna](https://github.com/lm-sys/FastChat): the base model we built upon, and our base model Vicuna-13B that has the amazing language capabilities!