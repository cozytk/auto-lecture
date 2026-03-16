# Session 0: 실습 환경 설정 가이드

**대상**: Windows / Linux 사용자 (macOS 참고 포함)
**소요 시간**: 수업 전 사전 설치 권장 (약 20~30분)

---

## 개요

이 문서는 TypeScript + React 수업에 필요한 개발 환경을 **처음부터** 설정하는 가이드입니다.
수업 당일에 환경 문제로 시간을 낭비하지 않도록, 아래 순서대로 **사전에 설치를 완료**해 주세요.

### 설치할 것 요약

| 순서 | 도구 | 용도 |
|------|------|------|
| 1 | **Node.js** (v18 이상) | JavaScript/TypeScript 실행 환경 + npm 패키지 관리자 |
| 2 | **tsx** | TypeScript 파일을 즉시 실행하는 도구 (수업 중 코드 실습용) |
| 3 | **VS Code** | 코드 편집기 |
| 4 | **VS Code 확장(Extensions)** | 개발 편의 도구 |
| 5 | **Git** (선택) | 버전 관리 + Windows에서 Git Bash 터미널 제공 |
| 6 | **Chrome** (권장) | 개발자 도구가 가장 강력한 브라우저 |

---

## 1. Node.js 설치

### Node.js란?

JavaScript는 원래 브라우저에서만 실행되는 언어였습니다. **Node.js**는 브라우저 밖(터미널, 서버)에서도 JavaScript를 실행할 수 있게 해주는 런타임입니다. React 개발에서는 직접 Node.js 코드를 작성하지는 않지만, 개발 도구(Vite, TypeScript 컴파일러 등)가 Node.js 위에서 동작하기 때문에 반드시 필요합니다.

Node.js를 설치하면 **npm**(Node Package Manager)이 함께 설치됩니다. npm은 React, TypeScript 등 수만 개의 오픈소스 패키지를 설치·관리하는 도구입니다.

### 먼저 확인: 이미 설치되어 있나요?

터미널을 열고 아래 명령어를 실행해 보세요:

```bash
node --version
npm --version
```

