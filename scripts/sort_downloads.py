"""
sort_downloads.py - 將從 Google Drive 下載的簡報 PDF 自動歸類至對應分組資料夾

使用方式:
    python scripts/sort_downloads.py --src ./downloads --dest .

它會掃描 --src 目錄中的所有 PDF，依檔名關鍵字配對到正確的 Group 資料夾。
無法配對的檔案會列出供手動處理。
"""

import argparse
import shutil
from pathlib import Path

# 關鍵字 → 分組資料夾對應表
# 可依實際簡報檔名調整關鍵字
GROUP_KEYWORDS: dict[str, list[str]] = {
    "Group1_Weather_Climate_Prediction": ["氣候預報", "天氣預報模型", "climate prediction", "weather model", "NWP"],
    "Group2_Marine_Climate_Tech": ["海象", "海洋", "marine", "ocean", "海氣"],
    "Group3_Warning_Forecasting": ["預警", "warning", "forecasting", "劇烈天氣"],
    "Group4_Earthquake_Warning": ["地震", "earthquake", "seismic", "震源"],
    "Group5_Weather_Monitoring": ["監測", "monitoring", "觀測", "衛星", "雷達"],
    "Group7_IT_OpenSource": ["資訊系統", "開源", "open source", "IT", "HPC", "容器"],
    "Group8_AI_Talent_Cultivation": ["人才培育", "talent", "教育", "培訓", "人工智慧基礎"],
    "Group9_Data_Integration_Reconstruction": ["資料整集", "重建", "data integration", "reconstruction", "品管"],
}


def find_matching_group(filename: str) -> str | None:
    name_lower = filename.lower()
    for group, keywords in GROUP_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in name_lower:
                return group
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="將下載的簡報 PDF 歸類至分組資料夾")
    parser.add_argument("--src", type=str, default="./downloads", help="下載檔案所在目錄")
    parser.add_argument("--dest", type=str, default=".", help="專案根目錄（含 Group* 資料夾）")
    parser.add_argument("--dry-run", action="store_true", help="僅顯示配對結果，不實際移動檔案")
    args = parser.parse_args()

    src_dir = Path(args.src)
    dest_dir = Path(args.dest)

    if not src_dir.exists():
        print(f"錯誤: 來源目錄不存在 → {src_dir}")
        return

    pdf_files = list(src_dir.rglob("*.pdf")) + list(src_dir.rglob("*.pptx")) + list(src_dir.rglob("*.ppt"))
    if not pdf_files:
        print(f"在 {src_dir} 中找不到任何 PDF/PPT 檔案")
        return

    matched = []
    unmatched = []

    for f in pdf_files:
        group = find_matching_group(f.name)
        if group:
            matched.append((f, group))
        else:
            unmatched.append(f)

    print(f"\n=== 配對結果 ===")
    print(f"已配對: {len(matched)} 個檔案")
    print(f"未配對: {len(unmatched)} 個檔案\n")

    for f, group in matched:
        target = dest_dir / group / "raw_data" / f.name
        print(f"  ✓ {f.name} → {group}/raw_data/")
        if not args.dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(f), str(target))

    if unmatched:
        print(f"\n⚠ 以下檔案無法自動配對，請手動歸類:")
        for f in unmatched:
            print(f"  ? {f.name}")

    if args.dry_run:
        print("\n(--dry-run 模式，未實際移動檔案)")
    else:
        print("\n✅ 歸類完成！")


if __name__ == "__main__":
    main()
