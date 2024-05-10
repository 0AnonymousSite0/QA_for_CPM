import os
import pandas as pd
os.environ['QIANFAN_AK'] = " "
os.environ['QIANFAN_SK'] = " "

uri = "bolt://localhost:7687"
username = "neo4j"
password = " "
database = "neo4j"

query="""
match (n)-[r]-(m) 
return n,r,m
"""

def score_of_single_choice(answers_from_model, correct_answer):
  score = 0
  number_of_answers=0
  if correct_answer in str(answers_from_model):
    score = 1
  if "A" in correct_answer:
    number_of_answers=number_of_answers+1
  if "B" in correct_answer:
    number_of_answers=number_of_answers+1
  if "C" in correct_answer:
    number_of_answers=number_of_answers+1
  if "D" in correct_answer:
    number_of_answers=number_of_answers+1
  if number_of_answers>1:
    score=0
  return score
def save_df_to_excel(df, file_path, sheet_name):
  writer = pd.ExcelWriter(file_path)
  df.to_excel(writer, sheet_name=sheet_name, index=False)
  writer.close()

def split_correct_answers(string):
  answer = []
  for character in string:
    answer.append(character)
  return answer
def score_of_multi_choice(answers_from_model, correct_answers):
  score = 0
  correct_ones = 0
  missed_ones = 0
  wrong_ones = 0
  individual_correct_answers = split_correct_answers(correct_answers)
  for individual_answer in individual_correct_answers:
    if individual_answer in str(answers_from_model):
      correct_ones = correct_ones + 1
    if individual_answer not in str(answers_from_model):
      missed_ones = missed_ones + 1
  wrong_answers = set(["A", "B", "C", "D", "E"]).difference(correct_answers)
  for individual_wrong_answer in wrong_answers:
    if individual_wrong_answer in str(answers_from_model):
      wrong_ones = wrong_ones + 1
  if wrong_ones == 0:
    if missed_ones == 0:
      score = 2
    else:
      score = min(correct_ones * 0.5, 2)
  return score

def read_excel_column(file_path, sheet_name, column_name):
  df = pd.read_excel(file_path, sheet_name=sheet_name)
  column_data = df[column_name].tolist()
  return column_data

def final_score(Question, answers_from_model, answers):
  if "四个" in Question:
    score = score_of_single_choice(answers_from_model, answers)
  if "五个" in Question:
    score = score_of_multi_choice(answers_from_model, answers)
  return score

is_chinese = True

if is_chinese:
    CUSTOM_PROMPT_TEMPLATE = """
       利用所提供的知识从选项中选出正确的答案，回答仅限于选项字母，不做额外的阐述。
        知识:{context}
        问题:{question}
    """
    QUESTION1 = """
        单项选择题，利用所提供的知识从四个选项中选出唯一正确的答案，回答仅限于选项字母，不做额外的阐述。
        建设项目工程总承包的项目管理工作主要在项目的（  ）。 
        A 决策阶段、实施阶段、使用阶段        B 实施阶段        C 设计阶段、施工阶段、保修阶段        D 施工阶段
    """
    QUESTION2 = """
        多项选择题，利用所提供的知识从五个选项中选出多个正确的答案，回答仅限于选项字母，不做额外的阐述。
        根据《质量管理体系基础和术语》，质量控制是质量管理的一部分，是致力于满足质量要求的一系列相关活动。这些活动主要包括（  ）。      
        A 设定目标    B 测量检查      C 评价分析      D 质量策划    E 纠正偏差
    """
else:
    WEB_URL = "https://lilianweng.github.io/posts/2023-06-23-agent/"
    CUSTOM_PROMPT_TEMPLATE = """
        Utilize the provided knowledge to find accurate answers from choices.
        Focus on the choices strictly without extra elaboration.
        Knowledge:{context}.
        Question:{question}.
    """
    QUESTION1 = "How do agents use Task decomposition?"
    QUESTION2 = "What are the various ways to implemet memory to support it?"

from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import QianfanEmbeddingsEndpoint
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.vectorstores import Chroma
if not os.path.exists('VectorStore_kg'):
    text_loader_kwargs={'autodetect_encoding': True}
    loader = DirectoryLoader(r'D:\AECKnowledge\filesformKG',glob="**/*.csv", show_progress=True)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 250, chunk_overlap = 50, separators=["\n\n", "\n", " ", "", "。", "，"])
    all_splits = text_splitter.split_documents(data)
    vectorstore_kg = Chroma.from_documents(documents=all_splits, embedding=QianfanEmbeddingsEndpoint(),
                                        persist_directory="vectorstore_kg")
    vectorstore_kg.persist()
else:
    vectorstore_kg = Chroma(persist_directory='vectorstore_kg', embedding_function=QianfanEmbeddingsEndpoint())
