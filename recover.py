import json

log_file = r"C:\Users\MELİH TEMEL\.gemini\antigravity\brain\a00c9593-3943-4c1d-962b-131fc689b738\.system_generated\logs\transcript.jsonl"
found_app = ""
try:
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            tool_calls = data.get("tool_calls", [])
            for call in tool_calls:
                name = call.get("name")
                if name == "default_api:write_to_file":
                    args = call.get("arguments", {})
                    target = args.get("TargetFile", "")
                    if target.endswith("app.py"):
                        found_app = args.get("CodeContent", "")
except Exception as e:
    print(e)

if found_app:
    print("Found app.py in logs. Length:", len(found_app))
    with open(r"C:\Users\MELİH TEMEL\Desktop\BİDB_ARSİV\app_recovered.py", "w", encoding="utf-8") as out:
        out.write(found_app)
else:
    print("Not found.")
