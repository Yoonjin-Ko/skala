
# 실무형 데이터 수집·검증·품질 파이프라인

## 프로젝트 개요

외부 API 데이터를 비동기로 수집하고, 데이터 스키마 검증 및 품질 관리를 거친 뒤 CSV/Parquet 형태로 저장하는 미니 ETL 파이프라인 프로젝트입니다.

API 수집 → 데이터 정제 → 스키마 검증 → DataFrame 변환 → 저장 → 성능 비교

과정을 직접 구현했습니다.

---

## 개발 목적

- 외부 API 데이터 수집 자동화 경험
- 비동기 HTTP 요청 처리 경험
- Pydantic 기반 데이터 검증 경험
- 데이터 품질 관리 흐름 이해
- CSV와 Parquet 저장 방식 비교

---

## 사용 기술

| Library | Purpose |
|---------|---------|
| asyncio | 비동기 처리 |
| httpx | Async HTTP Client |
| pandas | 데이터 처리 및 저장 |
| pydantic | 데이터 스키마 검증 |
| pyarrow | Parquet 저장 |
| pytest | 테스트 코드 |
| ruff | 코드 스타일 검사 |

---

## 구현 기능

### 1. 비동기 API 데이터 수집

`asyncio`와 `httpx.AsyncClient`를 활용하여 3개 API를 동시에 호출했습니다.

**수집 데이터:**

- **Weather API** (Open-Meteo)
  - 위도, 경도, 현재 온도, 강수 확률

- **Country API** (Countries.dev)
  - 국가명, 수도, 인구

- **IP API** (ip-api.com)
  - 국가, 도시, Timezone

### 2. 데이터 스키마 검증

Pydantic BaseModel을 활용하여 API 응답 데이터의 품질을 검증했습니다.

```python
class WeatherSchema(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    temperature: float = Field(ge=-100, le=60)
    precipitation_probability: int = Field(ge=0, le=100)
```

**검증 항목:**
- 위도/경도 범위 확인
- 온도 정상 범위 확인
- 강수 확률 0~100 검증
- 필수 데이터 존재 여부 확인

### 3. 데이터 저장

검증 완료된 데이터는 pandas DataFrame으로 변환 후 저장합니다.

| 형식 | 장점 | 단점 |
|------|------|------|
| CSV | 사람이 읽기 쉬움, 호환성 우수 | 파일 크기가 큼, 대규모 비효율 |
| Parquet | 컬럼 기반 저장, 압축 효율 우수 | 사람이 직접 읽기 어려움 |

---

## 성능 측정 결과

### 측정 환경
- Python 3.10+
- pandas 2.x
- pyarrow 14.x

### 측정 결과

| 행 수 | CSV 쓰기 | CSV 읽기 | Parquet 쓰기 | Parquet 읽기 |
|-------|----------|----------|--------------|--------------|
| 100 | 0.003s | 0.024s | 0.005s | 0.028s |
| 1,000 | 0.010s | 0.029s | 0.010s | 0.025s |
| 10,000 | 0.077s | 0.044s | 0.037s | 0.026s |
| 50,000 | 0.406s | 0.132s | 0.058s | 0.034s |

### 분석

**1. 소규모 데이터 (1,000행 이하)**
- CSV와 Parquet의 성능 차이가 거의 없음
- CSV가 사람이 읽기 쉬워 소규모 데이터에 적합

**2. 대규모 데이터 (10,000행 이상)**
- Parquet이 CSV보다 저장 속도 2~7배 빠름
- Parquet이 CSV보다 읽기 속도 4배 빠름
- Parquet의 압축 효율로 디스크 공간 절약 가능

**3. 읽기 성능**
- CSV: 데이터 크기에 비례해 읽기 시간 증가
- Parquet: 데이터 크기에 영향 적음 (컬럼 기반 저장)

### 결론

- **소규모 데이터**: CSV (가독성, 호환성)
- **대규모 데이터**: Parquet (속도, 압축, 효율성)
- **분석/ML 워크로드**: Parquet 권장

---

## 실행 방법

### 1. 가상환경 생성
```bash
python -m venv venv
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 실행
```bash
python pipeline.py
```

### 4. 테스트 실행 결과

```bash
$ pytest test_pipeline.py -v

============================= test session starts =============================
collected 6 items

test_pipeline.py::test_weather_success PASSED                           [ 16%]
test_pipeline.py::test_weather_boundary_values_pass PASSED              [ 33%]
test_pipeline.py::test_temperature_fail_upper PASSED                    [ 50%]
test_pipeline.py::test_temperature_fail_lower PASSED                    [ 66%]
test_pipeline.py::test_probability_fail PASSED                          [ 83%]
test_pipeline.py::test_latitude_fail PASSED                             [100%]

============================= 6 passed in 1.48s ==============================
```

### 5. 코드 스타일 검사 (ruff)
```bash
ruff check pipeline.py
ruff check test_pipeline.py
```
$ ruff check pipeline.py
All checks passed!
$ ruff check test_pipeline.py
All checks passed!


## 프로젝트 구조

```
project/
│
├── pipeline.py          # 메인 실행 코드
├── test_pipeline.py     # pytest 코드
├── requirements.txt     # 의존성 패키지
├── README.md            # 프로젝트 문서
│
└── data/
    ├── result.csv       # CSV 저장 결과
    └── result.parquet   # Parquet 저장 결과
```

---

## 배운 점

- API 데이터를 활용할 때는 검증 단계가 필요합니다.
- 비동기 처리는 여러 외부 I/O 작업에서 효율적인 방법입니다.
- 데이터가 커질수록 Parquet의 장점이 두드러집니다.
- CSV는 단순하고 보편적이지만, 대규모에서는 비효율적입니다.
- 상황에 맞게 CSV와 Parquet을 선택해야 합니다.

---

## 개선 예정

-모든 코드가 `pipeline.py` 하나에 몰려 있어서, 모듈을 분리할 필요성을 느꼈습니다.
-다음에는 다양한 ip주소를 넣어 테스트해보고 싶습니다.
-기술적인 문제가 많았는데 아직도 이해가 잘 안 가는 것들이 있어서 공부 후 더 깨끗한 코드를 만들어보겠습니다.
