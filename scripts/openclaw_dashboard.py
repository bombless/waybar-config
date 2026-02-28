#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
from datetime import datetime

BASE = 'http://127.0.0.1:8787'


def get_json(path: str, timeout: float = 1.2):
    with urllib.request.urlopen(BASE + path, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8', 'ignore'))


try:
    s = get_json('/api/usage/summary')
    ex = get_json('/api/exec/recent?limit=1')

    calls = int(s.get('total_calls') or 0)
    in_tok = int(s.get('total_input_tokens') or 0)
    out_tok = int(s.get('total_output_tokens') or 0)
    cost = float(s.get('total_cost_usd') or 0.0)

    last = (ex.get('items') or [{}])[0]
    cmd = (last.get('command') or '(none)').replace('\n', ' ')[:120]
    status = last.get('status') or '-'
    ts = last.get('ts')
    ts_text = '-'
    if ts:
        try:
            ts_text = datetime.fromtimestamp(ts / 1000).strftime('%m-%d %H:%M:%S')
        except Exception:
            pass

    text = f"󱚣 {calls}"
    tooltip = (
        f"OpenClaw Enhanced Dashboard\\n"
        f"Calls: {calls}\\n"
        f"Tokens: {in_tok}/{out_tok}\\n"
        f"Cost: ${cost:.4f}\\n"
        f"\\nLast exec: {status} @ {ts_text}\\n{cmd}"
    )

    print(json.dumps({
        'text': text,
        'tooltip': tooltip,
        'class': 'ok' if calls > 0 else 'idle'
    }, ensure_ascii=False))
except (urllib.error.URLError, TimeoutError, ConnectionError):
    print(json.dumps({
        'text': '󰅛 -',
        'tooltip': 'OpenClaw dashboard unavailable\\nhttp://127.0.0.1:8787',
        'class': 'down'
    }, ensure_ascii=False))
except Exception as e:
    print(json.dumps({
        'text': '󰅛 !',
        'tooltip': f'OpenClaw dashboard parse error: {e}',
        'class': 'down'
    }, ensure_ascii=False))
