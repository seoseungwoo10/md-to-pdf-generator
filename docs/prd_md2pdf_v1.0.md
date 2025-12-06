# PRD: Markdown to PDF Converter

## 1. 프로젝트 개요

### 1.1 목적
Markdown 파일을 고품질 PDF 문서로 변환하는 Python 기반 CLI 도구 개발

### 1.2 주요 목표
- Markdown 문법을 완벽하게 지원하는 PDF 변환
- 사용자 친화적인 명령줄 인터페이스 제공
- Windows 환경에서 즉시 실행 가능한 EXE 파일 배포 (GTK3 런타임 포함)
- 단일 파일 및 대량 변환 모두 지원

## 2. 기술 스택

### 2.1 개발 언어 및 프레임워크
- **언어**: Python 3.10+
- **주요 라이브러리**:
  - `markdown`: Markdown 파싱
  - `weasyprint`: HTML to PDF 변환 (xhtml2pdf 대체)
  - `click`: CLI 인터페이스
  - `pygments`: 코드 하이라이팅
  - `jinja2`: HTML 템플릿 렌더링
  - `matplotlib`: 수식(LaTeX) 이미지 렌더링

### 2.2 패키징
- **도구**: PyInstaller
- **목표**: 단일 실행 파일(.exe) 생성
- **배포**: GTK3 런타임 및 Fontconfig 설정 번들링으로 외부 의존성 최소화

## 3. 핵심 기능 요구사항

### 3.1 단일 파일 변환
```bash
md2pdf convert input.md -o output.pdf
```

**기능 상세**:
- 단일 Markdown 파일을 PDF로 변환
- 출력 경로 지정 옵션 (`-o`, `--output`)
- 출력 경로 미지정 시 입력 파일과 동일한 위치에 같은 이름으로 PDF 생성
- 파일 존재 시 덮어쓰기 확인 옵션

### 3.2 디렉토리 일괄 변환
```bash
md2pdf batch-convert ./source_dir -o ./output_dir
```

**기능 상세**:
- 지정된 디렉토리의 모든 `.md` 파일 변환
- 재귀적 검색 옵션 (`-r`, `--recursive`)
- 하위 디렉토리 구조 유지
- 변환 진행 상황 표시 (프로그레스 바)
- 실패한 파일 목록 보고
- 병렬 처리 지원 (Windows Multiprocessing 호환)

### 3.3 스타일 커스터마이징
```bash
md2pdf convert input.md -o output.pdf --style dark --font-size 12
```

**기능 상세**:
- 사전 정의된 테마 (light, dark, github, minimal)
- 커스텀 CSS 파일 지원 (`--css custom.css`)
- 폰트 크기 조정 옵션
- 페이지 여백 설정
- 용지 크기 선택 (A4, Letter, Legal)

### 3.4 Markdown 확장 기능
- **기본 지원**:
  - 제목, 목록, 인용구
  - 코드 블록 (구문 강조 포함)
  - 표(Table)
  - 이미지 (상대/절대 경로, URL)
  - 링크
  
- **확장 지원**:
  - GitHub Flavored Markdown (GFM)
  - 수식 지원 (LaTeX): `matplotlib`를 사용하여 이미지로 렌더링
    - 인라인 수식: `\( ... \)`
    - 블록 수식: `\[ ... \]`
    - 화폐 기호(`$`)와의 충돌 방지를 위해 `smart_dollar` 비활성화
  - 작업 목록 (Task lists)
  - 각주 (Footnotes)
  - 목차 자동 생성 옵션 (`--toc`, 기본값: False)

### 3.5 메타데이터 지원
```yaml
---
title: 문서 제목
author: 작성자
date: 2025-12-05
---
```

**기능 상세**:
- YAML Front Matter 파싱
- PDF 메타데이터에 반영
- 헤더/푸터에 표시 옵션

### 3.6 이미지 처리
- 로컬 이미지 자동 임베드
- 상대 경로 자동 해석
- URL 이미지 다운로드 및 포함
- 이미지 크기 자동 조정
- 깨진 이미지 처리 (경고 표시)

### 3.7 로깅 및 디버깅
```bash
md2pdf convert input.md --verbose
md2pdf convert input.md --log debug.log
```

