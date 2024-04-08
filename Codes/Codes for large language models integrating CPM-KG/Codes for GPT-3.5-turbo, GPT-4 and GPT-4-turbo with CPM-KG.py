import openai
import os
os.environ["OPENAI_API_KEY"] = ' '

messages = []
import os
import pandas as pd
os.environ["http_proxy"] = "http://localhost:7897"
os.environ["https_proxy"] = "http://localhost:7897"

import chromadb
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index.llms import OpenAI
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext

documents = SimpleDirectoryReader(r' ', recursive=True, exclude_hidden=True).load_data()
print("Local Knowledge are loaded")
db = chromadb.PersistentClient(path="./storage_of_CPM-KG")
chroma_collection = db.get_or_create_collection("storage_of_CPM-KG")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

llm = OpenAI(temperature=0.01, model="gpt-3.5-turbo")
service_context = ServiceContext.from_defaults(llm=llm)

# Replace GPT-4 model
# llm = OpenAI(temperature=0, model="gpt-4")
# service_context = ServiceContext.from_defaults(llm=llm)

# Replace GPT-4-turbo model
# llm = OpenAI(temperature=0, model="gpt-4-1106-preview")
# service_context = ServiceContext.from_defaults(llm=llm)

index1 = VectorStoreIndex.from_documents(documents,service_context=service_context,show_progress=True)
index1 = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context,show_progress=True
)
print("index1 are created")
# If index1 is created and stored, it is directly loaded
# index1 = VectorStoreIndex.from_vector_store(
#     vector_store, storage_context=storage_context
# )
# print("index1 are read directly")

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

years=["First_Level_CRCEE_2013"]

query_engine = index1.as_query_engine(service_context=service_context)

for year in years:
  print("Code of the examination",year)
  Questions=read_excel_column(year+".xlsx", "Sheet1", "Question")
  Answers=read_excel_column(year+".xlsx", "Sheet1", "Answer")
  df = pd.DataFrame(columns=["Question","Correct_Answer",'Answer1', "Score1"])
  for i in range(len(Questions)):
    answer1 = query_engine.query(Questions[i])

    df2 = pd.DataFrame([{"Question":Questions[i],"Correct_Answer":Answers[i],"Answer1":answer1,"Score1":final_score(Questions[i],answer1,Answers[i])}])
    print("No of Question",i+1,"\n","Right_Answer:",Answers[i],"\n"+"Answer_from_GPT-3.5-turbo_with_CPM-KG:",str(answer1).strip().replace("\n",""))

    df = pd.concat([df, df2], axis=0)
  save_df_to_excel(df, "Answer_from_GPT-3.5-turbo_with_CPM-KG"+year+".xlsx", "sheet1")



