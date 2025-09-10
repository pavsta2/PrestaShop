#!/bin/sh
set +e

. .venv/bin/activate

ALLURE_RESULTS="${ALLURE_RESULTS:-/root/Presta/allure-results}"
mkdir -p $ALLURE_RESULTS

echo "=== Запускается Pytest ==="

pytest --browser="$BROWSER" \
      --log_level="$LOG_LEVEL" \
      --browser_ver="$BROWSER_VER" \
      --numprocesses="$XDIST" \
      --remote_start \
      --remote_url="$REMOTE_URL" \
      --alluredir="$ALLURE_RESULTS" \
      --clean-alluredir \
      --api_key="$PS_API_KEY" \
      --api_url="$PS_API_URL"

chmod -R 777 $ALLURE_RESULTS