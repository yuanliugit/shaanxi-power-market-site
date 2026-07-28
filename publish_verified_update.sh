#!/bin/zsh
set -euo pipefail

site_root="/Users/ly/.codex/.chatgpt-projects/g-p-6a662011fd208191a478f322f4d45a52/site"
publish_root="/Users/ly/WorkBuddy/2026-07-27-23-31-38/output"
workbook_name="陕西现货市场每日出清价格跟踪_2025至今_含风光分项.xlsx"

npm --prefix "$site_root" run sync:data
npm --prefix "$site_root" test

if cmp -s "$site_root/public/data/snpx_spot_history.json" "$publish_root/data/snpx_spot_history.json" \
  && cmp -s "$site_root/public/data/wechat_wind_solar_prices.json" "$publish_root/data/wechat_wind_solar_prices.json" \
  && cmp -s "$site_root/public/downloads/$workbook_name" "$publish_root/downloads/$workbook_name"; then
  print "No verified data or workbook changes; skipping Git deployment."
  exit 0
fi

python3 "$publish_root/build_html.py"

latest_date="$(
  node -e '
    const fs = require("fs");
    const snapshot = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
    process.stdout.write(snapshot.latestTradingDate);
  ' "$publish_root/data/data_snapshot.json"
)"

git -C "$publish_root" add \
  index.html \
  data \
  downloads \
  "$workbook_name"

if git -C "$publish_root" diff --cached --quiet; then
  print "Generated site is unchanged; skipping Git deployment."
  exit 0
fi

git -C "$publish_root" commit -m "Update verified market data through $latest_date"
git -C "$publish_root" push origin main
