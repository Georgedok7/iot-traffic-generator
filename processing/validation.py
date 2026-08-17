def validate_dataset(df, expected_flows):
    print()
    print("=== DATASET VALIDATION ===")

    if len(df) == expected_flows:
        print("Flow count: OK")
    else:
        print(
            f"Flow count: ERROR "
            f"(expected {expected_flows}, got {len(df)})"
        )

    missing_labels = df["label"].isna().sum()

    if missing_labels == 0:
        print("Missing labels: OK")
    else:
        print(
            f"Missing labels: ERROR "
            f"({missing_labels} missing)"
        )

    if df["label"].notna().all():
        print("Labeling: OK")
    else:
        print("Labeling: ERROR")

    required_columns = [
        "src_ip",
        "src_port",
        "dst_ip",
        "dst_port",
        "protocol",
        "label"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if not missing_columns:
        print("Required columns: OK")
    else:
        print(
            "Missing columns:",
            missing_columns
        )

def validate_config(
    total_flows,
    attack_ratio,
    dns_ratio,
    http_ratio,
    mqtt_ratio,
    port_scan_ratio,
    mqtt_flood_ratio,
    dns_exfiltration_ratio,
    mirai_ratio
):
    print()
    print("=== CONFIG VALIDATION ===")

    if total_flows > 0:
        print("Total flows: OK")
    else:
        raise ValueError("TOTAL_FLOWS must be greater than 0.")

    if 0 <= attack_ratio <= 1:
        print("Attack ratio: OK")
    else:
        raise ValueError("ATTACK_RATIO must be between 0 and 1.")

    normal_ratio_sum = (
        dns_ratio
        + http_ratio
        + mqtt_ratio
    )

    if abs(normal_ratio_sum - 1.0) < 0.000001:
        print("Normal traffic ratios: OK")
    else:
        raise ValueError(
            "DNS_RATIO + HTTP_RATIO + MQTT_RATIO must equal 1."
        )

    attack_ratio_sum = (
        port_scan_ratio
        + mqtt_flood_ratio
        + dns_exfiltration_ratio
        + mirai_ratio
    )

    if abs(attack_ratio_sum - 1.0) < 0.000001:
        print("Attack traffic ratios: OK")
    else:
        raise ValueError(
            "Attack type ratios must equal 1."
        )