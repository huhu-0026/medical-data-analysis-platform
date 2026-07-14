from __future__ import annotations

import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker

from config import engine


fake = Faker("zh_CN")

HOSPITALS = [
    "郑州大学第一附属医院",
    "洛阳市第三人民医院",
    "上海某医院",
    "北京某三甲医院",
    "杭州某综合医院",
]

GENDERS = ["男", "女"]

VISIT_TYPES = [
    "门诊",
    "住院",
    "急诊",
]

DEPARTMENTS = [
    "心内科",
    "内分泌科",
    "妇科",
    "呼吸科",
    "消化科",
    "神经内科",
]

DIAGNOSIS_CATALOG = [
    {
        "diagnosis_name": "冠心病",
        "diagnosis_code": "I25.101",
        "department_name": "心内科",
    },
    {
        "diagnosis_name": "高血压",
        "diagnosis_code": "I10.x00",
        "department_name": "心内科",
    },
    {
        "diagnosis_name": "2型糖尿病",
        "diagnosis_code": "E11.900",
        "department_name": "内分泌科",
    },
    {
        "diagnosis_name": "卵巢功能减退",
        "diagnosis_code": "E28.300",
        "department_name": "妇科",
    },
    {
        "diagnosis_name": "慢性阻塞性肺疾病",
        "diagnosis_code": "J44.900",
        "department_name": "呼吸科",
    },
    {
        "diagnosis_name": "胃炎",
        "diagnosis_code": "K29.700",
        "department_name": "消化科",
    },
    {
        "diagnosis_name": "脑梗死",
        "diagnosis_code": "I63.900",
        "department_name": "神经内科",
    },
]
MEDICATION_CATALOG = [
    {
        "drug_name": "阿司匹林肠溶片",
        "department_name": "心内科",
        "normal_dose": 100,
        "dose_unit": "mg",
        "frequency": "qd",
    },
    {
        "drug_name": "硝苯地平控释片",
        "department_name": "心内科",
        "normal_dose": 30,
        "dose_unit": "mg",
        "frequency": "qd",
    },
    {
        "drug_name": "盐酸二甲双胍片",
        "department_name": "内分泌科",
        "normal_dose": 500,
        "dose_unit": "mg",
        "frequency": "bid",
    },
    {
        "drug_name": "地屈孕酮片",
        "department_name": "妇科",
        "normal_dose": 10,
        "dose_unit": "mg",
        "frequency": "bid",
    },
    {
        "drug_name": "头孢克肟胶囊",
        "department_name": "呼吸科",
        "normal_dose": 100,
        "dose_unit": "mg",
        "frequency": "tid",
    },
    {
        "drug_name": "奥美拉唑肠溶胶囊",
        "department_name": "消化科",
        "normal_dose": 20,
        "dose_unit": "mg",
        "frequency": "qd",
    },
    {
        "drug_name": "阿托伐他汀钙片",
        "department_name": "神经内科",
        "normal_dose": 20,
        "dose_unit": "mg",
        "frequency": "qn",
    },
]
RANDOM_SEED = 42


def generate_patient_data(
    patient_count: int = 1000,
    abnormal_age_rate: float = 0.02,
    abnormal_gender_rate: float = 0.01,
) -> pd.DataFrame:
    """生成患者基础信息。"""

    if patient_count <= 0:
        raise ValueError("patient_count 必须大于 0")

    random.seed(RANDOM_SEED)
    Faker.seed(RANDOM_SEED)

    records: list[dict] = []
    now = datetime.now()

    for index in range(1, patient_count + 1):
        patient_id = f"P{index:08d}"

        age = random.randint(1, 95)
        gender = random.choice(GENDERS)

        if random.random() < abnormal_age_rate:
            age = random.choice([None, -1, 130, 999])

        if random.random() < abnormal_gender_rate:
            gender = random.choice(
                ["未知", "M", "F", "", None]
            )

        create_time = now - timedelta(
            days=random.randint(0, 365),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )

        records.append(
            {
                "patient_id": patient_id,
                "patient_name": fake.name(),
                "gender": gender,
                "age": age,
                "hospital_name": random.choice(HOSPITALS),
                "create_time": create_time,
            }
        )

    return pd.DataFrame(records)

