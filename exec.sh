#!/bin/bash

# コンテナ内で実行するスクリプトのパス
SCRIPT_PATH="bin/test-serenium.py"

# コンテナの名前
CONTAINER_NAME="selenium-python-container"

# コンテナ外にいる場合はコンテナに入り、スクリプトを実行
docker exec -it "$CONTAINER_NAME" /bin/bash -c "python3 $SCRIPT_PATH"