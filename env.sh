#!/bin/sh

# FIXME: dialogflow api v1
export DIALOGFLOW_CLIENT_ACCESS_TOKEN="your token"
export DIALOGFLOW_DEVELOPER_ACCESS_TOKEN="your token"
export DIALOGFLOW_WEB_DEMO_URL="your url"
export JUPYTER_NOTEBOOK_TOKEN="hellopython"  # Jupyter Login 암호

# etc
export LC_ALL="ko_KR.UTF-8"
alias python="python3"
alias pip="pip3"

echo "loaded."
