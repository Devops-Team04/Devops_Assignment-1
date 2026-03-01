<div align="center">

# 📱 Mobile Test Automation Framework
### Tasks.org Android App · Appium + Pytest + GitHub Actions

![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python&logoColor=white)
![Appium](https://img.shields.io/badge/Appium-3.2.0-purple?style=for-the-badge&logo=appium&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-8.1.1-red?style=for-the-badge&logo=pytest&logoColor=white)
![Android](https://img.shields.io/badge/Android-UiAutomator2-green?style=for-the-badge&logo=android&logoColor=white)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-black?style=for-the-badge&logo=github-actions&logoColor=white)

</div>

---

## 📖 Project Overview

A fully automated **Mobile Test Automation Framework** built from scratch for the [Tasks.org](https://tasks.org) open-source Android to-do app. The framework follows the **Page Object Model (POM)** design pattern, ensuring clean separation between test logic and UI locators. Every test is fully independent and can be executed locally or via a CI pipeline.

```
📦 Assignment 1
├── 🧪 10 independent test cases
├── 🏗️  Page Object Model architecture
├── ⚙️  GitHub Actions CI pipeline
└── 📊 Auto-generated HTML test reports
```

---

## 🛠️ Tools & Technologies

| Layer | Tool | Version | Purpose |
|---|---|---|---|
| **Language** | Python | 3.14.2 | Test scripting |
| **Test Runner** | Pytest | 8.1.1 | Test execution & reporting |
| **Mobile Driver** | Appium | 3.2.0 | Android automation server |
| **Python Client** | Appium-Python-Client | 3.1.0 | Appium Python bindings |
| **Android Driver** | UiAutomator2 | 7.0.0 | Native Android UI interaction |
| **Web Driver** | Selenium | 4.19.0 | WebDriver protocol base |
| **Reports** | pytest-html | 4.1.1 | HTML test report generation |
| **CI** | GitHub Actions | — | Automated pipeline |
| **UI Inspector** | Appium Inspector | — | Locator discovery from XML dumps |

---

## 🏗️ Project Structure

```
📦 Assignment 1
 ┣ 📂 pages/                    ← Page Object Model classes
 ┃ ┣ 📄 base_page.py            ← Shared Appium actions (parent class)
 ┃ ┣ 📄 home_page.py            ← Home screen (FAB, sidebar, search)
 ┃ ┣ 📄 task_page.py            ← Add/Edit task screen
 ┃ ┣ 📄 sidebar_page.py         ← Navigation drawer
 ┃ ┣ 📂 xml/                    ← Appium Inspector UI dumps
 ┃ ┃ ┣ 📄 home.xml
 ┃ ┃ ┣ 📄 addTask.xml
 ┃ ┃ ┗ 📄 hamburger_sidebar.xml
 ┃ ┗ 📄 __init__.py
 ┣ 📂 tests/                    ← One file per test case
 ┃ ┣ 📄 test_TC01_home_title.py
 ┃ ┣ 📄 test_TC02_fab_visible.py
 ┃ ┣ 📄 test_TC03_add_task.py
 ┃ ┣ 📄 test_TC04_add_task_with_description.py
 ┃ ┣ 📄 test_TC05_open_sidebar.py
 ┃ ┣ 📄 test_TC06_sidebar_today.py
 ┃ ┣ 📄 test_TC07_sidebar_filters.py
 ┃ ┣ 📄 test_TC08_search_button.py
 ┃ ┣ 📄 test_TC09_default_no_due_date.py
 ┃ ┗ 📄 test_TC10_sidebar_default_list.py
 ┣ 📂 demo/                     ← Proof-of-concept tests (do not modify)
 ┣ 📂 reports/                  ← Auto-generated HTML reports
 ┣ 📄 conftest.py               ← Pytest fixtures & Appium driver setup
 ┣ 📄 pytest.ini                ← Pytest configuration
 ┣ 📄 requirements.txt          ← Python dependencies
 ┗ 📄 .github/workflows/main.yml ← CI pipeline definition
```

---

## ⚙️ Setup Instructions

### Prerequisites

Make sure the following are installed before proceeding:

- ✅ **Python 3.10+** — [python.org](https://www.python.org/downloads/)
- ✅ **Node.js 18+** — [nodejs.org](https://nodejs.org/)
- ✅ **Android SDK** with `platform-tools` in PATH — [Android Studio](https://developer.android.com/studio)
- ✅ **Java JDK 11+**
- ✅ **Android Emulator** running (e.g. Pixel 6, API 33+)
- ✅ **Tasks.org APK** installed on the emulator

### Step 1 — Clone the repository

```bash
git clone https://github.com/Devops-Team04/Devops_Assignment-1.git
cd "Devops_Assignment-1"
```

### Step 2 — Create and activate a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### Step 3 — Install Python dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Install Appium server and UiAutomator2 driver

```bash
npm install -g appium
appium driver install uiautomator2
```

### Step 5 — Set Android environment variables (Windows)

```powershell
setx ANDROID_HOME "C:\Users\<YourUser>\AppData\Local\Android\Sdk" /M
setx PATH "%PATH%;%ANDROID_HOME%\platform-tools" /M
```
> Restart your terminal after setting these.

### Step 6 — Verify device is connected

```bash
adb devices
# Should show: emulator-5554   device
```

---

## ▶️ How to Run Tests Locally

### Start the Appium server (keep this terminal open)

```bash
appium
```

### Run all 10 tests

```bash
pytest
```

### Run a specific test file

```bash
pytest tests/test_TC03_add_task.py -v
```

### Run with live logs visible

```bash
pytest -v --tb=short
```

### View HTML report (auto-generated after each run)

```
reports/report.html
```

---

## 🧪 Test Cases

| # | Test File | What It Verifies |
|---|---|---|
| TC01 | `test_TC01_home_title.py` | Home screen shows "My Tasks" title |
| TC02 | `test_TC02_fab_visible.py` | FAB "Create new task" button is visible |
| TC03 | `test_TC03_add_task.py` | A task can be added and appears in the list |
| TC04 | `test_TC04_add_task_with_description.py` | A task with a description saves correctly |
| TC05 | `test_TC05_open_sidebar.py` | Hamburger opens the navigation drawer |
| TC06 | `test_TC06_sidebar_today.py` | Sidebar contains "Today" option |
| TC07 | `test_TC07_sidebar_filters.py` | Sidebar contains "Filters" option |
| TC08 | `test_TC08_search_button.py` | Search button is visible and tappable |
| TC09 | `test_TC09_default_no_due_date.py` | New task form defaults to "No due date" |
| TC10 | `test_TC10_sidebar_default_list.py` | Sidebar contains "Default list" option |

---

## 🔄 CI Workflow Explanation

The pipeline is defined in `.github/workflows/main.yml` and runs automatically on every **push** or **pull request** to `main`.

```
┌─────────────────────────────────────────────────┐
│               GitHub Actions Pipeline           │
├─────────────────────────────────────────────────┤
│  1. Checkout code                               │
│  2. Set up Python 3.11                          │
│  3. Install Python dependencies (requirements)  │
│  4. Install Appium server (npm)                 │
│  5. Install UiAutomator2 driver                 │
│  6. Start Android emulator                      │
│  7. Wait for emulator to boot                   │
│  8. Install Tasks.org APK                       │
│  9. Start Appium server                         │
│  10. Run pytest (all 10 test cases)             │
│  11. Upload HTML report as artifact             │
└─────────────────────────────────────────────────┘
```

---

## 🌿 Git Workflow

This project follows a **feature branch workflow**:

```
main
 ├── feat/POM_Foundation         ← POM classes (BasePage, HomePage, etc.)
 ├── feat/home_                  ← TC01 to TC05
 ├── feat/SideBar_test_cases     ← TC06 to TC10
 ├── feat/ci-pipeline            ← GitHub Actions workflow
 └── feat/others                 ← 4 mores
```

### Rules
- ❌ Never commit directly to `main`
- ✅ All work happens on feature branches
- ✅ Branches are merged via **Pull Requests** only
- ✅ **Pull Requests** are Accepted at least after reviewing by one reviewer
- ✅ Each commit message follows the format:
  ```
  feat: <short description + plus Issue ID> ||
  fix: <short description + plus Issue ID>  ||
  chore: <short description + plus Issue ID>
  ```

---

<div align="center">

All Rights Reserved 

</div>
