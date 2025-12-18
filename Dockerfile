# Python 3.12 기반 이미지 사용
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치 (필요한 경우)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# pyproject.toml 복사 및 의존성 설치
COPY pyproject.toml . 

# pip 업그레이드 및 의존성 설치
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir . 

# 애플리케이션 소스 코드 복사
COPY . .

# FastAPI 기본 포트 노출
EXPOSE 8000

CMD ["uvicorn", "keywords:app", "--host", "0.0.0.0", "--port", "8000"]