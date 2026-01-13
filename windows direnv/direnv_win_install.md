# Windows 環境下 direnv 安裝與設定指南

本指南說明如何在 Windows 環境中手動安裝 `direnv`，並配置 Git Bash 以自動載入環境變數。

## 1. 下載與安裝

1.  **下載執行檔**：
    前往 [direnv releases](https://github.com/direnv/direnv/releases) 下載適用於 Windows 的執行檔（通常是 `direnv.windows-amd64.exe`）。
2.  **重新命名與存局**：
    將下載的檔案重新命名為 `direnv.exe`。
3.  **放置目錄**：
    將 `direnv.exe` 移動到您習慣的工具目錄，例如 `C:\tools`。

## 2. 設定環境變數

為了讓系統能找到 `direnv` 指令，需要將存放目錄加入系統路徑。建議使用環境變數來管理路徑，以便日後維護。

### 方法一：透過使用者介面設定 (推薦)

1.  開啟「編輯系統環境變數」或「編輯您的帳戶的環境變數」。
2.  **新增使用者變數** (User Variable)：
    *   變數名稱 (`Variable name`): `DIRENV_BIN` (建議使用此名稱以區別於設定檔路徑，原筆記使用 `DIRENV_CONFIG`)
    *   變數值 (`Variable value`): `C:\tools`
3.  **編輯 Path 變數**：
    *   找到 `Path` 變數並編輯。
    *   新增一筆紀錄：`%DIRENV_BIN%`

### 方法二：透過 PowerShell 設定

```powershell
[System.Environment]::SetEnvironmentVariable("DIRENV_BIN", "C:\tools", "User")
# 注意：直接修改 Path 較為複雜，建議手動添加或確認 Path 中已包含 C:\tools
```

> **注意**：原筆記中使用 `DIRENV_CONFIG` 作為目錄變數，這可能會與 direnv 自身的配置路徑變數混淆。建議僅將 `C:\tools` 加入 `Path` 或使用非保留字的變數名稱（如 `TOOLS_HOME` 或 `DIRENV_BIN`）。

## 3. 設定 Shell Hook

配置 Git Bash 以便在進入目錄時自動觸發 `direnv`。

1.  開啟 **Git Bash**。
2.  編輯 `.bashrc` 設定檔：
    ```bash
    vi ~/.bashrc
    ```
3.  在檔案末端加入以下內容：
    ```bash
    eval "$(direnv hook bash)"
    ```
4.  儲存並離開 (`:wq`)。
5.  重新載入設定檔或重啟 Git Bash：
    ```bash
    source ~/.bashrc
    ```

## 4. 驗證與使用

*   **驗證安裝**：
    ```bash
    direnv version
    ```
*   **基本使用**：
    在專案目錄下建立 `.envrc` 檔案：
    ```bash
    echo export TEST_VAR=hello > .envrc
    direnv allow
    echo $TEST_VAR
    # 輸出應為 hello
    ```

## 常見問題

*   **如果不設定 `.bashrc`**：
    若未設定 Hook，每次開啟 Shell 都需要手動執行 `eval "$(direnv hook bash)"` 才能啟用自動載入功能。
