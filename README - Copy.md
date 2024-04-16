# Augmenting large language models with domain-specific multimodal knowledge graph for question-answering in construction project management

## !!! As the paper is under review, all materials in this repository currently are not allowed to be re-used by anyone until this announcement is deleted.

# 0. Videos of running the LLMs before and after integrating the multiple CPM-KG
![GIF for running video of LLMs with CPM-KG.gif](https://s2.loli.net/2024/04/16/WTyF9DnsqlQKCNH.gif)
↑↑↑Multiple original LLMs simultaneously answering the CPM-related questions

![GIF for running video of LLMs with CPM-KG.gif](https://s2.loli.net/2024/04/16/WTyF9DnsqlQKCNH.gif)
↑↑↑Multiple LLMs with CPM-KG simultaneously answering the CPM-related questions


# 1. General introduction of this repository

1.1 This repository aims at providing the codes and data regarding the paper entitled “……” for the public, and it is developed by University of XXX in UK,  The University of XX in Hong Kong SAR, and XXX University in China.

1.2 We greatly appreciate the selfless spirits of these voluntary contributors of a series of open python libraries, including langchain, llamaindex, meta's llama2, openai, chatglm, numpy, and so on. Our work stands on the shoulders of these giants.

1.3 As for anything regarding the copyright, please refer to the MIT License or contact the authors.

# 2. Summary of supplemental materials in this repository

The table below shows all supplemental materials. All sheets in Tables S1, S2, and S3 are arranged in the order shown in this table.



All supplemental materials are provided in Github repository (https://huggingface.co/datasets/AnonymousSite/QA_dataset_for_CPM). Besides the Github repository, the  CCLR QA dataset is also shared in Hugging Face repository (https://github.com/0AnonymousSite0/QA_for_CPM).

# 3. LLM Leaderboard for CCLR QA

The test results of different large language models on the QA dataset for Chinese Construction Project Management are shown below. Welcome global scholars to test their LLM works on CPM-QA, please see the following specification of reusing the QA dataset.

| Large Language Model | Publishing Institution | Overall Scoring Rate | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | Ranking |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|------|------|------|
| ERNIE-Bot 4.0 with knowledge graph | Baidu&The authors | 0.822 | 0.842 | 0.826 | 0.830 | 0.801 | 0.853 | 0.842 | 0.800 | 0.862 | 1 |
| ERNIE-Bot 4.0 | Baidu | 0.757 | 0.783 | 0.718 | 0.762 | 0.768 | 0.724 | 0.724 | 0.731 | 0.788 | 2 |
| GPT-4 with knowledge graph | OpenAI&The authors | 0.666 | 0.719 | 0.734 | 0.661 | 0.660 | 0.757 | 0.681 | 0.664 | 0.689 | 3 |
| GPT-4 | OpenAI | 0.532 | 0.602 | 0.490 | 0.556 | 0.536 | 0.570 | 0.519 | 0.514 | 0.566 | 4 |
| GPT-3.5-turbo with knowledge graph | OpenAI&The authors | 0.504 | 0.532 | 0.503 | 0.527 | 0.472 | 0.626 | 0.522 | 0.540 | 0.467 | 5 |
| ChatGLM3-6B with knowledge graph | Tsinghua & Zhipu.AI | 0.483 | 0.497 | 0.444 | 0.510 | 0.421 | 0.540 | 0.596 | 0.543 | 0.444 | 6 |
| Text-davinci-003 with knowledge graph | OpenAI&The authors | 0.482 | 0.507 | 0.521 | 0.470 | 0.478 | 0.582 | 0.516 | 0.510 | 0.516 | 7 |
| Qianfan-Chinese-Llama-2-7B with knowledge graph| Baidu&The authors | 0.474 | 0.474 | 0.486 | 0.494 | 0.469 | 0.570 | 0.529 | 0.514 | 0.470 | 8 |
| ChatGLM2-6B with knowledge graph | Tsinghua & Zhipu.AI | 0.472 | 0.471 | 0.469 | 0.488 | 0.464 | 0.517 | 0.507 | 0.528 | 0.462 | 9 |
| ChatGLM2-6B | Tsinghua & Zhipu.AI | 0.430 | 0.454 | 0.412 | 0.477 | 0.409 | 0.469 | 0.444 | 0.494 | 0.420 | 10 |
| ChatGLM3-6B | Tsinghua & Zhipu.AI | 0.399 | 0.452 | 0.389 | 0.415 | 0.356 | 0.412 | 0.389 | 0.416 | 0.399 | 11 |
| Qianfan-Chinese-Llama-2-7B | Baidu | 0.373 | 0.421 | 0.377 | 0.364 | 0.359 | 0.422 | 0.374 | 0.411 | 0.358 | 12 |
| GPT-3.5-turbo | OpenAI | 0.348 | 0.422 | 0.317 | 0.368 | 0.322 | 0.438 | 0.332 | 0.405 | 0.333 | 13 |
| Llama-2-70b with knowledge graph | MetaAI&The authors | 0.377 | 0.335 | 0.369 | 0.323 | 0.328 | 0.414 | 0.354 | 0.335 | 0.332 | 14 |
| Text-davinci-003 | OpenAI | 0.328 | 0.351 | 0.318 | 0.343 | 0.334 | 0.382 | 0.343 | 0.361 | 0.341 | 15 |
| Llama-2-70b | MetaAI | 0.284 | 0.284 | 0.338 | 0.255 | 0.316 | 0.313 | 0.291 | 0.299 | 0.293 | 16 |

# 4. Reuse of the multiple CPM-KG 

## 4.1 Three optional versions of CPM-KG



The CPM-KG is available through this link (XX).

## 4.2 Data layer details of CPM-KG
The data layer development in the CPM-KG includes determining the three-tier knowledge field framework, collecting and iteratively refining the laws and regulations, and dividing each law or regulation into multiple clauses.



↑↑↑43 triples of [knowledge field, has subfield of, knowledge field]



↑↑↑278 triples of [tertiary knowledge field, involves, document]



↑↑↑1,375 triples of [document, contains, document content]

# 5. Reuse of the CPM-QA test dataset

Our dataset is specifically tailored to the CPM field and encompasses 2,435 questions.



↑↑↑The CPM-QA dataset in huggingface



↑↑↑The examples of one single-answer and multiple-answer question in the CPM-QA dataset

More information about the dataset can be found through this link (https://huggingface.co/datasets/AnonymousSite/QA_dataset_for_CPM).

# 6. Reuse of the codes for running LLMs with and without CPM-KG
 
## 6.1 Environment set

All codes are developed on Python 3.9, and the IDE adopted is PyCharm (Professional version). The codes also support GPU computing for higher speed; the Navida CUDA we adopted is V10.0.130. The GIS platform is Arcgis Pro 2.3, and its license is necessary. 

aiohttp==3.9.0

aiolimiter==1.1.0

aiosignal==1.3.1

aiostream==0.5.2

annotated-types==0.6.0

anyio==3.7.1

Appium-Python-Client==3.1.0

async-timeout==4.0.3

attrs==23.1.0

backoff==2.2.1

bce-python-sdk==0.8.96

bcrypt==4.0.1

beautifulsoup4==4.12.2

......

Please refer to the supplementary materials for the complete requirement file.(https://github.com/0AnonymousSite0/QA_for_CPM/XXX)

Before submitting these codes to Github, all of them have been tested to be well-performed (as shown in the screenshots). Even so, we are not able to guarantee their operation in other computing environments due to the differences in the Python version, computer operating system, and adopted hardware.

## 6.2 Codes for testing the LLMs

Closed-source LLMs are API-only, while open-source LLMs over 24GB also use APIs to avoid high-end GPU costs. The open-source LLMs under 24GB are deployed directly on the AutoDL Cloud server with GTX 4090 GPUs.



↑↑↑Codes for testing original large language models



↑↑↑Codes for testing large language models integrating CPM-KG
