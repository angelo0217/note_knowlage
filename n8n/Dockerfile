FROM n8nio/n8n:1.97.1

USER root

# 安裝 Python 和 pip
# 確保每個續行符號 `\` 後面都沒有任何內容，包括註解或空格。
# 註解必須獨立一行。
RUN apk add --no-cache \
    python3 \
    py3-pip \
    # 根據你的需求添加其他必要的系統依賴
    # 如果不需要這些編譯工具，請將整行刪除或保持註解
    build-base \
    g++ \
    libffi-dev \
    openssl-dev

# 創建一個 Python 虛擬環境（可選但推薦，保持環境乾淨）
RUN python3 -m venv /opt/venv

# 激活虛擬環境並安裝你的 Python 套件
# 在此替換為你實際需要的套件名稱
# 確保每個續行符號 `\` 後面都沒有任何內容，包括註解或空格。
RUN /opt/venv/bin/pip install --no-cache-dir \
    redis==5.3.0 \
    pandas \
    requests \
    langchain \
    langchain-community \
    langchain-text-splitters \
    langchain-ollama

# Create the custom directory and set ownership before installing npm packages
RUN mkdir -p /home/node/.n8n/custom && chown -R node:node /home/node/.n8n

# Switch to the node user to run npm install in the custom directory
USER node

RUN cd /home/node/.n8n/custom && npm install redis@^4.0.0 @langchain/redis @langchain/core @langchain/openai @langchain/ollama
# 將虛擬環境的路徑添加到 PATH，這樣 n8n 的 Python 節點就能找到它
ENV PATH="/opt/venv/bin:$PATH"

USER node
