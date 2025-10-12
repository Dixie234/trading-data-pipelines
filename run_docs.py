import subprocess
import sys

commands = [
    ["dbt", "docs", "generate"],
    ["dbt", "docs", "serve", "--port", "8080", "--no-browser", "--host", "0.0.0.0"],
]

for cmd in commands:
    print(f"Running: {' '.join(cmd)}", flush=True)
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)