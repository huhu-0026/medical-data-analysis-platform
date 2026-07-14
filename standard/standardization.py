from __future__ import annotations

import pandas as pd


def standardize_gender(df: pd.DataFrame) -> pd.DataFrame:
    """统一性别字段口径。"""

    result = df.copy()

    gender_mapping = {
        "男性": "男",
        "男": "男",
        "M": "男",
        "m": "男",
        "male": "男",
        "MALE": "男",
        "女性": "女",
        "女": "女",
        "F": "女",
        "f": "女",
        "female": "女",
        "FEMALE": "女",
    }

    result["gender_standard"] = (
        result["gender"]
        .map(gender_mapping)
        .fillna("未知")
    )

    return result


def standardize_icd(df: pd.DataFrame) -> pd.DataFrame:
    """根据 ICD 编码映射标准疾病名称和疾病分类。"""

    result = df.copy()

    icd_mapping = {
        "I25.101": {
            "disease_name": "冠心病",
            "category": "心血管疾病",
        },
        "E11.900": {
            "disease_name": "2型糖尿病",
            "category": "代谢疾病",
        },
        "I10.x00": {
            "disease_name": "高血压",
            "category": "心血管疾病",
        },
        "E28.300": {
            "disease_name": "卵巢功能减退",
            "category": "妇科疾病",
        },
        "J44.900": {
            "disease_name": "慢性阻塞性肺疾病",
            "category": "呼吸系统疾病",
        },
        "K29.700": {
            "disease_name": "胃炎",
            "category": "消化系统疾病",
        },
        "I63.900": {
            "disease_name": "脑梗死",
            "category": "神经系统疾病",
        },
    }

    result["standard_disease_name"] = result["diagnosis_code"].map(
        lambda code: icd_mapping.get(code, {}).get("disease_name")
    )

    result["disease_category"] = result["diagnosis_code"].map(
        lambda code: icd_mapping.get(code, {}).get("category")
    )

    return result