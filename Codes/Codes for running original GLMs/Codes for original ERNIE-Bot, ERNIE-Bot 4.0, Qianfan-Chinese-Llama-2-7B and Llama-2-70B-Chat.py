import requests
import json
import qianfan
import pandas as pd
import os
chat_comp = qianfan.ChatCompletion(ak=" ", sk=" ")
os.environ['QIANFAN_AK'] = " "
os.environ['QIANFAN_SK'] = " "

def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token?client_id=ewcQGuXT4otZmj5Y3jBFNj5h&client_secret=ouQUt1pt5CfRnjamXQfsGvFqI01D3pBo&grant_type=client_credentials"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")
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
  print("string:", string)
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
  score=0
  if "四个" in Question:
    score = score_of_single_choice(answers_from_model, answers)

  if "五个" in Question:
    score = score_of_multi_choice(answers_from_model, answers)

  return score

years=["First_Level_CRCEE_2013"]

for year in years:
  print("Year",year)
  Questions=read_excel_column(year+".xlsx", "Sheet1", "Question")
  Answers=read_excel_column(year+".xlsx", "Sheet1", "Answer")
  df = pd.DataFrame(columns=["Question","Correct_Answer","Answer1", "Score1","Answer2", "Score2","Answer3", "Score3", "Answer4", "Score4"])
  n = 0
  messages = []
  for i in range(len(Questions)):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + str(
          get_access_token())
    n=n+1
    message=Questions[i]
    result_llm_llama_2_70b=chat_comp.do(model="Llama-2-70b-chat", messages=[{
    "role": "user",
    "content": message
    }])

    result_llm_ERNIE_Bot=chat_comp.do(model="ERNIE-Bot", messages=[{
    "role": "user",
    "content": message
    }])

    result_llm_ERNIE_Bot_turbo40=chat_comp.do(model="ERNIE-Bot-4", messages=[{
    "role": "user",
    "content": message
    }])

    result_llm_Qianfan_Chinese_Llama_2_7B=chat_comp.do(model="Qianfan-Chinese-Llama-2-7B", messages=[{
    "role": "user",
    "content": message
    }])

    df2 = pd.DataFrame([{"Question": Questions[i], "Correct_Answer": Answers[i],
                         "Answer1": result_llm_llama_2_70b['result'],"Score1": final_score(Questions[i], result_llm_llama_2_70b['result'], Answers[i]),
                         "Answer2": result_llm_ERNIE_Bot['result'],"Score2": final_score(Questions[i], result_llm_ERNIE_Bot['result'], Answers[i]),
                         "Answer3": result_llm_ERNIE_Bot_turbo40['result'],"Score3": final_score(Questions[i], result_llm_ERNIE_Bot_turbo40['result'], Answers[i]),
                         "Answer4": result_llm_Qianfan_Chinese_Llama_2_7B['result'],"Score4": final_score(Questions[i], result_llm_Qianfan_Chinese_Llama_2_7B['result'],Answers[i])}])

    print("No of Question", i + 1, "\n", "Right_Answer:", Answers[i],
          "\n" + "Answer_from_llama_2_70b_with_local_knowledge:",
          str(result_llm_llama_2_70b['result']).strip().replace("\n", ""),
          "\n" + "Answer_from_ERNIE_Bot_with_local_knowledge:",
          str(result_llm_ERNIE_Bot['result']).strip().replace("\n", ""),
          "\n" + "Answer_from_ERNIE_Bot_turbo40_with_local_knowledge:",
          str(result_llm_ERNIE_Bot_turbo40['result']).strip().replace("\n", ""),
          "\n" + "Answer_from_Qianfan_Chinese_Llama_2_7B:",
          str(result_llm_Qianfan_Chinese_Llama_2_7B['result']).strip().replace("\n", ""))
    df = pd.concat([df, df2], axis=0)
  save_df_to_excel(df, "Answer_from_original_ERNIE-Bot_ERNIE-Bot 4.0_Qianfan-Chinese-Llama-2-7B_Llama-2-70B-Chat" + year + ".xlsx", "sheet1")