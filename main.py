from logger import get_logger
logger = get_logger(__name__)
from analysis.analysis import (
    analyze_disease_category,
    analyze_drug_usage,
    analyze_hospital_quality,
    build_medical_wide_table,
    calculate_overall_kpi,
)
from loader.data_loader import (
    load_diagnosis_data,
    load_medication_data,
    load_patient_data,
)
from quality.quality_check import (
    check_diagnosis_quality,
    check_medication_quality,
    check_patient_quality,
)
from report.report import export_analysis_report
from standard.standardization import (
    standardize_gender,
    standardize_icd,
)
from visualization.visualization import (
    generate_disease_category_chart,
    generate_drug_usage_chart,
    generate_hospital_quality_chart,
)
from config import DATASET_MODE
from time import perf_counter

def main() -> None:
    start_time = perf_counter()
    logger.info("医学数据分析任务开始")

    try:
        # 1. 数据读取
        logger.info("正在读取数据库数据")

        patient_df = load_patient_data()
        diagnosis_df = load_diagnosis_data()
        medication_df = load_medication_data()

        # ===== 新增：数据读取后的日志 =====
        logger.info(
            "当前数据集模式：%s",
            DATASET_MODE,
        )
        logger.info(
            "数据读取完成：患者=%s，就诊关联诊断=%s，用药=%s",
            len(patient_df),
            len(diagnosis_df),
            len(medication_df),
        )


        # 2. 字段标准化
        logger.info("正在进行字段标准化")

        patient_standard_df = standardize_gender(patient_df)
        diagnosis_standard_df = standardize_icd(diagnosis_df)

        # 3. 数据质控
        logger.info("正在执行数据质量检查")

        patient_quality_df = check_patient_quality(
            patient_standard_df
        )

        diagnosis_quality_df = check_diagnosis_quality(
            diagnosis_standard_df
        )

        medication_quality_df = check_medication_quality(
            medication_df
        )

        # 4. 构建医学宽表
        logger.info("正在构建医学宽表")

        medical_wide_df = build_medical_wide_table(
            patient_quality_df,
            diagnosis_quality_df,
            medication_quality_df,
        )
        logger.info(
            "医学宽表生成完成：%s 行，%s 列",
            medical_wide_df.shape[0],
            medical_wide_df.shape[1],
        )

        # 5. 指标分析
        logger.info("正在计算分析指标")

        overall_kpi = calculate_overall_kpi(
            patient_quality_df,
            diagnosis_quality_df,
            medication_quality_df,
        )

        hospital_summary_df = analyze_hospital_quality(
            patient_quality_df
        )

        disease_category_df = analyze_disease_category(
            diagnosis_quality_df
        )

        drug_usage_df = analyze_drug_usage(
            medication_quality_df
        )

        logger.info("总体KPI：%s", overall_kpi)

        # 6. 生成图表
        logger.info("正在生成分析图表")

        hospital_chart = generate_hospital_quality_chart(
            hospital_summary_df
        )

        disease_chart = generate_disease_category_chart(
            disease_category_df
        )

        drug_chart = generate_drug_usage_chart(
            drug_usage_df
        )

        # 7. 生成 Excel 报告
        logger.info("正在生成Excel分析报告")

        report_path = export_analysis_report(
            overall_kpi=overall_kpi,
            patient_quality_df=patient_quality_df,
            diagnosis_quality_df=diagnosis_quality_df,
            medication_quality_df=medication_quality_df,
            medical_wide_df=medical_wide_df,
            hospital_summary_df=hospital_summary_df,
            disease_category_df=disease_category_df,
            drug_usage_df=drug_usage_df,
        )

        logger.info("医院质量图表：%s", hospital_chart)
        logger.info("疾病分类图表：%s", disease_chart)
        logger.info("用药统计图表：%s", drug_chart)
        logger.info("Excel报告：%s", report_path)

        logger.info("医学数据分析任务执行完成")

    except Exception:
        logger.exception("医学数据分析任务执行失败")
        raise

    elapsed_seconds = perf_counter() - start_time
    logger.info(
        "任务总耗时：%.2f 秒",
        elapsed_seconds,
    )

    print("\n图表已生成：")
    print(hospital_chart)
    print(disease_chart)
    print(drug_chart)

    print("\nExcel 报告已生成：")
    print(report_path)

    print("=" * 60)
    print("医学数据分析任务执行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()