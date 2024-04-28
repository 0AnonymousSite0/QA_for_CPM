# Augmenting general-purpose large-language models with domain-specific multimodal knowledge graph for question-answering in construction project management 

## !!! As the paper is under review, all materials in this repository currently are not allowed to be re-used by anyone until this announcement is deleted.

# 0. Videos of running the GLMs before and after integrating the multimodal CPM-KG
![GIF for running video of original GLMs.gif](https://github.com/0AnonymousSite0/QA_for_CPM/blob/main/Images%20for%20Readme/GIF%20for%20running%20video%20of%20original%20GLMs.gif)

↑↑↑Multiple original GLMs simultaneously answering the CPM-related questions

![GIF for running video of GLMs with CPM-KG](https://github.com/0AnonymousSite0/QA_for_CPM/blob/main/Images%20for%20Readme/GIF%20for%20running%20video%20of%20GLMs%20with%20%20CPM-KG.gif)

↑↑↑Multiple GLMs with CPM-KG simultaneously answering the CPM-related questions


# 1. General introduction of this repository

1.1 This repository aims at providing the codes and data regarding the paper entitled “……” for the public, and it is developed by University of XXX in UK,  The University of XX in Hong Kong SAR, and XXX University in China.

1.2 We greatly appreciate the selfless spirits of these voluntary contributors of a series of open python libraries, including langchain, llamaindex, meta's llama2, openai, chatglm, numpy, and so on. Our work stands on the shoulders of these giants.

1.3 As for anything regarding the copyright, please refer to the MIT License or contact the authors.

# 2. Summary of supplemental materials in this repository

The table below shows all supplemental materials. All sheets in Tables S1, S2, and S3 are arranged in the order shown in this table.

![supplemental materials](https://github.com/0AnonymousSite0/QA_for_CPM/blob/main/Images%20for%20Readme/Inventory%20of%20supplemental%20materials.png)

All supplemental materials are provided in Github repository (https://huggingface.co/datasets/AnonymousSite/QA_dataset_for_CPM). Besides the Github repository, the CPM-QA dataset is also shared in Hugging Face repository (https://github.com/0AnonymousSite0/QA_for_CPM).

# 3. GLM Leaderboard for CPM-QA

The test results of different GLMs on the QA dataset for Chinese Construction Project Management are shown below. Welcome global scholars to test their GLM works on CPM-QA, please see the following specification of reusing the QA dataset.

| General-purpose large-language models | Publishing institution | Accuracy rate of SAMCQs | Accuracy rate of MAMCQs | Accuracy rate of text-only questions | Accuracy rate of image-embedded questions | Average accuracy rate | Ranking |
|-----|-----|-----|-----|-----|-----|-----|-----|
| ERNIE-Bot 4.0 with CPM-KG | Baidu&The authors | 0.773 | 0.568 | 0.701 | 0.224 | 0.682 | 1 |
| GPT-4-turbo with CPM-KG | OpenAI&The authors | 0.723 | 0.543 | 0.661 | 0.250 | 0.643 | 2 |
| GPT-4 with CPM-KG | OpenAI&The authors | 0.686 | 0.550 | 0.646 | 0.218 | 0.628 | 3 |
| ERNIE-Bot 4.0 | Baidu | 0.726 | 0.442 | 0.621 | 0.166 | 0.602 | 4 |
| ERNIE-Bot with CPM-KG | Baidu&The authors | 0.727 | 0.361 | 0.578 | 0.235 | 0.566 | 5 |
| GPT-4-turbo | OpenAI | 0.589 | 0.372 | 0.503 | 0.235 | 0.494 | 6 |
| GPT-3.5-turbo with CPM-KG | OpenAI&The authors | 0.538 | 0.394 | 0.480 | 0.244 | 0.472 | 7 |
| ERNIE-Bot | Baidu | 0.656 | 0.234 | 0.481 | 0.218 | 0.471 | 8 |
| GPT-4 | OpenAI | 0.591 | 0.313 | 0.482 | 0.198 | 0.470 | 9 |
| ChatGLM3-6B with CPM-KG | Tsinghua & Zhipu.AI | 0.497 | 0.319 | 0.424 | 0.238 | 0.418 | 10 |
| Qianfan-Chinese-Llama-2-7B with CPM-KG | Baidu&The authors | 0.464 | 0.238 | 0.369 | 0.221 | 0.367 | 11 |
| ChatGLM3-6B | Tsinghua & Zhipu.AI | 0.419 | 0.262 | 0.355 | 0.203 | 0.351 | 12 |
| GPT-3.5-turbo | OpenAI | 0.427 | 0.237 | 0.346 | 0.174 | 0.342 | 13 |
| Llama-2-70B-Chat with CPM-KG | MetaAI&The authors | 0.443 | 0.189 | 0.328 | 0.323 | 0.331 | 14 |
| Llama-2-70B-Chat | MetaAI | 0.335 | 0.137 | 0.247 | 0.235 | 0.249 | 15 |
| Qianfan-Chinese-Llama-2-7B | Baidu | 0.314 | 0.140 | 0.237 | 0.203 | 0.240 | 16 |

# 4. Reuse of the multimodal CPM-KG 

## 4.1 Three optional versions of CPM-KG

![supplemental materials](https://github.com/0AnonymousSite0/QA_for_CPM/blob/main/Images%20for%20Readme/Inventory%20of%20supplemental%20materials.png)

The CPM-KG is available through this link (https://drive.google.com/drive/folders/1-Ok_qjl5ADD8nlCSyEghupGqBz3TIk1W?usp=sharing).

## 4.2 Instance layer details of CPM-KG
Developing the instance layer of the CPM-KG involves building the three-level architecture of CPM knowledge fields, collecting CPM-related documents, and processing multimodal document content with text and image data.


![Figure S1](https://github.com/0AnonymousSite0/QA_for_CPM/blob/main/Images%20for%20Readme/Figure%20S1%2043%20triples%20of%20%5Bknowledge%20field%2C%20has%20subfield%20of%2C%20knowledge%20field%5D.png)
↑↑↑43 triples of [knowledge field, has subfield of, knowledge field]


![Figure S2](https://github.com/0AnonymousSite0/QA_for_CPM/blob/main/Images%20for%20Readme/Figure%20S2%20278%20triples%20of%20%5Btertiary%20knowledge%20field%2C%20involves%2C%20document%5D.png)
↑↑↑278 triples of [tertiary knowledge field, involves, document]


![Figure S3](https://github.com/0AnonymousSite0/QA_for_CPM/blob/main/Images%20for%20Readme/Figure%20S3%201%2C375%20triples%20of%20%5Bdocument%2C%20contains%2C%20document%20content%5D.png)
↑↑↑1,375 triples of [document, contains, document content]

# 5. Reuse of the CPM-QA test dataset

The CPM-QA test dataset containing 2,435 questions is manually tagged with four characteristics. The characteristics are the paper’s level and year, knowledge subfields, single- or multiple-answer questions, and questions with or without images.


![CPM-QA dataset in huggingface](https://github.com/0AnonymousSite0/QA_for_CPM/blob/main/Images%20for%20Readme/CPM-QA%20dataset%20in%20huggingface.png)
↑↑↑The CPM-QA dataset in huggingface


![The annotations of CPM questions characteristics](https://github.com/0AnonymousSite0/QA_for_CPM/blob/main/Images%20for%20Readme/The%20annotations%20of%20CPM%20questions%E2%80%99%20characteristics.png)
↑↑↑The annotations of CPM questions’ characteristics

More information about the dataset can be found through this link (https://huggingface.co/datasets/AnonymousSite/QA_dataset_for_CPM).

# 6. Reuse of the codes for running GLMs with and without CPM-KG
 
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

Please refer to the supplementary materials for the complete requirement file.(https://github.com/0AnonymousSite0/QA_for_CPM/blob/main/Codes/Codes%20for%20running%20GLMs%20integrated%20with%20CPM-KG/requirements.txt)

Before submitting these codes to Github, all of them have been tested to be well-performed (as shown in the images). Even so, we are not able to guarantee their operation in other computing environments due to the differences in the Python version, computer operating system, and adopted hardware.

## 6.2 Codes for testing the GLMs

Closed-source GLMs are API-only, while open-source GLMs over 24GB also use APIs to avoid high-end GPU costs. The open-source GLMs under 24GB are deployed directly on the AutoDL Cloud server with GTX 4090 GPUs.


![Codes for original GLMs](https://github.com/0AnonymousSite0/QA_for_CPM/blob/main/Images%20for%20Readme/Codes%20for%20running%20original%20GLMs.png)
↑↑↑Codes for testing original GLMs


![Codes for GLMs with CPM-KG](https://github.com/0AnonymousSite0/QA_for_CPM/blob/main/Images%20for%20Readme/Codes%20for%20running%20GLMs%20integrated%20with%20CPM-KG.png)
↑↑↑Codes for testing GLMs integrating CPM-KG
