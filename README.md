# Streamlit OpenAI 챗봇

`gpt-4o-mini`를 사용하는 간단한 한국어 챗봇입니다.

## Streamlit Community Cloud 배포

1. 이 폴더를 GitHub 저장소에 올립니다.
2. Streamlit Community Cloud에서 저장소와 `app.py`를 선택합니다.
3. 앱의 **Settings → Secrets**에 아래 내용을 등록합니다.

```toml
OPENAI_API_KEY = "sk-여기에-API-키"
```

API 키는 소스 코드나 GitHub 저장소에 직접 넣지 마세요.

## 로컬 실행

```bash
pip install -r requirements.txt
streamlit run app.py
```

PowerShell에서는 실행 전에 다음처럼 환경 변수로도 테스트할 수 있습니다.

```powershell
$env:OPENAI_API_KEY = "sk-여기에-API-키"
streamlit run app.py
```
