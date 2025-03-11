import pandas as pd
import re
import os
import time
import requests
from deep_translator import GoogleTranslator  # pip install deep-translator

# 텍스트 정제 함수
def clean_text(text):
    """
    특수기호 제거, 링크 제거 등의 전처리를 수행하는 함수
    """
    # 문자열이 아닌 경우 빈 문자열 반환
    if not isinstance(text, str):
        return ""
    
    # URL 패턴 제거 (http, https, www 등으로 시작하는 링크)
    cleaned = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # 트위터 사용자명(@username) 제거
    cleaned = re.sub(r'@\w+', '', cleaned)
    
    # 이모티콘과 이모지 제거
    cleaned = re.sub(r'[:;]-?[)D(P]', '', cleaned)
    
    # 특수문자 제거 (알파벳, 숫자, 한글, 공백 제외)
    cleaned = re.sub(r'[^\w\s가-힣]', ' ', cleaned)
    
    # 여러 공백을 하나로 통합
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    return cleaned

# deep-translator 라이브러리를 사용한 Google 번역
def translate_with_deep_translator(text, source='en', target='ko', max_length=5000):
    """
    deep-translator 라이브러리를 사용하여 텍스트를 번역하는 함수
    
    Args:
        text (str): 번역할 텍스트
        source (str): 원본 언어 코드 (기본값: 'en')
        target (str): 대상 언어 코드 (기본값: 'ko')
        max_length (int): 한 번에 번역할 최대 텍스트 길이
        
    Returns:
        str: 번역된 텍스트
    """
    try:
        # 빈 텍스트는 그대로 반환
        if not text or not text.strip():
            return text
        
        # 텍스트가 최대 길이를 초과하는 경우, 분할하여 번역
        if len(text) > max_length:
            parts = [text[i:i+max_length] for i in range(0, len(text), max_length)]
            translated_parts = []
            
            for part in parts:
                translator = GoogleTranslator(source=source, target=target)
                translated_part = translator.translate(part)
                translated_parts.append(translated_part)
                time.sleep(0.5)  # API 요청 제한 방지를 위한 딜레이
                
            return ' '.join(translated_parts)
        else:
            translator = GoogleTranslator(source=source, target=target)
            return translator.translate(text)
    except Exception as e:
        print(f"번역 오류: {e}")
        return f"[번역 오류] {text}"

# Papago API 사용 (네이버 개발자 계정 필요)
def translate_with_papago(text, client_id, client_secret, source='en', target='ko'):
    """
    네이버 Papago API를 사용하여 텍스트를 번역하는 함수
    
    Args:
        text (str): 번역할 텍스트
        client_id (str): 네이버 개발자 센터에서 발급받은 클라이언트 ID
        client_secret (str): 네이버 개발자 센터에서 발급받은 클라이언트 시크릿
        source (str): 원본 언어 코드 (기본값: 'en')
        target (str): 대상 언어 코드 (기본값: 'ko')
        
    Returns:
        str: 번역된 텍스트
    """
    try:
        # 빈 텍스트는 그대로 반환
        if not text or not text.strip():
            return text
        
        url = "https://openapi.naver.com/v1/papago/n2mt"
        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "source": source,
            "target": target,
            "text": text
        }
        
        response = requests.post(url, headers=headers, data=data)
        result = response.json()
        
        if response.status_code == 200:
            return result["message"]["result"]["translatedText"]
        else:
            print(f"Papago 번역 오류: {result}")
            return f"[번역 오류] {text}"
    except Exception as e:
        print(f"Papago 번역 오류: {e}")
        return f"[번역 오류] {text}"

# 메인 처리 함수 - deep-translator 사용
def process_with_deep_translator(input_path, output_path, batch_size=50):
    """
    CSV 파일을 읽어서 deep-translator로 번역하고 결과를 저장하는 함수
    
    Args:
        input_path (str): 입력 CSV 파일 경로
        output_path (str): 출력 CSV 파일 경로
        batch_size (int): 한 번에 처리할 데이터 수 (API 속도 제한 대응)
    """
    # CSV 파일 읽기
    df = pd.read_csv(input_path)
    
    # text 열이 있는지 확인
    if 'text' not in df.columns:
        print("Error: 'text' 열이 파일에 없습니다.")
        return
    
    # 원본 텍스트 저장
    df['original_text'] = df['text']
    
    # 텍스트 정제
    print("텍스트 정제 중...")
    df['cleaned_text'] = df['text'].apply(clean_text)
    
    # 번역 진행
    print("Google Translate(deep-translator)로 번역 중...")
    
    # 메모리 효율성을 위해 배치 처리
    translations = []
    total_rows = len(df)
    
    for i in range(0, total_rows, batch_size):
        end_idx = min(i + batch_size, total_rows)
        batch = df['cleaned_text'][i:end_idx]
        
        print(f"배치 번역 중: {i+1}~{end_idx}/{total_rows}")
        
        batch_translations = []
        for text in batch:
            translated = translate_with_deep_translator(text)
            batch_translations.append(translated)
            # API 요청 제한 방지를 위한 딜레이
            time.sleep(0.5)
        
        translations.extend(batch_translations)
    
    df['korean_translation'] = translations
    
    # 결과 저장
    df.to_csv(output_path, index=False, encoding='utf-8-sig')  # 한글 깨짐 방지를 위한 인코딩
    print(f"처리 완료: {output_path}에 저장되었습니다.")
    
    # 처리된 데이터의 처음 5개 행 반환
    return df.head()

# 실행 예시
if __name__ == "__main__":
    # 입력 파일 경로를 실제 파일 위치로 변경
    input_file = "/Users/isejin/Desktop/세진 폴더/SKN_Family_project1/LLM/03_vector_db/data/sentiment.csv"  # 실제 파일 경로로 수정
    output_file = "/Users/isejin/Desktop/세진 폴더/SKN_Family_project1/LLM/03_vector_db/data/sentiment_trans.csv"  # 출력 파일 경로도 같은 디렉토리에 저장
    
    # deep-translator 라이브러리 사용
    process_with_deep_translator(input_file, output_file)

    # Papago API 사용 (네이버 개발자 계정 필요)
    # CLIENT_ID = "네이버 개발자 센터에서 발급받은 클라이언트 ID"
    # CLIENT_SECRET = "네이버 개발자 센터에서 발급받은 클라이언트 시크릿"
    # process_with_papago(input_file, output_file, CLIENT_ID, CLIENT_SECRET)