print("vectorstore_stored")

from langchain.chat_models import QianfanChatEndpoint
from langchain.prompts import PromptTemplate

QA_CHAIN_PROMPT = PromptTemplate.from_template(CUSTOM_PROMPT_TEMPLATE)

llm_llama_2_70b = QianfanChatEndpoint(streaming=True, model="Llama-2-70b-chat")
llm_ERNIE_Bot = QianfanChatEndpoint(streaming=True, model="ERNIE-Bot",temperature=0.01,top_p=0,penalty_score=1)
llm_ERNIE_Bot_turbo40 = QianfanChatEndpoint(streaming=True, model="ERNIE-Bot-4",temperature=0.01,top_p=0,penalty_score=1)
llm_Qianfan_Chinese_Llama_2_7B = QianfanChatEndpoint(streaming=True, model="Qianfan-Chinese-Llama-2-7B")

retriever = vectorstore_kg.as_retriever(search_type="similarity_score_threshold", search_kwargs={'score_threshold': 0.1})

from langchain.chains import RetrievalQA

qa_chain_llm_llama_2_70b = RetrievalQA.from_chain_type(llm_llama_2_70b, retriever=retriever, chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}, return_source_documents=True)
qa_chain_llm_ERNIE_Bot = RetrievalQA.from_chain_type(llm_ERNIE_Bot, retriever=retriever, chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}, return_source_documents=True)
qa_chain_llm_ERNIE_Bot_turbo40 = RetrievalQA.from_chain_type(llm_ERNIE_Bot_turbo40, retriever=retriever, chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}, return_source_documents=True)
qa_chain_llm_Qianfan_Chinese_Llama_2_7B = RetrievalQA.from_chain_type(llm_Qianfan_Chinese_Llama_2_7B, retriever=retriever, chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}, return_source_documents=True)

years=["First_Level_CRCEE_2013"]

for year in years:
  print("Code of the examination",year)
  Questions=read_excel_column(year+".xlsx", "Sheet1", "Question")
  Answers=read_excel_column(year+".xlsx", "Sheet1", "Answer")
  df = pd.DataFrame(columns=["Question","Correct_Answer","Answer1", "Score1","Answer2", "Score2","Answer3", "Score3","Answer4", "Score4"])
  for i in range(len(Questions)):
    result_llm_llama_2_70b = qa_chain_llm_llama_2_70b({"query": Questions[i]})
    result_llm_ERNIE_Bot = qa_chain_llm_ERNIE_Bot({"query": Questions[i]})
    result_llm_ERNIE_Bot_turbo40 = qa_chain_llm_ERNIE_Bot_turbo40({"query": Questions[i]})
    result_llm_Qianfan_Chinese_Llama_2_7B = qa_chain_llm_Qianfan_Chinese_Llama_2_7B({"query": Questions[i]})

    df2 = pd.DataFrame([{"Question":Questions[i],"Correct_Answer":Answers[i],
                         "Answer1": result_llm_llama_2_70b['result'],"Score1": final_score(Questions[i], result_llm_llama_2_70b['result'], Answers[i]),
                         "Answer2": result_llm_ERNIE_Bot['result'],"Score2": final_score(Questions[i], result_llm_ERNIE_Bot['result'], Answers[i]),
                         "Answer3": result_llm_ERNIE_Bot_turbo40['result'],"Score3": final_score(Questions[i], result_llm_ERNIE_Bot_turbo40['result'], Answers[i]),
                         "Answer4": result_llm_Qianfan_Chinese_Llama_2_7B['result'],"Score4": final_score(Questions[i], result_llm_Qianfan_Chinese_Llama_2_7B['result'],Answers[i])}])

    print("No of Question",i+1,"\n","Right_Answer:",Answers[i],
          "\n"+"Answer_from_llama_2_70b_with_local_knowledge:",str(result_llm_llama_2_70b['result']).strip().replace("\n",""),
          "\n"+"Answer_from_ERNIE_Bot_with_local_knowledge:",str(result_llm_ERNIE_Bot['result']).strip().replace("\n",""),
          "\n"+"Answer_from_ERNIE_Bot_turbo40_with_local_knowledge:",str(result_llm_ERNIE_Bot_turbo40['result']).strip().replace("\n",""),
          "\n"+"Answer_from_Qianfan_Chinese_Llama_2_7B:",str(result_llm_Qianfan_Chinese_Llama_2_7B['result']).strip().replace("\n",""))
    df = pd.concat([df, df2], axis=0)
  save_df_to_excel(df, "Answer_from_ERNIE-Bot_ERNIE-Bot 4.0_Qianfan-Chinese-Llama-2-7B_Llama-2-70B-Chat_with_CPM-KG"+year+".xlsx", "sheet1")
