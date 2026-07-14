from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


OUTPUT_DIR = Path("output")


def build_kpi_dataframe(
    overall_kpi: dict[str, Any],
) -> pd.DataFrame:
    """将 KPI 字典转换成适合 Excel 展示的表格。"""

    kpi_name_mapping = {
        "total_patient": "患者总人数",
        "abnormal_patient": "异常患者人数",
        "patient_quality_rate": "患者数据质量率（%）",
        "diagnosis_abnormal_count": "异常诊断记录数",
        "medication_abnormal_count": "异常用药记录数",
    }

    return pd.DataFrame(
        [
            {
                "指标名称": kpi_name_mapping.get(key, key),
                "指标值": value,
            }
            for key, value in overall_kpi.items()
        ]
    )


def export_analysis_report(
    overall_kpi: dict[str, Any],
    patient_quality_df: pd.DataFrame,
    diagnosis_quality_df: pd.DataFrame,
    medication_quality_df: pd.DataFrame,
    medical_wide_df: pd.DataFrame,
    hospital_summary_df: pd.DataFrame,
    disease_category_df: pd.DataFrame,
    drug_usage_df: pd.DataFrame,
) -> Path:
    """生成医学数据质量与运营分析 Excel 报告。"""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIR / "medical_data_analysis_report.xlsx"
    kpi_df = build_kpi_dataframe(overall_kpi)

    patient_abnormal_df = patient_quality_df[
        patient_quality_df["patient_quality_status"] == "异常"
    ]

    diagnosis_abnormal_df = diagnosis_quality_df[
        diagnosis_quality_df["diagnosis_quality_status"] != "正常"
    ]

    medication_abnormal_df = medication_quality_df[
        medication_quality_df["medication_quality_status"] != "正常"
    ]

    with pd.ExcelWriter(
        output_path,
        engine="openpyxl",
    ) as writer:
        kpi_df.to_excel(
            writer,
            sheet_name="总体KPI",
            index=False,
        )

        hospital_summary_df.to_excel(
            writer,
            sheet_name="医院质量排名",
            index=False,
        )

        disease_category_df.to_excel(
            writer,
            sheet_name="疾病分类统计",
            index=False,
        )

        drug_usage_df.to_excel(
            writer,
            sheet_name="用药统计",
            index=False,
        )

        patient_abnormal_df.to_excel(
            writer,
            sheet_name="患者异常明细",
            index=False,
        )

        diagnosis_abnormal_df.to_excel(
            writer,
            sheet_name="诊断异常明细",
            index=False,
        )

        medication_abnormal_df.to_excel(
            writer,
            sheet_name="用药异常明细",
            index=False,
        )

        medical_wide_df.to_excel(
            writer,
            sheet_name="医学宽表",
            index=False,
        )

    return output_path