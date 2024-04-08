from transformers import AutoTokenizer, AutoModel
import os

tokenizer = AutoTokenizer.from_pretrained("/root/autodl-tmp/chatglm3-6b/", trust_remote_code=True)
model = AutoModel.from_pretrained("/root/autodl-tmp/chatglm3-6b/", trust_remote_code=True,top_p=0, 
  temperature=0.3).cuda()

messages = []
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

years=["First_Level_CRCEE_2013"]
for year in years:
  print("Code of the examination",year)
  Questions=read_excel_column(year+".xlsx", "Sheet1", "Question")
  Answers=read_excel_column(year+".xlsx", "Sheet1", "Answer")
  df = pd.DataFrame(columns=["Question","Correct_Answer","Answer1", "Score1"])
  for i in range(len(Questions)):
    message=Questions[i]

    def final_score(Question,answers_from_model,answers):
      if "四个" in Question:
        score = score_of_single_choice(answers_from_model, answers)
      if "五个" in Question:
        score = score_of_multi_choice(answers_from_model, answers)
      return score
    
    history=[]
    answers_from_model,history = model.chat(tokenizer, Questions[i],history=[])

    answer1=answers_from_model

    df2 = pd.DataFrame([
    {"Question":Questions[i],"Correct_Answer":Answers[i],"Answer1":answer1,"Score1":final_score(Questions[i],answer1,Answers[i])}])
    print("No Question",i+1,"\n","Right_Answer:",Answers[i],"\nAnswer_from_original_ChatGLM3-6B:",answer1.strip().replace("\n",""))
    df = pd.concat([df, df2], axis=0)
  save_df_to_excel(df, "All_answers_from_original_ChatGLM3-6B"+year+".xlsx", "sheet1")



        