- **둘 다 버전이 출력되고, node가 v18 이상이면** → Node.js 설치를 건너뛰고 [2. tsx 설치](#2-tsx-설치)로 이동하세요.
- **node는 있지만 v18 미만이면** → 아래 "기존 환경과 버전 충돌 방지" 섹션을 참고하세요.
- **`command not found` 또는 아무 출력도 없으면** → 아래 설치 과정을 진행하세요.
- **node는 있는데 npm이 없으면** → 드문 경우이지만, Node.js를 재설치하면 npm이 함께 설치됩니다.

### 기존 환경과 버전 충돌 방지

이미 다른 프로젝트에서 Node.js를 사용하고 있다면, 버전을 함부로 바꾸면 기존 프로젝트가 깨질 수 있습니다. **nvm(Node Version Manager)** 을 사용하면 여러 버전을 설치해두고 프로젝트별로 전환할 수 있습니다.

> **권장**: 이미 Node.js가 설치되어 있는 환경이라면 nvm을 사용하세요. 새로 설치하는 분은 공식 설치 파일로 바로 설치해도 됩니다.

**Windows — nvm-windows:**

```powershell
# 1. https://github.com/coreybutler/nvm-windows/releases 에서 nvm-setup.exe 다운로드·설치
# 2. 터미널을 새로 열고:
nvm install 20       # Node.js 20.x LTS 설치
nvm use 20           # 이 수업에서 사용할 버전 활성화
node --version       # v20.x.x 확인
```

**Linux / macOS — nvm:**

```bash
# nvm 설치 (이미 있다면 생략)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc  # 또는 ~/.zshrc

# Node.js 20 설치 및 활성화
nvm install 20
nvm use 20
node --version    # v20.x.x 확인
```

> **수업 끝난 후 원래 버전으로 돌아가기**: `nvm use {원래버전}` (예: `nvm use 18`). `nvm ls`로 설치된 버전 목록을 확인할 수 있습니다.

### Windows (nvm 없이 새로 설치)

1. [https://nodejs.org](https://nodejs.org) 접속
2. **LTS (Long Term Support)** 버전 다운로드 (초록색 버튼)
   - "Current" 버전이 아닌 **LTS**를 선택합니다. LTS는 안정성이 검증된 버전입니다
3. 다운로드된 `.msi` 설치 파일 실행
4. 설치 마법사 진행:
   - **License Agreement**: "I accept" 체크 → Next
   - **Destination Folder**: 기본 경로 그대로 → Next
   - **Custom Setup**: 기본 설정 그대로 → Next
   - **Tools for Native Modules**: 체크하지 **않아도** 됩니다 → Next
     - 이 옵션은 C/C++ 네이티브 모듈 빌드에 필요한 도구인데, 이 수업에서는 사용하지 않습니다
   - Install → Finish

> **주의**: 설치 후 **이미 열려 있는 터미널(PowerShell, CMD)은 닫고 새로 열어야** 합니다. 환경 변수(PATH)가 새 터미널에서만 반영됩니다.

### Linux (Ubuntu/Debian 계열)

```bash
# NodeSource 저장소 추가 후 설치 (Node.js 20.x LTS 기준)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 설치 확인
node --version
npm --version
```

또는 **nvm**(Node Version Manager)을 사용하면 여러 Node.js 버전을 쉽게 관리할 수 있습니다:

```bash
# nvm 설치
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

# 터미널 재시작 후
nvm install --lts
nvm use --lts
```

### macOS 참고

Homebrew가 설치되어 있다면:

```bash
brew install node@20
```

또는 공식 사이트에서 macOS용 `.pkg` 설치 파일을 다운로드합니다.

### 설치 확인

터미널(Windows: PowerShell / Linux: Terminal)을 **새로** 열고 다음 명령어를 실행합니다:

```bash
node --version
# 출력 예: v20.11.0 (v18 이상이면 OK)

npm --version
# 출력 예: 10.2.4 (v9 이상이면 OK)
```

두 명령어 모두 버전 번호가 출력되면 설치 성공입니다.

#### 트러블슈팅: `node`를 찾을 수 없다고 나올 때

**Windows:**
```
'node'은(는) 내부 또는 외부 명령, 실행할 수 있는 프로그램, 또는
배치 파일이 아닙니다.
```

- 터미널을 **닫고 새로** 여세요 (환경 변수 반영)
- 그래도 안 되면: 시작 메뉴 → "환경 변수" 검색 → "시스템 환경 변수 편집" → 환경 변수 → Path에 `C:\Program Files\nodejs\`가 있는지 확인
- 없으면 "새로 만들기"로 추가 후 터미널 재시작

**Linux:**
```
command not found: node
```

- `nvm`으로 설치한 경우: `source ~/.bashrc` (또는 `~/.zshrc`) 실행 후 다시 시도
- 일부 Linux 배포판에서는 `nodejs` 명령어를 사용합니다: `sudo apt install nodejs npm`

---

## 2. tsx 설치 — TypeScript 즉시 실행 도구

### tsx란?

**tsx**는 TypeScript 파일을 **컴파일 없이 바로 실행**할 수 있게 해주는 도구입니다. 원래 TypeScript 코드는 `tsc`로 JavaScript로 변환한 뒤 `node`로 실행해야 하지만, tsx를 사용하면 `tsx hello.ts` 한 줄로 바로 실행됩니다.

수업 중에 TypeScript 문법을 배우면서 **VS Code 터미널에서 코드를 직접 실행해보는 용도**로 사용합니다.

### 설치

```bash
npm install -g tsx
```

> **`npm`이 없다고 나오면**: 1절의 Node.js 설치가 안 된 것입니다. Node.js를 먼저 설치하세요.

> **Linux에서 `EACCES` 권한 오류가 나오면**: 8절의 "문제 3" 해결 방법을 참고하거나, nvm으로 Node.js를 설치하면 권한 문제가 발생하지 않습니다.

### 설치 확인

```bash
tsx --version
# 출력 예: tsx v4.x.x
```

### 사용법 — VS Code에서 TypeScript 코드 즉시 실행

1. VS Code에서 아무 폴더를 열고, `hello.ts` 파일을 만듭니다:

```ts
// hello.ts
const greeting: string = "안녕하세요, TypeScript!";
const year: number = 2026;
console.log(`${greeting} (${year}년)`);
```

2. VS Code 터미널(`` Ctrl+` ``)을 열고 실행합니다:

```bash
tsx hello.ts
# 출력: 안녕하세요, TypeScript! (2026년)
```

3. 타입 오류가 있으면 **VS Code가 빨간 줄로 표시**하고, tsx 실행 시에도 오류가 발생합니다:

```ts
// error-example.ts
const age: number = "스물다섯";  // ← VS Code에서 빨간 줄!
```

```bash
tsx error-example.ts
# TypeError: 타입 오류 발생
```

> **수업 중 활용**: Session 1에서 TypeScript 문법을 배울 때, 슬라이드의 코드 예제를 직접 `.ts` 파일로 만들어 실행해보면 이해가 훨씬 빠릅니다. "이렇게 바꾸면 어떻게 될까?" 궁금하면 바로 수정해서 `tsx` 로 실행해 보세요.

---

## 3. VS Code 설치

### VS Code란?

Visual Studio Code(줄여서 VS Code)는 Microsoft가 만든 **무료 코드 편집기**입니다. TypeScript를 만든 회사가 만든 편집기이기 때문에 TypeScript 지원이 가장 뛰어납니다. 자동 완성, 오류 감지, 디버깅이 별도 설정 없이 바로 동작합니다.

> **참고**: "Visual Studio"와 "Visual Studio Code"는 다른 프로그램입니다.
> - **Visual Studio** = 대형 IDE (C#, .NET 개발용, 용량 수 GB)
> - **Visual Studio Code** = 경량 코드 편집기 (웹 개발에 최적, 용량 약 300MB)

### Windows

1. [https://code.visualstudio.com](https://code.visualstudio.com) 접속
2. "Download for Windows" 클릭 → `.exe` 파일 다운로드
3. 설치 마법사 진행:
   - **License Agreement**: 동의 → Next
   - **Select Additional Tasks** (중요!):
     - [x] **"Add to PATH"** — **반드시 체크**합니다. 터미널에서 `code .` 명령어로 VS Code를 열 수 있게 됩니다
     - [x] **"Register Code as an editor for supported file types"** — 체크 권장
     - [x] **"Add 'Open with Code' action to Windows Explorer file context menu"** — 체크 권장 (폴더 우클릭 메뉴에서 VS Code 열기 가능)
     - [x] **"Add 'Open with Code' action to Windows Explorer directory context menu"** — 체크 권장
   - Install → Finish

> **`code .` 명령어 설명**: 터미널에서 `code .`을 입력하면 **현재 폴더**를 VS Code로 바로 엽니다. `.`은 "현재 디렉토리"를 의미합니다. 수업 중에 자주 사용하는 명령어입니다.

### Linux (Ubuntu/Debian 계열)

```bash
# 방법 1: snap (가장 간단)
sudo snap install code --classic

# 방법 2: apt (Microsoft 저장소 추가)
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" | sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null
sudo apt update
sudo apt install code
```

### macOS 참고

```bash
brew install --cask visual-studio-code
```

또는 공식 사이트에서 `.zip`을 다운로드하고 Applications 폴더로 이동합니다.

터미널에서 `code` 명령어를 사용하려면: VS Code 실행 → `Cmd+Shift+P` → "Shell Command: Install 'code' command in PATH" 선택

### 설치 확인

터미널을 **새로** 열고:

```bash
code --version
# 출력 예:
# 1.96.2
# ...
```

버전 번호가 출력되면 성공입니다.

#### 트러블슈팅: `code` 명령어를 찾을 수 없을 때

**Windows:**
- 설치 시 "Add to PATH" 옵션을 놓쳤을 수 있습니다
- 해결: VS Code를 **제거 후 재설치**하면서 해당 옵션을 체크하거나, 수동으로 PATH에 추가합니다
  - 기본 경로: `C:\Users\{사용자이름}\AppData\Local\Programs\Microsoft VS Code\bin`

**Linux:**
- snap으로 설치한 경우 대부분 자동으로 PATH에 추가됩니다
- `which code` 명령어로 확인합니다

---

## 4. VS Code 기본 설정

### 4.1 한국어 언어 팩 (선택)

VS Code의 메뉴를 한국어로 바꿀 수 있습니다.

1. VS Code 실행
2. 왼쪽 사이드바에서 **확장(Extensions)** 아이콘 클릭 (네모 4개 모양, 또는 `Ctrl+Shift+X`)
3. 검색창에 `Korean Language Pack` 입력
4. **Korean Language Pack for Visual Studio Code** (Microsoft 제작) → Install
5. 우측 하단에 "Restart" 알림이 뜨면 클릭하여 VS Code 재시작

> **강사 참고**: 수업에서는 영문 메뉴 기준으로 설명합니다. 한국어 팩은 개인 선호에 따라 선택합니다. 영문 메뉴에 익숙해지면 해외 자료를 참고할 때 편합니다.

### 4.2 기본 터미널 설정 (Windows만 해당)

VS Code에는 터미널이 내장되어 있습니다. `` Ctrl+` `` (백틱, 키보드 숫자 1 왼쪽)을 누르면 하단에 터미널이 열립니다.

Windows에서 VS Code의 기본 터미널이 **CMD(명령 프롬프트)**로 되어 있을 수 있습니다. **PowerShell**로 변경하는 것을 권장합니다.

1. VS Code에서 `Ctrl+Shift+P` → 명령 팔레트 열기
2. `Terminal: Select Default Profile` 입력 → 선택
3. **PowerShell** 선택

> **CMD vs PowerShell**: CMD는 오래된 Windows 명령 프롬프트입니다. PowerShell은 CMD의 후속으로, 더 많은 기능을 제공합니다. `npm`, `node` 등의 명령어는 둘 다에서 동작하지만, 일부 Unix 스타일 명령어(`ls`, `cat` 등)는 PowerShell에서만 사용할 수 있습니다.

> **Git Bash 옵션**: Git을 설치하면(6절 참조) Git Bash도 터미널 목록에 나타납니다. Git Bash는 Linux/macOS의 Bash와 동일한 명령어를 제공하므로, Linux 명령어에 익숙하다면 Git Bash를 기본 터미널로 설정해도 좋습니다.

### 4.3 자동 저장 설정 (권장)

코드를 수정한 뒤 저장(`Ctrl+S`)을 깜빡하면, 개발 서버에 변경 사항이 반영되지 않아 혼란스러울 수 있습니다. 자동 저장을 켜두면 이 실수를 방지할 수 있습니다.

1. `Ctrl+,` (설정 열기)
2. 검색창에 `Auto Save` 입력
3. **Files: Auto Save** 항목을 `afterDelay`로 변경
4. **Files: Auto Save Delay** 항목은 기본값 `1000` (1초) 유지

또는 메뉴에서: File → Auto Save 체크

### 4.4 글꼴 크기 조정 (선택)

수업 중 프로젝터나 화면 공유 시 글자가 작게 보일 수 있습니다.

- **빠른 조정**: `Ctrl+` `+` (확대) / `Ctrl+` `-` (축소) / `Ctrl+0` (원래 크기)
- **설정에서 변경**: `Ctrl+,` → `Font Size` 검색 → 16~18px 권장 (기본값 14px)

---

## 5. VS Code 확장(Extensions) 설치

확장(Extension)은 VS Code에 기능을 추가하는 플러그인입니다. 아래 확장들을 미리 설치하면 수업 중 코딩이 훨씬 편해집니다.

### 확장 설치 방법

1. VS Code 왼쪽 사이드바 → **Extensions** 아이콘 (`Ctrl+Shift+X`)
2. 검색창에 확장 이름 입력
3. **Install** 클릭

### 필수 확장

| 확장 이름 | 설명 | 검색어 |
|-----------|------|--------|
| **ESLint** | JavaScript/TypeScript 코드 품질 검사. 잠재적 버그를 빨간 밑줄로 경고합니다 | `dbaeumer.vscode-eslint` |
| **Prettier - Code formatter** | 코드 자동 정렬 도구. 저장 시 들여쓰기·따옴표 등을 자동으로 통일합니다 | `esbenp.prettier-vscode` |

### 권장 확장

| 확장 이름 | 설명 | 검색어 |
|-----------|------|--------|
| **ES7+ React/Redux/React-Native snippets** | `rfc` → React 함수형 컴포넌트 자동 생성 등 코드 스니펫 | `dsznajder.es7-react-js-snippets` |
| **Auto Rename Tag** | HTML/JSX 태그 이름을 수정하면 닫는 태그도 자동으로 변경 | `formulahendry.auto-rename-tag` |
| **Error Lens** | 오류/경고 메시지를 코드 줄 옆에 직접 표시 (기본은 마우스를 올려야 보임) | `usernamehw.errorlens` |

### Prettier를 기본 포매터로 설정

Prettier를 설치한 뒤, 저장 시 자동으로 코드를 정리하도록 설정합니다.

1. `Ctrl+,` (설정 열기)
2. 검색창에 `Default Formatter` 입력
3. **Editor: Default Formatter** → `Prettier - Code formatter` 선택
4. 검색창에 `Format On Save` 입력
5. **Editor: Format On Save** → 체크

이렇게 설정하면 `Ctrl+S`로 저장할 때마다 코드가 자동으로 정리됩니다.

> **Format On Save가 동작하지 않을 때**:
> - VS Code 우측 하단 상태바에 `Prettier` 아이콘에 경고 표시(⚠)가 있는지 확인
> - `Ctrl+Shift+P` → `Format Document` 실행 시 "포매터가 설치되어 있지 않습니다" 메시지가 뜨면 Prettier 확장이 제대로 설치되었는지 재확인

---

## 6. Git 설치 (선택 사항)

이 수업에서 Git을 직접 사용하지는 않지만, 다음과 같은 이유로 설치를 권장합니다:

- Windows에서 **Git Bash** 터미널을 사용할 수 있음 (Linux/macOS와 동일한 명령어)
- VS Code의 소스 제어(Source Control) 기능 활용 가능
- 추후 팀 프로젝트에서 반드시 필요

### Windows

1. [https://git-scm.com/downloads/win](https://git-scm.com/downloads/win) 접속
2. **Standalone Installer** 다운로드 (64-bit)
3. 설치 마법사 진행:
   - 대부분 기본 설정 그대로 Next
   - **Choosing the default editor used by Git** 화면: **Use Visual Studio Code as Git's default editor** 선택
   - **Adjusting the name of the initial branch in new repositories**: `main` 선택 권장
   - 나머지는 기본값 유지 → Install → Finish

### Linux

대부분의 Linux 배포판에 Git이 기본 설치되어 있습니다.

```bash
# 설치 확인
git --version

# 없다면 설치
sudo apt install git     # Ubuntu/Debian
sudo dnf install git     # Fedora
```

### 설치 확인

```bash
git --version
# 출력 예: git version 2.43.0
```

---

## 7. Chrome 브라우저 (권장)

### 왜 Chrome인가?

React 개발 시 **Chrome 개발자 도구(DevTools)**를 자주 사용합니다. 특히:

- **Console 탭**: JavaScript 오류 확인, `console.log` 출력 확인
- **Elements 탭**: 렌더링된 HTML 구조 확인
- **Network 탭**: API 호출 확인 (종합 실습에서 사용)

Chrome이 이미 설치되어 있다면 추가 작업은 필요 없습니다.

> **다른 브라우저**: Edge, Firefox도 유사한 개발자 도구를 제공합니다. 수업은 Chrome 기준으로 진행하지만, 다른 브라우저를 사용해도 큰 문제는 없습니다.

### 개발자 도구 여는 법

- **단축키**: `F12` 또는 `Ctrl+Shift+I`
- **메뉴**: 브라우저 우측 상단 점 세 개(⋮) → 도구 더보기 → 개발자 도구

---

## 8. 전체 설치 확인 체크리스트

모든 설치가 끝났다면, 터미널을 **새로** 열고 아래 명령어를 순서대로 실행합니다.

```bash
node --version
# ✅ v18.0.0 이상

npm --version
# ✅ v9.0.0 이상

tsx --version
# ✅ 버전 번호 출력

code --version
# ✅ 버전 번호 출력

git --version
# ✅ (선택) 버전 번호 출력
```

### 최종 동작 테스트

설치가 모두 완료되었는지 확인하기 위해 간단한 테스트 프로젝트를 만들어 봅니다.

**Windows (PowerShell):**

```powershell
# 바탕화면에 테스트 폴더 생성
cd ~/Desktop
mkdir test-setup
cd test-setup

# Vite 프로젝트 생성
npm create vite@latest hello-react -- --template react-ts

# 프로젝트 폴더 이동 + 의존성 설치
cd hello-react
npm install

# 개발 서버 실행
npm run dev
```

**Linux / macOS:**

```bash
# 홈 디렉토리에 테스트 폴더 생성
cd ~
mkdir test-setup && cd test-setup

# Vite 프로젝트 생성
npm create vite@latest hello-react -- --template react-ts

# 프로젝트 폴더 이동 + 의존성 설치
cd hello-react
npm install

# 개발 서버 실행
npm run dev
```

터미널에 아래와 같이 출력되면 성공입니다:

```
  VITE v5.x.x  ready in 342 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

브라우저에서 `http://localhost:5173`에 접속하여 React 로고가 표시되면 **환경 설정 완료**입니다.

`Ctrl+C`를 눌러 개발 서버를 종료합니다.

> **테스트 폴더 정리**: 테스트가 끝나면 `test-setup` 폴더는 삭제해도 됩니다. 수업 당일에 새로 프로젝트를 만들 예정입니다.

---

## 9. 자주 발생하는 문제와 해결

### 문제 1: PowerShell에서 스크립트 실행 정책 오류 (Windows)

```
npm : 이 시스템에서 스크립트를 실행할 수 없으므로 ...
... 자세한 내용은 about_Execution_Policies ...
```

Windows의 기본 보안 정책이 PowerShell 스크립트 실행을 막고 있는 경우입니다.

**해결:**

1. **PowerShell을 관리자 권한으로 실행** (시작 메뉴 → PowerShell 우클릭 → "관리자 권한으로 실행")
2. 다음 명령어 입력:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. `Y`를 입력하여 확인
4. PowerShell을 닫고 다시 열기

> **설명**: `RemoteSigned`는 "로컬에서 만든 스크립트는 허용, 인터넷에서 다운로드한 스크립트는 서명이 있어야 허용"하는 정책입니다. 개발 환경에서 권장되는 설정입니다.

### 문제 2: `npm create vite@latest` 실행 시 프록시/방화벽 오류

```
npm ERR! network request to https://registry.npmjs.org/... failed
```

회사나 학교 네트워크에서 npm 레지스트리가 차단된 경우입니다.

**해결:**

```bash
# 프록시 설정 (프록시 주소는 IT 부서에 문의)
npm config set proxy http://프록시주소:포트
npm config set https-proxy http://프록시주소:포트

# 또는 레지스트리를 미러로 변경
npm config set registry https://registry.npmmirror.com
```

> **강사 참고**: 사전에 네트워크 환경을 확인하고, 문제가 예상되면 `npm install`까지 완료된 프로젝트를 USB나 공유 폴더로 배포하는 것이 가장 확실합니다.

### 문제 3: `npm install` 중 `EACCES` 권한 오류 (Linux)

```
npm ERR! Error: EACCES: permission denied
```

**해결:**

```bash
# 방법 1: npm 글로벌 디렉토리 권한 변경
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# 방법 2: nvm 사용 (권장 — 1절의 "기존 환경과 버전 충돌 방지" 참조)
# nvm으로 설치하면 권한 문제가 발생하지 않음
```

> **주의**: `sudo npm install`은 피해야 합니다. root 권한으로 설치하면 이후에 권한 충돌이 발생합니다.

### 문제 4: VS Code에서 터미널이 열리지 않음 (Windows)

**증상**: `` Ctrl+` ``을 눌러도 터미널이 열리지 않거나, 열렸다가 바로 닫힘

**해결:**

1. `Ctrl+Shift+P` → `Terminal: Select Default Profile` → **PowerShell** 선택
2. 그래도 안 되면: `Ctrl+,` → `terminal.integrated.defaultProfile.windows` 검색 → `PowerShell` 입력
3. VS Code 재시작

### 문제 5: 한글 경로 문제 (Windows)

**증상**: 프로젝트 경로에 한글이 포함되면 빌드 오류 또는 이상 동작

```
❌ C:\Users\홍길동\Desktop\my-react-app
✅ C:\Users\홍길동\Desktop\projects\my-react-app
```

**해결:**

- Windows 사용자 이름이 한글이면 경로에 한글이 포함됩니다
- 프로젝트 폴더를 한글이 없는 경로에 생성합니다: `C:\dev\my-react-app` 또는 `D:\projects\my-react-app`
- **새 폴더 이름도 영문**으로 만드세요

```powershell
# 한글이 없는 경로에 프로젝트 폴더 생성
mkdir C:\dev
cd C:\dev
npm create vite@latest my-react-app -- --template react-ts
```

### 문제 6: 포트 5173이 이미 사용 중

**증상**: `npm run dev` 실행 시 Vite가 다른 포트(5174, 5175...)를 사용하거나 오류 발생

**해결:**

- Vite는 기본적으로 다음 빈 포트를 자동 선택합니다 → 터미널 출력에서 실제 URL 확인
- 이전에 종료하지 않은 개발 서버가 있을 수 있습니다

```powershell
# Windows: 5173 포트를 사용 중인 프로세스 확인
netstat -ano | findstr :5173

# Linux/macOS:
lsof -i :5173
```

### 문제 7: VS Code에서 TypeScript 오류가 빨간줄로 안 보임

**증상**: 코드에 타입 오류가 있는데 VS Code에서 표시되지 않음

**확인 사항:**

1. VS Code 우측 하단 상태바에서 TypeScript 버전이 표시되는지 확인 (예: `TS 5.3.3`)
2. 표시되지 않으면: `Ctrl+Shift+P` → `TypeScript: Select TypeScript Version` → `Use Workspace Version` 선택
3. 프로젝트 폴더를 **VS Code로 직접 열었는지** 확인 (상위 폴더를 열면 TypeScript가 `tsconfig.json`을 찾지 못할 수 있음)

---

## 10. VS Code 핵심 단축키 (수업 중 자주 사용)

수업 중에 자주 사용하는 단축키입니다. 외울 필요 없이 수업 중 반복하면서 익히면 됩니다.

| 동작 | Windows / Linux | macOS |
|------|----------------|-------|
| **터미널 열기/닫기** | `` Ctrl+` `` | `` Cmd+` `` |
| **명령 팔레트** | `Ctrl+Shift+P` | `Cmd+Shift+P` |
| **파일 빠르게 열기** | `Ctrl+P` | `Cmd+P` |
| **저장** | `Ctrl+S` | `Cmd+S` |
| **전체 저장** | `Ctrl+K S` | `Cmd+Option+S` |
| **되돌리기 / 다시 실행** | `Ctrl+Z` / `Ctrl+Shift+Z` | `Cmd+Z` / `Cmd+Shift+Z` |
| **줄 복제** | `Shift+Alt+↓` | `Shift+Option+↓` |
| **줄 이동** | `Alt+↑` / `Alt+↓` | `Option+↑` / `Option+↓` |
| **줄 삭제** | `Ctrl+Shift+K` | `Cmd+Shift+K` |
| **코드 접기/펼치기** | `Ctrl+Shift+[` / `]` | `Cmd+Option+[` / `]` |
| **사이드바 토글** | `Ctrl+B` | `Cmd+B` |
| **확장 탭 열기** | `Ctrl+Shift+X` | `Cmd+Shift+X` |
| **설정 열기** | `Ctrl+,` | `Cmd+,` |
| **주석 토글** | `Ctrl+/` | `Cmd+/` |
| **여러 줄 선택 (멀티 커서)** | `Alt+클릭` | `Option+클릭` |
| **같은 단어 선택 추가** | `Ctrl+D` | `Cmd+D` |

> **팁**: `Ctrl+P`로 파일을 열 때 파일 이름 일부만 입력해도 됩니다. 예: `App` 입력 → `App.tsx` 바로 열기

---

## 마무리

위 과정을 모두 완료했다면 수업 준비가 끝난 것입니다. 수업 당일에는 바로 코딩을 시작할 수 있습니다.

**체크리스트 최종 확인:**

- [ ] Node.js v18 이상 설치 완료 (`node --version`)
- [ ] npm v9 이상 설치 완료 (`npm --version`)
- [ ] tsx 설치 완료 (`tsx --version`)
- [ ] VS Code 설치 완료 (`code --version`)
- [ ] VS Code 확장 설치: ESLint, Prettier
- [ ] Prettier를 기본 포매터로 설정 + Format On Save 활성화
- [ ] 테스트 프로젝트 생성 및 `npm run dev`로 브라우저 확인 완료

설치 중 문제가 발생하면 오류 메시지를 캡처하여 강사에게 공유해 주세요.
