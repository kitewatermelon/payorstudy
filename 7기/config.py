MEMBER = ['박연수', '김건영','권세한', '박지은', '송호석', '이신후', '이준수', '임혁규']
START_DATE = '2024-05-15'
END_DATE = '2024-06-28'

pattern_set = r'\d{4}\s?\w+\s?설정' # 설정 정규식
pattern_success = r'\d{4}\s?\w+\s?성공' # 성공 정규식
pattern_fail = r'\d{4}\s?\w+\s?실패' # 실패 정규식
pattern_off = r'\d{4}\s?\w+\s?.*?\s?off' # off 정규식
pattern_offs = r'\d{4}-\d{4}\s?\w+\s?.*?\s?off' # offs 정규식
pattern_retry_set = r'\d{4}\s?\w+\s?\d{4}\s?재도전' # 재도전 설정 정규식
pattern_retry_sucess = r'\d{4}\s?\w+\s?\d{4}\s?재성공' # 재도전 인증 정규식
pattern_time = r'\d{4}\s?'


박연수_벌금 = sum([0]) 
권세한_벌금 = sum([0])
김건영_벌금 = sum([0])
박지은_벌금 = sum([0])
박하은_벌금 = sum([0])
손하진_벌금 = sum([0])
송호석_벌금 = sum([0])
이신후_벌금 = sum([0])
이준수_벌금 = sum([0])
임혁규_벌금 = sum([0])