def generate_visit_data(
    patient_df: pd.DataFrame,
    min_visits_per_patient: int = 1,
    max_visits_per_patient: int = 5,
) -> pd.DataFrame:
    """
    基于患者数据生成就诊记录。

    一个患者可对应多次就诊，形成一对多关系。
    """

    if min_visits_per_patient <= 0:
        raise ValueError("min_visits_per_patient 必须大于 0")

    if max_visits_per_patient < min_visits_per_patient:
        raise ValueError(
            "max_visits_per_patient 不能小于 min_visits_per_patient"
        )

    records: list[dict] = []
    visit_index = 1

    for _, patient in patient_df.iterrows():
        visit_count = random.randint(
            min_visits_per_patient,
            max_visits_per_patient,
        )

        patient_create_time = pd.to_datetime(
            patient["create_time"]
        )

        for _ in range(visit_count):
            visit_time = patient_create_time + timedelta(
                days=random.randint(0, 180),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            )

            records.append(
                {
                    "visit_id": f"V{visit_index:010d}",
                    "patient_id": patient["patient_id"],
                    "hospital_name": patient["hospital_name"],
                    "visit_type": random.choice(VISIT_TYPES),
                    "department_name": random.choice(DEPARTMENTS),
                    "visit_time": visit_time,
                }
            )

            visit_index += 1

    return pd.DataFrame(records)

def generate_diagnosis_data(
    visit_df: pd.DataFrame,
    min_diagnoses_per_visit: int = 1,
    max_diagnoses_per_visit: int = 3,
    missing_diagnosis_rate: float = 0.01,
) -> pd.DataFrame:
    """
    基于就诊记录生成诊断数据。

    每次就诊生成 1～3 条诊断，
    并按比例注入诊断名称或 ICD 编码缺失。
    """

    if min_diagnoses_per_visit <= 0:
        raise ValueError("min_diagnoses_per_visit 必须大于 0")

    if max_diagnoses_per_visit < min_diagnoses_per_visit:
        raise ValueError(
            "max_diagnoses_per_visit 不能小于 min_diagnoses_per_visit"
        )

    records: list[dict] = []
    diagnosis_index = 1

    for _, visit in visit_df.iterrows():
        diagnosis_count = random.randint(
            min_diagnoses_per_visit,
            max_diagnoses_per_visit,
        )

        department_name = visit["department_name"]

        department_diagnoses = [
            item
            for item in DIAGNOSIS_CATALOG
            if item["department_name"] == department_name
        ]

        if not department_diagnoses:
            department_diagnoses = DIAGNOSIS_CATALOG

        for _ in range(diagnosis_count):
            diagnosis = random.choice(department_diagnoses)

            diagnosis_name = diagnosis["diagnosis_name"]
            diagnosis_code = diagnosis["diagnosis_code"]

            if random.random() < missing_diagnosis_rate:
                missing_type = random.choice(
                    [
                        "name",
                        "code",
                        "both",
                    ]
                )

                if missing_type in {"name", "both"}:
                    diagnosis_name = None

                if missing_type in {"code", "both"}:
                    diagnosis_code = None

            records.append(
                {
                    "diagnosis_id": f"D{diagnosis_index:010d}",
                    "visit_id": visit["visit_id"],
                    "patient_id": visit["patient_id"],
                    "diagnosis_name": diagnosis_name,
                    "diagnosis_code": diagnosis_code,
                    "diagnosis_date": visit["visit_time"].date(),
                }
            )

            diagnosis_index += 1

    return pd.DataFrame(records)

def generate_medication_data(
    visit_df: pd.DataFrame,
    min_medications_per_visit: int = 0,
    max_medications_per_visit: int = 3,
    abnormal_dose_rate: float = 0.01,
    missing_unit_rate: float = 0.01,
) -> pd.DataFrame:
    """
    基于就诊记录生成用药数据。

    每次就诊生成 0～3 条用药记录，
    并注入少量剂量异常和剂量单位缺失。
    """

    if min_medications_per_visit < 0:
        raise ValueError(
            "min_medications_per_visit 不能小于 0"
        )

    if max_medications_per_visit < min_medications_per_visit:
        raise ValueError(
            "max_medications_per_visit 不能小于 min_medications_per_visit"
        )

    records: list[dict] = []
    medication_index = 1

    for _, visit in visit_df.iterrows():
        medication_count = random.randint(
            min_medications_per_visit,
            max_medications_per_visit,
        )

        department_name = visit["department_name"]

        department_medications = [
            item
            for item in MEDICATION_CATALOG
            if item["department_name"] == department_name
        ]

        if not department_medications:
            department_medications = MEDICATION_CATALOG

        for _ in range(medication_count):
            medication = random.choice(
                department_medications
            )

            dose = medication["normal_dose"]
            dose_unit = medication["dose_unit"]

            if random.random() < abnormal_dose_rate:
                dose = random.choice(
                    [
                        None,
                        0,
                        -1,
                        9999,
                    ]
                )

            if random.random() < missing_unit_rate:
                dose_unit = random.choice(
                    [
                        None,
                        "",
                    ]
                )

            records.append(
                {
                    "medication_id": (
                        f"M{medication_index:010d}"
                    ),
                    "visit_id": visit["visit_id"],
                    "patient_id": visit["patient_id"],
                    "drug_name": medication["drug_name"],
                    "dose": dose,
                    "dose_unit": dose_unit,
                    "frequency": medication["frequency"],
                    "medication_date": (
                        visit["visit_time"].date()
                    ),
                }
            )

            medication_index += 1

    return pd.DataFrame(records)

