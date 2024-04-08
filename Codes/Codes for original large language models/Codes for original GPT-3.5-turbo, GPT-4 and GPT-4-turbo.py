import openai
import os
os.environ["OPENAI_API_KEY"] = ' '

messages = []
import os
import pandas as pd
os.environ["http_proxy"] = "http://localhost:7897"
os.environ["https_proxy"] = "http://localhost:7897"

from openai import OpenAI
client = OpenAI(
    api_key=os.environ.get(" "),
)

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

for year in years:
  print("Code of the examination",year)
  Questions=read_excel_column(year+".xlsx", "Sheet1", "Question")
  Answers=read_excel_column(year+".xlsx", "Sheet1", "Answer")
  df = pd.DataFrame(columns=["Question","Correct_Answer","Answer1", "Score1","Answer2", "Score2","Answer3", "Score3"])
  for i in range(len(Questions)):
    message=Questions[i]
    messages=[{"role":"user","content": message}]
    completion_gpt_35_turbo = openai.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=messages,
      top_p=0,
      temperature =0.5
    )

    completion_gpt_4 = openai.chat.completions.create(
      model="gpt-4",
      messages=messages,
      top_p=0,
      temperature =0.5
    )

    completion_gpt_4_1106_preview = openai.chat.completions.create(
      model="gpt-4-1106-preview",
      messages=messages,
      top_p=0,
      temperature =0.5
    )

    answer1 = completion_gpt_35_turbo.choices[0].message.content
    answer2 = completion_gpt_4.choices[0].message.content
    answer3 = completion_gpt_4_1106_preview.choices[0].message.content

    df2 = pd.DataFrame([{"Question":Questions[i],"Correct_Answer":Answers[i],
                         "Answer1":answer1,"Score1":final_score(Questions[i],answer1,Answers[i]),
                         "Answer2":answer1,"Score2":final_score(Questions[i],answer2,Answers[i]),
                         "Answer3":answer1,"Score3":final_score(Questions[i],answer3,Answers[i])}])
    print("No of Question",i+1,"\n","Right_Answer:",Answers[i],
          "\n"+"Answer_from_original_GPT-3.5-turbo:",str(answer1).strip().replace("\n",""),
          "\n"+"Answer_from_original_GPT-4:",str(answer1).strip().replace("\n",""),
          "\n"+"Answer_from_original_GPT-4-turbo:",str(answer1).strip().replace("\n",""))
    df = pd.concat([df, df2], axis=0)
  save_df_to_excel(df, "Answer_from_original_GPT-3.5-turbo_GPT-4_GPT-4-turbo"+year+".xlsx", "sheet1")



