from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


OUTPUT_DIR = Path("output")


def configure_chinese_font() -> None:
    """配置中文字体和负号显示。"""
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
    plt.rcParams["axes.unicode_minus"] = False


def generate_hospital_quality_chart(
    hospital_summary_df: pd.DataFrame,
) -> Path:
    """生成医院异常率排名柱状图。"""

    configure_chinese_font()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIR / "hospital_quality_ranking.png"

    plt.figure(figsize=(10, 6))
    plt.bar(
        hospital_summary_df["hospital_name"],
        hospital_summary_df["abnormal_rate"],
    )
    plt.title("医院患者数据异常率排名")
    plt.xlabel("医院")
    plt.ylabel("异常率（%）")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    return output_path


def generate_disease_category_chart(
    disease_category_df: pd.DataFrame,
) -> Path:
    """生成疾病分类患者分布柱状图。"""

    configure_chinese_font()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIR / "disease_category_distribution.png"

    plt.figure(figsize=(8, 5))
    plt.bar(
        disease_category_df["disease_category"],
        disease_category_df["patient_count"],
    )
    plt.title("疾病分类患者分布")
    plt.xlabel("疾病分类")
    plt.ylabel("患者人数")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    return output_path


def generate_drug_usage_chart(
    drug_usage_df: pd.DataFrame,
) -> Path:
    """生成药品使用患者分布柱状图。"""

    configure_chinese_font()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIR / "drug_usage_distribution.png"

    plt.figure(figsize=(11, 6))
    plt.bar(
        drug_usage_df["drug_name"],
        drug_usage_df["patient_count"],
    )
    plt.title("药品使用患者分布")
    plt.xlabel("药品名称")
    plt.ylabel("患者人数")
    plt.xticks(rotation=35)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    return output_path