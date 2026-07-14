from __future__ import annotations

import pandas as pd
from sqlalchemy import text

from config import DATASET_MODE, engine


TABLE_MAPPING = {
    "demo": {
        "patient": "patient",
        "diagnosis": "diagnosis_record",
        "medication": "medication_record",
    },
    "synthetic": {
        "patient": "patient_synthetic",
        "diagnosis": "diagnosis_synthetic",
        "medication": "medication_synthetic",
    },
}

ALLOWED_TABLES = {
    table_name
    for mode_mapping in TABLE_MAPPING.values()
    for table_name in mode_mapping.values()
}


def load_table(table_name: str) -> pd.DataFrame:
    """从 PostgreSQL 读取白名单中的数据表。"""

    if table_name not in ALLOWED_TABLES:
        raise ValueError(
            f"不允许读取的数据表：{table_name}"
        )

    with engine.connect() as connection:
        result = connection.execute(
            text(f"SELECT * FROM {table_name}")
        )

        return pd.DataFrame(
            result.fetchall(),
            columns=result.keys(),
        )


def load_patient_data() -> pd.DataFrame:
    table_name = TABLE_MAPPING[DATASET_MODE]["patient"]
    return load_table(table_name)


def load_diagnosis_data() -> pd.DataFrame:
    table_name = TABLE_MAPPING[DATASET_MODE]["diagnosis"]
    return load_table(table_name)


def load_medication_data() -> pd.DataFrame:
    table_name = TABLE_MAPPING[DATASET_MODE]["medication"]
    return load_table(table_name)