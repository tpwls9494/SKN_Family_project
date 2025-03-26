import os
import glob
import re
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain_community.llms import Ollama
from typing import List, Optional, Tuple
from langchain.prompts import PromptTemplate

pdf_directory = "./pdf"
txt_directory = "./txt"

documents = []

pdf_files = glob.glob(os.path.join(pdf_directory, "*.pdf"))
print(f"{len(pdf_files)}개의 PDF 파일을 발견했습니다.")

for pdf_file in pdf_files:
    loader = PyPDFLoader(pdf_file)
    documents.extend(loader.load())

txt_files = glob.glob(os.path.join(txt_directory, "*.txt"))
print(f"{len(txt_files)}개의 TXT 파일을 발견했습니다.")

for txt_file in txt_files:
    loader = TextLoader(txt_file, encoding='utf-8')  # 한글 인코딩 지원
    documents.extend(loader.load())
print(f"총 {len(documents)}개의 문서 로드 완료")

def clean_text(text: str) -> str:
    text = text.replace('\xa0', ' ')
    text = re.sub(r'http\S+', '', text)             # url 제거
    text = re.sub(r'\s+', ' ', text)                # 긴여백 제거
    text = re.sub(r'[^\w\s.,!?()\[\]{}가-힣A-Za-z0-9]', '', text)  #특수문자 제거
    return text.strip()


for i, doc in enumerate(documents):
    cleaned_content = clean_text(doc.page_content)
    documents[i].page_content = cleaned_content
    print(doc.metadata['source'],'|',documents[i].page_content)

# 확인 결과
# 1. 이미지로만 이뤄진 pdf는 제목만 뽑히고 내용은 없어서 삭제(홍콩을 여행할 때 알아둘 점.pdf, 기내반입절차 포스터(영문포함)_배포용.pdf)    
# 2. 띄어쓰기 엉망인 친구들 삭제 ([미국생활 꿀팁] 한국과 다른 미국 생활 미리 알면 삶이 쉬워진다_.pdf, 운송제한 물품│아시아나항공.pdf)
# 3. 띄어씌가 '제목'만 이상한 놈 (싱가포르 여행 시 주의사항, 반드시 알아두자!.pdf)