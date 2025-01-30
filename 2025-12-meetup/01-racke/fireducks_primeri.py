#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 16:45:11 2025

@author: mazinga
"""
import fireducks.pandas as pd
import duckdb
import time
import matplotlib.pyplot as plt

# Povezava z DuckDB
conn = duckdb.connect("/home/user/.../racja_baza")

# Uvoz podatkov iz DuckDB v FireDucks DataFrame
start_time_import = time.time()
df_pandas = conn.execute("SELECT * FROM dejanska_raba_20241231").df()
df = pd.DataFrame(df_pandas)  # Pretvorba v FireDucks DataFrame
import_time = time.time() - start_time_import

print(f"\u010cas uvoza podatkov: {import_time:.4f} s")

# Pretvorba površin iz m² v hektare
start_time_conversion = time.time()
df["AREA_HA"] = df["AREA"] / 10000
conversion_time = time.time() - start_time_conversion

print(f"Trajanje pretvorbe: {conversion_time:.4f} s")

# Filtriranje podatkov za trajne nasade (RABA_ID med 1211 in 1300)
start_time_filter = time.time()
df_filtered = df[(df["RABA_ID"] >= 1211) & (df["RABA_ID"] < 1300)].copy()
filter_time = time.time() - start_time_filter

print(f"Trajanje filtriranja: {filter_time:.4f} s")

# Zamenjava ID-jev z imeni trajnih nasadov
start_time_mapping = time.time()
raba_labels = {
    1211: "Vinograd",
    1212: "Matičnjak",
    1221: "Intenzivni sadovnjak",
    1222: "Ekstenzivni sadovnjak",
    1230: "Oljčnik",
    1240: "Ostali trajni nasadi"
}
df_filtered["RABA_NAME"] = df_filtered["RABA_ID"].map(raba_labels)
mapping_time = time.time() - start_time_mapping

print(f"\u010cas zamenjave ID-jev z imeni: {mapping_time:.4f} s")

# Združevanje površin po vrsti trajnega nasada
start_time_groupby = time.time()
area_summary = df_filtered.groupby("RABA_NAME")["AREA_HA"].sum().reset_index()
groupby_time = time.time() - start_time_groupby

print(f"Trajanje združevanja podatkov: {groupby_time:.4f} s")

# Izris pie charta za trajne nasade
plt.figure(figsize=(8, 8))
plt.pie(area_summary["AREA_HA"], labels=area_summary["RABA_NAME"], autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
plt.title("Površine trajnih nasadov (ha)")
plt.show()

# Zapri povezavo
conn.close()
