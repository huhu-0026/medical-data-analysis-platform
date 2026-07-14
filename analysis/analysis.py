from __future__ import annotations

import pandas as pd


def build_medical_wide_table(
    patient_quality_df: pd.DataFrame,
    diagnosis_quality_df: pd.DataFrame,
    medication_quality_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    构建就诊粒度医学宽表。

    先将同一次就诊的多条诊断和多条用药分别聚合，
    再进行关联，避免诊断数 × 用药数产生笛卡尔积。
    """

    diagnosis_visit_df = (
        diagnosis_quality_df
        .groupby(
            ["patient_id", "visit_id"],
            dropna=False,
        )
        .agg(
            diagnosis_names=(
                "standard_disease_name",
                lambda values: "；".join(
                    sorted(
                        {
                            str(value)
                            for value in values.dropna()
                        }
                    )
                ),
            ),
            diagnosis_codes=(
                "diagnosis_code",
                lambda values: "；".join(
                    sorted(
                        {
                            str(value)
                            for value in values.dropna()
                        }
                    )
                ),
            ),
            disease_categories=(
                "disease_category",
                lambda values: "；".join(
                    sorted(
                        {
                            str(value)
                            for value in values.dropna()
                        }
                    )
                ),
            ),
            diagnosis_quality_status=(
                "diagnosis_quality_status",
                lambda values: (
                    "正常"
                    if (values == "正常").all()
                    else "；".join(
                        sorted(
                            {
                                str(value)
                                for value in values
                                if value != "正常"
                            }
                        )
                    )
                ),
            ),
        )
        .reset_index()
    )

    medication_visit_df = (
        medication_quality_df
        .groupby(
            ["patient_id", "visit_id"],
            dropna=False,
        )
        .agg(
            drug_names=(
                "drug_name",
                lambda values: "；".join(
                    sorted(
                        {
                            str(value)
                            for value in values.dropna()
                        }
                    )
                ),
            ),
            medication_quality_status=(
                "medication_quality_status",
                lambda values: (
                    "正常"
                    if (values == "正常").all()
                    else "；".join(
                        sorted(
                            {
                                str(value)
                                for value in values
                                if value != "正常"
                            }
                        )
                    )
                ),
            ),
        )
        .reset_index()
    )

    patient_diagnosis_df = pd.merge(
        patient_quality_df,
        diagnosis_visit_df,
        on="patient_id",
        how="left",
    )

    medical_wide_df = pd.merge(
        patient_diagnosis_df,
        medication_visit_df,
        on=["patient_id", "visit_id"],
        how="left",
    )

    return medical_wide_df


def calculate_overall_kpi(
    patient_quality_df: pd.DataFrame,
    diagnosis_quality_df: pd.DataFrame,
    medication_quality_df: pd.DataFrame,
) -> dict[str, int | float]:
    """计算总体数据质量 KPI。"""

    total_patient = patient_quality_df["patient_id"].nunique()

    abnormal_patient = patient_quality_df.loc[
        patient_quality_df["patient_quality_status"] == "异常",
        "patient_id",
    ].nunique()

    diagnosis_abnormal_count = (
        diagnosis_quality_df["diagnosis_quality_status"] != "正常"
    ).sum()

    medication_abnormal_count = (
        medication_quality_df["medication_quality_status"] != "正常"
    ).sum()

    patient_quality_rate = (
        round(
            (total_patient - abnormal_patient)
            / total_patient
            * 100,
            2,
        )
        if total_patient > 0
        else 0.0
    )

    return {
        "total_patient": total_patient,
        "abnormal_patient": abnormal_patient,
        "patient_quality_rate": patient_quality_rate,
        "diagnosis_abnormal_count": int(diagnosis_abnormal_count),
        "medication_abnormal_count": int(medication_abnormal_count),
    }


def analyze_hospital_quality(
    patient_quality_df: pd.DataFrame,
) -> pd.DataFrame:
    """按医院统计患者数据质量。"""

    hospital_summary = (
        patient_quality_df
        .groupby("hospital_name")
        .agg(
            total_patient=("patient_id", "nunique"),
            abnormal_patient=(
                "patient_quality_status",
                lambda values: (values == "异常").sum(),
            ),
        )
        .reset_index()
    )

    hospital_summary["abnormal_rate"] = (
        hospital_summary["abnormal_patient"]
        / hospital_summary["total_patient"]
        * 100
    ).round(2)

    return hospital_summary.sort_values(
        by="abnormal_rate",
        ascending=False,
    )


def analyze_disease_category(
    diagnosis_quality_df: pd.DataFrame,
) -> pd.DataFrame:
    """基于诊断明细统计疾病分类，避免宽表关联重复。"""

    return (
        diagnosis_quality_df[
            diagnosis_quality_df[
                "disease_category"
            ].notna()
        ]
        .groupby("disease_category")
        .agg(
            diagnosis_count=(
                "diagnosis_id",
                "count",
            ),
            patient_count=(
                "patient_id",
                "nunique",
            ),
        )
        .reset_index()
        .sort_values(
            by="patient_count",
            ascending=False,
        )
    )


def analyze_drug_usage(
    medication_quality_df: pd.DataFrame,
) -> pd.DataFrame:
    """基于用药明细统计药品使用情况。"""

    return (
        medication_quality_df[
            medication_quality_df["drug_name"].notna()
        ]
        .groupby("drug_name")
        .agg(
            medication_count=(
                "medication_id",
                "count",
            ),
            patient_count=(
                "patient_id",
                "nunique",
            ),
        )
        .reset_index()
        .sort_values(
            by="patient_count",
            ascending=False,
        )
    )