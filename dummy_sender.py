name: Dummy test - send policy reminders

on:
  schedule:
    # TODAY ONLY (2 Nov): 13:07 UTC = 6:07 PM Pakistan time, 13:17 UTC = 6:17 PM
    - cron: "7 13 2 11 *"
    - cron: "17 13 2 11 *"
  workflow_dispatch:
    inputs:
      mode:
        description: "dry-run = only print | send-now = really send to Discord right now"
        type: choice
        options:
          - dry-run
          - send-now
        default: dry-run
      date:
        description: "Optional: pretend today is this date (YYYY-MM-DD), e.g. 2026-11-02"
        required: false
        default: ""

jobs:
  send:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install openpyxl
      - name: Run
        env:
          WEBHOOK_PRESTIGE: ${{ secrets.WEBHOOK_PRESTIGE }}
          SCHEDULE_TIME: ${{ github.event.schedule }}
          MODE: ${{ github.event.inputs.mode }}
          FAKE_DATE: ${{ github.event.inputs.date }}
        run: |
          ARGS=""
          if [ "$SCHEDULE_TIME" = "7 13 2 11 *" ]; then
            ARGS="--now --date 2026-11-02"     # 6:07 PM -> Monday, Week 1 policy
          elif [ "$SCHEDULE_TIME" = "17 13 2 11 *" ]; then
            ARGS="--now --date 2026-11-03"     # 6:17 PM -> Tuesday, Week 1 policy
          else
            if [ "$MODE" = "dry-run" ]; then ARGS="--dry-run"; fi
            if [ "$MODE" = "send-now" ]; then ARGS="--now"; fi
            if [ -n "$FAKE_DATE" ]; then ARGS="$ARGS --date $FAKE_DATE"; fi
          fi
          python dummy_sender.py $ARGS
