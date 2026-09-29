from datetime import datetime, timezone
import os
import platform
from pathlib import Path
 
 
def file_state(name):
    return "present" if Path(name).exists() else "missing"
 
 
version_file = Path("VERSION")
version = (
    version_file.read_text(encoding="utf-8").strip()
    if version_file.exists()
    else "unknown"
)
 
lines = [
    "SUPPORT REPORT",
    f"created_utc={datetime.now(timezone.utc).isoformat()}",
    f"version={version}",
    f"python={platform.python_version()}",
    f"os={platform.system()} {platform.release()}",
    f"github_run_id={os.getenv('GITHUB_RUN_ID', 'local')}",
    f"github_sha={os.getenv('GITHUB_SHA', 'local')}",
    f"ruff_report={file_state('ruff-report.txt')}",
    f"test_results={file_state('test-results.xml')}",
    f"coverage_report={file_state('coverage.xml')}",
]
 
Path("support-report.txt").write_text(
    "\n".join(lines) + "\n",
    encoding="utf-8",
)
