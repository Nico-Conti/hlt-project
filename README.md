# Dialogue Act Classification with BiGRU-RoBERTa

## Introduction
This group project was developed for the **Human Language Technologies** course in the Master’s Degree program at the **University of Pisa**. We tackled **Dialogue Act (DA) classification** with a hybrid neural architecture that combines **RoBERTa** token encodings, **BiGRU** sentence encodings with a **speaker turn** embedding, and a **GRU decoder**.

<br><br>
<p align="center">
  <img src="Stemma_unipi.svg" width="200" height="200">
</p>

<p align="center">
  Computer Science Department<br>
  A project for the Human Language Technologies course<br>
  in the AI Master's program at the University of Pisa.
</p>

## 📖 Overview
We evaluate on two benchmarks:

- **SWDA** — Switchboard Dialogue Act Corpus  
- **MRDA** — ICSI Meeting Recorder Dialog Act Corpus

**Architecture (Bi-GRUBERTa)**  
1) **RoBERTa encoder** at utterance level;  
2) **Speaker-Turn** (0/1) appended post-RoBERTa as an additive embedding (turn change vs. same speaker);  
3) **BiGRU** for contextual sentence-level encoding;  
4) **GRU decoder** with (hard) **guided attention** for aligned seq-to-seq prediction;  
5) **Teacher forcing** schedule and **gradual unfreezing** of RoBERTa layers during fine-tuning.  
We also tested **beam search** decoding (k=5) vs. greedy.

---

## 🚀 Features
- Hybrid **RoBERTa + BiGRU + GRU** with **talker-flag** embeddings.  
- **Guided attention** decoder; **teacher forcing**; **gradual unfreezing**.  
- Ready-to-use Hugging Face datasets (processed splits) for **SWDA** & **MRDA**.  
- Notebooks for beam/greedy decoding variants and ablations.

---

## 📦 Datasets (Hugging Face)
- SWDA (processed): https://huggingface.co/datasets/nico8771/swda_processed  
- MRDA (processed): https://huggingface.co/datasets/nico8771/mrda_processed  

---
## 📊 Results

| Model / Dataset        | SWDA Acc. | MRDA Acc. | SWDA Macro-F1 | MRDA Macro-F1 |
|------------------------|-----------|-----------|---------------|---------------|
| He et al. (2021), reproduced on our dataset | 78.45     | 90.26     | 0.56          | 0.88          |
| **Bi-GRUBERTa (ours)** | **78.72** | **90.70** | **0.57**      | **0.89**      |


---
## 📚 References

- He, Z., Tavabi, L., Lerman, K., & Soleymani, M. (2021). **Speaker Turn Modeling for Dialogue Act Classification.** *Findings of the Association for Computational Linguistics: EMNLP 2021*, 2150–2157.

- Colombo, P., Chapuis, E., Manica, M., Vignon, E., Varni, G., & Clavel, C. (2020). **Guiding Attention in Sequence-to-Sequence Models for Dialogue Act Prediction.** *Proceedings of the AAAI Conference on Artificial Intelligence (AAAI-20).*

- Liu, Y., Ott, M., Goyal, N., Du, J., Joshi, M., Chen, D., … Stoyanov, V. (2019). **RoBERTa: A Robustly Optimized BERT Pretraining Approach.** *arXiv preprint* arXiv:1907.11692.

---

## 📑 Detailed Report

For a comprehensive explanation of our methodology, architecture choices, hyperparameter settings, and extended results (including confusion matrices and ablation studies), please refer to the project report:

➡️ [Bi-GRUBERTa Model for Dialogue Act Classification (PDF)](./Bi_GRUBERTa_model_for_Dialogue_Act_Classification.pdf)

The report contains additional diagrams and discussions that complement this README.
