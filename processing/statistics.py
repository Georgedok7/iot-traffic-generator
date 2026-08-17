def print_dataset_statistics(df):
    print()
    print("=== DATASET STATISTICS ===")

    print()
    print("Total flows:", len(df))

    print()
    print("Label distribution:")
    print(df["label"].value_counts())

    print()
    print("Protocol distribution:")
    print(df["protocol"].value_counts())

    print()
    print("Average flow duration:")
    print(df["duration"].mean())

    print()
    print("Average original packets per flow:")
    print(df["orig_pkts"].mean())

    print()
    print("Average response packets per flow:")
    print(df["resp_pkts"].mean())

    print()
    print("Average original bytes per flow:")
    print(df["orig_bytes"].mean())

    print()
    print("Average response bytes per flow:")
    print(df["resp_bytes"].mean())

    print()
    print("Most common destination ports:")
    print(df["dst_port"].value_counts().head(10))
    print()
    print("Statistics by label:")

    label_statistics = df.groupby("label")[
        [
            "duration",
            "orig_bytes",
            "resp_bytes",
            "orig_pkts",
            "resp_pkts"
        ]
    ].mean()

    print(label_statistics)