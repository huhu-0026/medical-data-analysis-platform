from __future__ import annotations

import pandas as pd


def check_patient_quality(df: pd.DataFrame) -> pd.DataFrame:
    """检查患者年龄和性别质量。"""

    result = df.copy()

    def check_age(row: pd.Series) -> str:
        age = row["age"]

        if pd.isna(age):
            return "年龄缺失"
        if age < 0:
            return "年龄小于0"
        if age > 120:
            return "年龄超出合理范围"

        return "正常"

    def check_gender(row: pd.Series) -> str:
        gender = row["gender_standard"]

        if gender == "未知":
            return "性别不规范"

        return "正常"

    result["age_quality_status"] = result.apply(check_age, axis=1)
    result["gender_quality_status"] = result.apply(check_gender, axis=1)

    result["patient_quality_status"] = result.apply(
        lambda row: (
            "正常"
            if row["age_quality_status"] == "正常"
            and row["gender_quality_status"] == "正常"
            else "异常"
        ),
        axis=1,
    )

    return result


def check_diagnosis_quality(df: pd.DataFrame) -> pd.DataFrame:
    """检查诊断名称和 ICD 编码完整性。"""

    result = df.copy()

    def check(row: pd.Series) -> str:
        errors: list[str] = []

        diagnosis_name = row["diagnosis_name"]
        diagnosis_code = row["diagnosis_code"]

        if pd.isna(diagnosis_name) or str(diagnosis_name).strip() == "":
            errors.append("诊断名称缺失")

        if pd.isna(diagnosis_code) or str(diagnosis_code).strip() == "":
            errors.append("ICD编码缺失")

        return "；".join(errors) if errors else "正常"

    result["diagnosis_quality_status"] = result.apply(check, axis=1)

    return result


def check_medication_quality(df: pd.DataFrame) -> pd.DataFrame:
    """检查用药剂量和剂量单位。"""

    result = df.copy()

    def check(row: pd.Series) -> str:
        errors: list[str] = []

        dose = row["dose"]
        dose_unit = row["dose_unit"]

        if pd.isna(dose):
            errors.append("剂量缺失")
        elif dose <= 0:
            errors.append("剂量小于等于0")
        elif dose > 1000:
            errors.append("剂量超出合理范围")

        if pd.isna(dose_unit) or str(dose_unit).strip() == "":
            errors.append("剂量单位缺失")

        return "；".join(errors) if errors else "正常"

    result["medication_quality_status"] = result.apply(check, axis=1)

    return result