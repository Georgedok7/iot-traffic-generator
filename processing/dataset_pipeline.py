import pandas as pd

from processing.zeek_processor import (
    run_zeek,
    load_conn_log
)


def create_labeled_dataset(
    flow_df,
    event_metadata
):
    metadata_df = pd.DataFrame(
        event_metadata
    )

    merge_columns = [
        "src_ip",
        "src_port",
        "dst_ip",
        "dst_port",
        "protocol"
    ]

    metadata_df["occurrence"] = (
        metadata_df.groupby(
            merge_columns
        ).cumcount()
    )

    flow_df = flow_df.copy()

    flow_df["occurrence"] = (
        flow_df.groupby(
            merge_columns
        ).cumcount()
    )

    labeled_flow_df = flow_df.merge(
        metadata_df,
        on=merge_columns + ["occurrence"],
        how="left"
    )

    labeled_flow_df = labeled_flow_df.drop(
        columns=["occurrence"]
    )

    return labeled_flow_df


def process_flow_dataset(
    pcap_path,
    event_metadata,
    zeek_output_dir,
    csv_output_path
):
    run_zeek(
        pcap_path,
        zeek_output_dir
    )

    flow_df = load_conn_log(
        f"{zeek_output_dir}/conn.log"
    )

    labeled_flow_df = (
        create_labeled_dataset(
            flow_df,
            event_metadata
        )
    )

    labeled_flow_df.to_csv(
        csv_output_path,
        index=False
    )

    return labeled_flow_df