import re
from datetime import datetime, timedelta
import pandas as pd
from config import *

def make_off_every_sunday():
    for idx, _ in 설정맵.iterrows():
        if idx.weekday() == 6:
            설정맵.loc[idx] = 'off'
            
def set_deadline(USER, line):
    if USER in ['권세한', '임혁규', '이신후', '이준수']:
        DEADLINE = 21
    elif 3 <= datetime.strptime(line, "%Y%m%d").month <= 6:
        DEADLINE = 11    
    else :
        DEADLINE = 10
        
    return DEADLINE

today = datetime.today() + timedelta(days=1)
date_rng = pd.date_range(start=START_DATE, end=END_DATE, freq='D')

# 데이터프레임 생성
설정맵 = pd.DataFrame(columns=MEMBER, index=date_rng)
벌금맵 = 설정맵
설정맵 = 설정맵.fillna("설정X")
벌금맵 = 벌금맵.fillna(0)

설정맵.loc['2024-02-19'] = '성공'
            
make_off_every_sunday()

file = pd.read_csv("6기.csv", encoding='UTF8')
def filter_msg(file):
    filter_option = f"{pattern_set}|{pattern_success}|{pattern_fail}|{pattern_off}|{pattern_offs}|{pattern_retry_set}|{pattern_retry_sucess}"
    filtered_rows = file[file['Message'].str.contains(filter_option, regex=True)]
    set_rows = file[file['Message'].str.contains(pattern_set, regex=True)].reset_index(drop=True, inplace=False)
    success_rows = file[file['Message'].str.contains(pattern_success, regex=True)].reset_index(drop=True, inplace=False)
    fail_rows = file[file['Message'].str.contains(pattern_fail, regex=True)].reset_index(drop=True, inplace=False)
    off_rows = file[file['Message'].str.contains(f'{pattern_off}|{pattern_offs}', regex=True)].reset_index(drop=True, inplace=False)
    retry_rows = file[file['Message'].str.contains(f'{pattern_retry_set}|{pattern_retry_sucess}', regex=True)].reset_index(drop=True, inplace=False)
    filtered_rows = filtered_rows.reset_index(drop=True, inplace=False)
    filtered_rows['Late'] = 'O'
    
    return filtered_rows, set_rows, success_rows, fail_rows, off_rows, retry_rows
# 지각 여부 확인
def check_late(df):
    i = 0
    for index in range(df.shape[0]):
        DATE = df['Date'][index]
        USER = df['User'][index]
        MESSAGE = df['Message'][index]
        LATE = df['Late'][index]

        result_set = str(re.findall(pattern_set, MESSAGE))[2:][:-2]
        result_retry_set = str(re.findall(pattern_retry_set, MESSAGE))[2:][:-2]

        result_success = str(re.findall(pattern_success, MESSAGE))[2:][:-2]
        result_retry_success = str(re.findall(pattern_retry_sucess, MESSAGE))[2:][:-2]
        result_fail = str(re.findall(pattern_fail, MESSAGE))[2:][:-2]
            
        time_str = DATE
        time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        
        if len(result_success) >= 1 | len(result_fail) >= 1 | len(result_retry_success) >= 1:
            if  len(result_retry_success) > 1:
                date_str_next = '2024' + result_retry_success[:4]
                
            elif len(result_fail) > 1:
                date_str_next = '2024' + result_fail[:4]
            
            else:
                date_str_next = '2024' + result_success[:4]

            DEADLINE = set_deadline(USER, date_str_next)
                
            date_obj_next = datetime.strptime(date_str_next + f'{DEADLINE}', "%Y%m%d%H") + timedelta(days=1)
            formatted_date_next = date_obj_next.strftime("%Y-%m-%d %H:%M:%S")
            time_difference_next = time_obj - datetime.strptime(formatted_date_next, "%Y-%m-%d %H:%M:%S")    
            date_str_next = date_obj_next.strftime("%Y-%m-%d")
            date_index_next = datetime.strptime(date_str_next, '%Y-%m-%d')
        
            if time_difference_next.days > 0 or (time_difference_next.days == 0 and time_difference_next.seconds >= 60):
                df['Late'][index] = '지각'
            
        
        elif len(result_set) >= 1 | len(result_retry_set) >= 1:
            if len(result_retry_set) > 1:
                date_str = '2024' + result_retry_set[:4]
            else:
                date_str = '2024' + result_set[:4]
                
            DEADLINE = set_deadline(USER, date_str)

            date_obj = datetime.strptime(date_str + f'{DEADLINE}', "%Y%m%d%H")
            formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
            time_difference = time_obj - datetime.strptime(formatted_date, "%Y-%m-%d %H:%M:%S")
            date_str = date_obj.strftime("%Y-%m-%d")
            date_index = datetime.strptime(date_str, '%Y-%m-%d')
        
            if time_difference.days > 0 or (time_difference.days == 0 and time_difference.seconds >= 60):
                df['Late'][index] = '지각'
                
    return df
                
# 1. msg에서 요소만 따오기
filtered_rows, set_rows, success_rows, fail_rows, off_rows, retry_rows = filter_msg(file)