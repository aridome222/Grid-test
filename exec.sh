#!/bin/bash

# コンテナ内で実行するスクリプトのパス
SCRIPT_PATH="bin/test-serenium.py"

# コンテナの名前
CONTAINER_NAME="selenium-python-container"

# 環境変数でコンテナ内かどうかを判定
if grep -q docker /proc/1/cgroup; then
  # コンテナ内にいる場合はスクリプトのみ実行
  python3 "$SCRIPT_PATH"
else
  # コンテナ外にいる場合はコンテナに入り、スクリプトを実行
  docker exec -it "$CONTAINER_NAME" /bin/bash -c "python3 /$SCRIPT_PATH"
fi