**기능 상세**:
- Verbose 모드 (`-v`, `--verbose`)
- 로그 파일 저장 옵션
- 에러 상세 정보 출력
- 변환 통계 (처리 시간, 파일 수)

### 3.8 설정 파일 지원
```yaml
# md2pdf.config.yaml
default_style: github
font_size: 11
page_size: A4
recursive: true
toc: false
```

**기능 상세**:
- 프로젝트별 설정 파일 (`.md2pdf.yaml`)
- 전역 설정 지원
- CLI 옵션이 설정 파일보다 우선

## 4. CLI 인터페이스 설계

### 4.1 명령어 구조
```
md2pdf [COMMAND] [OPTIONS] [ARGUMENTS]
```

### 4.2 주요 명령어

#### 4.2.1 convert (단일 파일 변환)
```bash
md2pdf convert <input_file> [OPTIONS]

옵션:
  -o, --output PATH          출력 PDF 파일 경로
  -s, --style THEME          스타일 테마 (light|dark|github|minimal)
  --css PATH                 커스텀 CSS 파일
  --font-size INTEGER        폰트 크기 (기본: 11)
  --page-size SIZE           용지 크기 (A4|Letter|Legal)
  --toc                      목차 생성 (기본: False)
  --no-confirm               덮어쓰기 확인 생략
  -v, --verbose              상세 출력
```

#### 4.2.2 batch-convert (일괄 변환)
```bash
md2pdf batch-convert <input_dir> [OPTIONS]

옵션:
  -o, --output PATH          출력 디렉토리
  -r, --recursive            하위 디렉토리 포함
  --pattern GLOB             파일 패턴 (기본: *.md)
  -s, --style THEME          스타일 테마
  --css PATH                 커스텀 CSS 파일
  --parallel INTEGER         병렬 처리 수 (기본: CPU 코어 수)
  --continue-on-error        에러 발생 시 계속 진행
  -v, --verbose              상세 출력
```

#### 4.2.3 init (설정 파일 생성)
```bash
md2pdf init [OPTIONS]

옵션:
  --global                   전역 설정 파일 생성
  --template TEMPLATE        템플릿 선택
```

#### 4.2.4 list-styles (스타일 목록)
```bash
md2pdf list-styles

사전 정의된 스타일 테마 목록 출력
```

#### 4.2.5 version (버전 정보)
```bash
md2pdf --version
```

## 5. 비기능적 요구사항

### 5.1 성능
- 단일 파일 변환: 1MB 문서 기준 5초 이내
- 병렬 처리: CPU 코어 수에 따라 자동 조정 (ProcessPoolExecutor)
- 메모리 효율: 대용량 파일 스트리밍 처리

### 5.2 품질
- 한글 폰트 완벽 지원 (Noto Sans KR, Malgun Gothic fallback)
- 코드 블록 구문 강조 정확도 99%+
- 수식 렌더링 정확도 (Matplotlib 기반)
- 이미지 해상도 유지

### 5.3 사용성
- 직관적인 에러 메시지
- 진행 상황 시각화 (프로그레스 바)
- 도움말 자동 생성 (`--help`)

### 5.4 호환성
- Windows 10/11 지원
- Python 3.10 이상
- 외부 의존성(GTK3) 포함 단일 실행 파일

## 6. 프로젝트 구조

```
md-to-pdf-generator/
├── src/
│   ├── __init__.py
│   ├── cli.py                 # CLI 진입점
│   ├── converter.py           # 핵심 변환 로직
│   ├── parser.py              # Markdown 파싱
│   ├── renderer.py            # HTML to PDF 렌더링 (WeasyPrint)
│   ├── math_renderer.py       # 수식 렌더링 (Matplotlib)
│   ├── styles.py              # 스타일 관리
│   ├── config.py              # 설정 관리
│   ├── utils.py               # 유틸리티 함수
│   └── extensions/
│       └── math_img.py        # Markdown 수식 확장
├── templates/
│   ├── default.html           # 기본 HTML 템플릿
│   └── styles/
│       ├── light.css
│       ├── dark.css
│       ├── github.css
│       └── minimal.css
├── fonts/
│   └── NotoSansKR/            # 한글 폰트
├── tests/
│   ├── test_converter.py
│   ├── test_parser.py
│   ├── test_math.py
│   └── fixtures/              # 테스트 데이터
├── docs/
│   ├── README.md
│   ├── USAGE.md
│   ├── DEVELOPMENT.md
│   └── setup_gtk3_windows.md
├── .md2pdf.example.yaml       # 설정 파일 예제
├── requirements.txt
├── setup.py
├── md2pdf.spec                # PyInstaller 설정
├── md2pdf.py                  # 실행 파일 진입점
├── fonts.conf                 # Fontconfig 설정
└── README.md
```

