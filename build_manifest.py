#!/usr/bin/env python3
"""
生成 data_manifest.json：将同一批数据文件绑定为一个版本。

用法：
  cd /Users/ly/WorkBuddy/2026-07-27-23-31-38/output
  python3 build_manifest.py

输出：data/data_manifest.json

遵循需求文档 3.2 节定义的 schema。
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
DOWNLOADS_DIR = ROOT / "downloads"

# 文件清单（key 必须与需求文档 3.2 节一致）
# path 统一相对于网站根（index.html 所在目录），前端校验时直接用 "./" + path
FILES = {
    "history":     "data/snpx_spot_history.json",
    "types":       "data/snpx_spot_types.json",
    "windSolar":   "data/wechat_wind_solar_prices.json",
    "snapshot":    "data/data_snapshot.json",
    "quality":     "data/snpx_quality_checks.json",
    "differences": "data/snpx_source_discrepancies.json",
    "changes":     "data/snpx_run_changes.json",
}
WORKBOOK_REL = "downloads/陕西现货市场每日出清价格跟踪_2025至今_含风光分项.xlsx"
WORKBOOK_ABS = DOWNLOADS_DIR / "陕西现货市场每日出清价格跟踪_2025至今_含风光分项.xlsx"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    files_entry = {}
    for key, rel in FILES.items():
        p = ROOT / rel
        if not p.exists():
            raise FileNotFoundError(f"缺失关键数据文件：{p}")
        files_entry[key] = {"path": rel, "sha256": sha256(p)}

    if not WORKBOOK_ABS.exists():
        raise FileNotFoundError(f"缺失 Excel 文件：{WORKBOOK_ABS}")
    files_entry["workbook"] = {"path": WORKBOOK_REL, "sha256": sha256(WORKBOOK_ABS)}

    # 从 snapshot 读取元数据（不写死）
    snap = load_json(DATA_DIR / "data_snapshot.json")
    latest_trading = snap.get("latestTradingDate")
    latest_wind_solar = snap.get("latestWindSolarDate")
    quality_gate = snap.get("qualityGate")

    # latestCompleteDate：所有必需数据都已通过质量检查的共同最新日
    # = min(latestTradingDate, latestWindSolarDate)（ISO 日期字符串可直接比较）
    latest_complete = None
    if latest_trading and latest_wind_solar:
        latest_complete = min(latest_trading, latest_wind_solar)

    # datasetVersion 用 git commit 号（若在 git 仓库中）或生成时间
    dataset_version = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    try:
        import subprocess
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(ROOT), capture_output=True, text=True, timeout=5
        )
        if out.returncode == 0:
            dataset_version = out.stdout.strip()
    except Exception:
        pass

    manifest = {
        "schemaVersion": "1.0",
        "datasetVersion": dataset_version,
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "files": files_entry,
        "latestTradingDate": latest_trading,
        "latestWindSolarDate": latest_wind_solar,
        "latestCompleteDate": latest_complete,
        "qualityGate": quality_gate,
    }

    out_path = DATA_DIR / "data_manifest.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"已生成 {out_path}")
    print(f"  datasetVersion: {dataset_version}")
    print(f"  latestTradingDate: {latest_trading}")
    print(f"  latestWindSolarDate: {latest_wind_solar}")
    print(f"  latestCompleteDate: {latest_complete}")
    print(f"  qualityGate: {quality_gate}")
    print(f"  files: {len(files_entry)} 个")
    for k, v in files_entry.items():
        print(f"    {k}: {v['path']} ({v['sha256'][:12]}...)")


if __name__ == "__main__":
    main()