def save_patient_data(
    patient_df: pd.DataFrame,
    table_name: str = "patient_synthetic",
) -> None:
    """将合成患者数据写入 PostgreSQL。"""

    patient_df.to_sql(
        name=table_name,
        con=engine,
        schema="public",
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=1000,
    )

    print(f"\n患者数据已写入 PostgreSQL：{table_name}")
    print(f"写入记录数：{len(patient_df)}")

def save_visit_data(
    visit_df: pd.DataFrame,
    table_name: str = "visit_synthetic",
) -> None:
    """将合成就诊数据写入 PostgreSQL。"""

    visit_df.to_sql(
        name=table_name,
        con=engine,
        schema="public",
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=1000,
    )

    print(f"\n就诊数据已写入 PostgreSQL：{table_name}")
    print(f"写入记录数：{len(visit_df)}")
def save_diagnosis_data(
    diagnosis_df: pd.DataFrame,
    table_name: str = "diagnosis_synthetic",
) -> None:
    """将合成诊断数据写入 PostgreSQL。"""

    diagnosis_df.to_sql(
        name=table_name,
        con=engine,
        schema="public",
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=1000,
    )

    print(f"\n诊断数据已写入 PostgreSQL：{table_name}")
    print(f"写入记录数：{len(diagnosis_df)}")

def save_medication_data(
            medication_df: pd.DataFrame,
            table_name: str = "medication_synthetic",
    ) -> None:
        """将合成用药数据写入 PostgreSQL。"""

        medication_df.to_sql(
            name=table_name,
            con=engine,
            schema="public",
            if_exists="replace",
            index=False,
            method="multi",
            chunksize=1000,
        )

        print(f"\n用药数据已写入 PostgreSQL：{table_name}")
        print(f"写入记录数：{len(medication_df)}")

def main() -> None:
    patient_df = generate_patient_data(
        patient_count=1000,
        abnormal_age_rate=0.02,
        abnormal_gender_rate=0.01,
    )

    save_patient_data(patient_df)

    visit_df = generate_visit_data(
        patient_df=patient_df,
        min_visits_per_patient=1,
        max_visits_per_patient=5,
    )

    save_visit_data(visit_df)

    diagnosis_df = generate_diagnosis_data(
        visit_df=visit_df,
        min_diagnoses_per_visit=1,
        max_diagnoses_per_visit=3,
        missing_diagnosis_rate=0.01,
    )

    save_diagnosis_data(diagnosis_df)

    medication_df = generate_medication_data(
        visit_df=visit_df,
        min_medications_per_visit=0,
        max_medications_per_visit=3,
        abnormal_dose_rate=0.01,
        missing_unit_rate=0.01,
    )

    save_medication_data(medication_df)


    print("患者数据生成完成")
    print("数据规模：", patient_df.shape)

    print("\n前10条数据：")
    print(patient_df.head(10))

    print("\n缺失值统计：")
    print(patient_df.isna().sum())
    print("\n就诊数据生成完成")
    print("就诊数据规模：", visit_df.shape)

    print("\n就诊数据前10条：")
    print(visit_df.head(10))

    print("\n每名患者就诊次数统计：")
    print(
        visit_df.groupby("patient_id")
        .size()
        .describe()
    )

    abnormal_age_count = (
        patient_df["age"].isna()
        | (patient_df["age"] < 0)
        | (patient_df["age"] > 120)
    ).sum()

    print("\n年龄异常数量：")
    print(abnormal_age_count)

    abnormal_gender_count = (
        patient_df["gender"].isna()
        | ~patient_df["gender"].isin(["男", "女"])
    ).sum()

    print("\n性别异常数量：")
    print(abnormal_gender_count)
    print("\n诊断数据生成完成")
    print("诊断数据规模：", diagnosis_df.shape)

    print("\n诊断数据前10条：")
    print(diagnosis_df.head(10))

    print("\n诊断异常数量：")
    diagnosis_abnormal_count = (
            diagnosis_df["diagnosis_name"].isna()
            | diagnosis_df["diagnosis_code"].isna()
    ).sum()
    print(diagnosis_abnormal_count)

    print("\n用药数据生成完成")
    print("用药数据规模：", medication_df.shape)

    print("\n用药数据前10条：")
    print(medication_df.head(10))

    print("\n剂量异常数量：")
    abnormal_dose_count = (
            medication_df["dose"].isna()
            | (medication_df["dose"] <= 0)
            | (medication_df["dose"] > 1000)
    ).sum()
    print(abnormal_dose_count)

    print("\n剂量单位缺失数量：")
    missing_unit_count = (
            medication_df["dose_unit"].isna()
            | (
                    medication_df["dose_unit"]
                    .astype(str)
                    .str.strip()
                    == ""
            )
    ).sum()
    print(missing_unit_count)


if __name__ == "__main__":
    main()