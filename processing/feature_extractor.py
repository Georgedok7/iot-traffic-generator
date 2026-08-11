def prepare_features(df):
    df = df.copy()

    df["src_port"] = df["tcp.srcport"].fillna(df["udp.srcport"])
    df["dst_port"] = df["tcp.dstport"].fillna(df["udp.dstport"])

    return df