## 7. 개발 로드맵

### Phase 1: 핵심 기능
- [x] 기본 Markdown to PDF 변환
- [x] CLI 인터페이스 구현
- [x] 단일 파일 변환 기능
- [x] 기본 스타일 적용

### Phase 2: 확장 기능
- [x] 디렉토리 일괄 변환
- [x] 다중 스타일 테마
- [x] 이미지 처리
- [x] 메타데이터 지원

### Phase 3: 고급 기능
- [x] 코드 구문 강조
- [x] 수식 지원 (Matplotlib + WeasyPrint)
- [x] 목차 자동 생성 (옵션화)
- [x] 설정 파일 지원

### Phase 4: 최적화 및 배포
- [x] 성능 최적화
- [x] 병렬 처리 (Windows 호환성 확보)
- [x] PyInstaller 패키징 (GTK3 번들링)
- [x] 문서 작성

### Phase 5: 테스트 및 배포
- [x] 단위 테스트 작성
- [x] 통합 테스트
- [x] 사용자 테스트 (피드백 반영 완료)
- [ ] 릴리스 준비

## 8. 품질 보증

### 8.1 테스트 전략
- 단위 테스트: 90% 이상 커버리지
- 통합 테스트: 주요 시나리오 검증
- 회귀 테스트: 자동화된 테스트 스위트

### 8.2 테스트 케이스
1. **Markdown 파싱**
   - 모든 Markdown 요소 정확한 파싱
   - GFM 확장 기능 지원
   - 깨진 문법 처리
   - 화폐 기호($)와 수식 구분

2. **PDF 변환**
   - 레이아웃 정확도
   - 한글 폰트 렌더링 (본문 및 수식)
   - 이미지 품질

3. **CLI 인터페이스**
   - 모든 옵션 조합 테스트
   - 에러 처리 (Fontconfig, DLL 로드 등)
   - 도움말 정확성

## 9. 릴리스 계획

### 9.1 버전 관리
- Semantic Versioning (MAJOR.MINOR.PATCH)
- v1.0.0: 초기 릴리스 (모든 핵심 기능)
- v1.1.0: 추가 테마 및 최적화
- v1.2.0: 커뮤니티 피드백 반영

### 9.2 배포 채널
- GitHub Releases
- EXE 파일 직접 다운로드
- (선택) PyPI 패키지 등록

## 10. 성공 지표

1. **기능 완성도**: 모든 핵심 기능 구현
2. **성능**: 1MB 문서 5초 이내 변환
3. **품질**: 테스트 커버리지 90% 이상
4. **사용성**: 첫 실행 성공률 95% 이상
5. **안정성**: 크래시 발생률 1% 미만

## 11. 위험 요소 및 대응

| 위험 | 영향 | 대응 방안 |
|------|------|-----------|
| 폰트 라이선스 문제 | 높음 | 오픈소스 폰트 사용 (Noto Sans) |
| PDF 렌더링 품질 | 중간 | WeasyPrint 도입으로 개선 |
| EXE 파일 크기 과대 | 낮음 | UPX 압축, 불필요한 의존성 제거 (필요시) |
| 플랫폼 호환성 | 중간 | Windows 우선 (GTK3 번들링), 추후 확장 고려 |

## 12. 참고 자료

- [Python-Markdown Documentation](https://python-markdown.github.io/)
- [WeasyPrint Documentation](https://weasyprint.org/)
- [PyInstaller Manual](https://pyinstaller.readthedocs.io/)
- [GitHub Flavored Markdown Spec](https://github.github.com/gfm/)

---

**문서 버전**: 1.1
**작성일**: 2025-12-05
**최종 수정일**: 2025-12-06
