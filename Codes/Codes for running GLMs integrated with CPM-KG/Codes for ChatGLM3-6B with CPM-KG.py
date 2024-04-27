from configs.model_config import *
from chains.local_doc_qa import LocalDocQA
import nltk
from models.loader.args import parser
import models.shared as shared
from models.loader import LoaderCheckPoint
nltk.data.path = [NLTK_DATA_PATH] + nltk.data.path

REPLY_WITH_SOURCE = True

messages = []
import os
import pandas as pd

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

def final_score(Question,answers_from_model,answers):
  if "四个" in Question:
    score = score_of_single_choice(answers_from_model, answers)
  if "五个" in Question:
    score = score_of_multi_choice(answers_from_model, answers)
  return score

def get_file_names(folder):
    file_names = [str(folder)+r"/"+filename for filename in os.listdir(folder) if os.path.isfile(os.path.join(folder, filename))]
    file_name_str = ",".join(file_names)
    return file_name_str

def main():
    llm_model_ins = shared.loaderLLM()
    llm_model_ins.history_len = LLM_HISTORY_LEN
    local_doc_qa = LocalDocQA()
    local_doc_qa.init_cfg(llm_model=llm_model_ins,
                          embedding_model=EMBEDDING_MODEL,
                          embedding_device=EMBEDDING_DEVICE,
                          top_k=VECTOR_SEARCH_TOP_K)
    filepath=get_file_names(r"/root/autodl-tmp/langchain-ChatGLM/knowledge_base/PMdocx1/Allfiles_PM_0127")
    print(filepath)
    filepath = filepath.split(",")
    vs_path=r"/root/autodl-tmp/langchain-ChatGLM/knowledge_base/PMdocx1"
    temp,loaded_files = local_doc_qa.init_knowledge_vector_store(filepath,vs_path)
    if temp is not None:
        vs_path = temp

    years=["First_Level_CRCEE_2013"]

    for year in years:
        print("Code of the examination",year)
        Questions=read_excel_column(year+".xlsx", "Sheet1", "Question")
        Answers=read_excel_column(year+".xlsx", "Sheet1", "Answer")
        df = pd.DataFrame(columns=["Question","Correct_Answer","Answer1", "Score1"])

        for i in range(len(Questions)):
            query=Questions[i]
            answers_from_model = local_doc_qa.get_knowledge_based_answer(query=query,
                                                                         vs_path=vs_path,
                                                                         chat_history=[],
                                                                         streaming=False)
            print(answers_from_model)
            answers_from_model = list(answers_from_model)

            answers_from_model=answers_from_model[0]
            answers_from_model=answers_from_model[0]["result"]
            print(answers_from_model)

            answer1=list(answers_from_model)
            
            df2 = pd.DataFrame([{"Question":Questions[i],"Correct_Answer":Answers[i],"Answer1":answer1,"Score1":final_score(Questions[i],answer1,Answers[i])}])
            print("No Question",i+1,"\n","Right_Answer:",Answers[i],"\nAnswer_fromm_ChatGLM3-6B_with_CPM-KG:",str(answer1).strip().replace("\n",""))
            df = pd.concat([df, df2], axis=0)
        save_df_to_excel(df, "All_answers_from_ChatGLM3-6B_with_CPM-KG"+year+".xlsx", "sheet1")

if __name__ == "__main__":
    args = None
    args = parser.parse_args()
    args_dict = vars(args)
    shared.loaderCheckPoint = LoaderCheckPoint(args_dict)
    main()
