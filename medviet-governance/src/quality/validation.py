import re

import pandas as pd
from great_expectations.core.expectation_suite import ExpectationSuite
from great_expectations.expectations import (
    ExpectColumnValueLengthsToEqual,
    ExpectColumnValuesToBeBetween,
    ExpectColumnValuesToBeInSet,
    ExpectColumnValuesToBeUnique,
    ExpectColumnValuesToMatchRegex,
    ExpectColumnValuesToNotBeNull,
)

def build_patient_expectation_suite() -> ExpectationSuite:
    """
    TODO: Tạo expectation suite cho anonymized patient data.
    """
    valid_conditions = ["Tiểu đường", "Huyết áp cao", "Tim mạch", "Khỏe mạnh"]
    return ExpectationSuite(
        name="patient_data_suite",
        expectations=[
            ExpectColumnValuesToNotBeNull(column="patient_id"),
            ExpectColumnValueLengthsToEqual(column="cccd", value=12),
            ExpectColumnValuesToBeBetween(
                column="ket_qua_xet_nghiem", min_value=0, max_value=50
            ),
            ExpectColumnValuesToBeInSet(column="benh", value_set=valid_conditions),
            ExpectColumnValuesToMatchRegex(
                column="email",
                regex=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
            ),
            ExpectColumnValuesToBeUnique(column="patient_id"),
        ],
    )


def validate_anonymized_data(filepath: str) -> dict:
    """
    TODO: Validate anonymized data.
    Trả về dict: {"success": bool, "failed_checks": list, "stats": dict}
    """
    df = pd.read_csv(filepath)
    results = {
        "success": True,
        "failed_checks": [],
        "stats": {
            "total_rows": len(df),
            "columns": list(df.columns)
        }
    }

    cccd_pattern = re.compile(r"^\d{12}$")
    if "cccd" not in df.columns or not df["cccd"].astype(str).str.match(cccd_pattern).all():
        results["success"] = False
        results["failed_checks"].append("cccd must contain anonymized 12-digit values")

    required_columns = ["patient_id", "cccd", "so_dien_thoai", "email", "benh", "ket_qua_xet_nghiem"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        results["success"] = False
        results["failed_checks"].append(f"missing columns: {missing_columns}")
    else:
        null_columns = [col for col in required_columns if df[col].isnull().any()]
        if null_columns:
            results["success"] = False
            results["failed_checks"].append(f"null values in columns: {null_columns}")

    original_path = "data/raw/patients_raw.csv"
    try:
        original_rows = len(pd.read_csv(original_path))
        results["stats"]["original_rows"] = original_rows
        if len(df) != original_rows:
            results["success"] = False
            results["failed_checks"].append(
                f"row count mismatch: anonymized={len(df)}, original={original_rows}"
            )
    except FileNotFoundError:
        results["failed_checks"].append("original raw data not found; row count comparison skipped")

    return results
