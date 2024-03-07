import pandas as pd
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import datetime

downloads_folder = r"D:\Downloads"

data = pd.read_csv(r'D:\merged.csv')

selected_cols = ["MidTime", "Timestamp", "ID", "Location", "Productivity", "Mood", "Stress", "Average_lux_30s",
                 "Average_spl_a_30s", "Average_score_30s", "Average_temp_30s", "Average_humid_30s", "Average_co2_30s",
                 "Average_voc_30s", "Average_pm10_est_30s", "Average_pm25_30s",
                 "Average_spl_a_30s_(below_50_dB)", "Average_spl_a_30s_(above_50_dB)", "Average_temp_30s_(below_22C)",
                 "Average_temp_30s_(above_22C)", "Average_humid_30s_(below_45%)", "Average_humid_30s_(above_45%)",
                 "Average_lux_60s", "Average_spl_a_60s", "Average_score_60s", "Average_temp_60s", "Average_humid_60s",
                 "Average_co2_60s", "Average_voc_60s", "Average_pm10_est_60s", "Average_pm25_60s",
                 "Average_spl_a_60s_(below_50_dB)", "Average_spl_a_60s_(above_50_dB)", "Average_temp_60s_(below_22C)",
                 "Average_temp_60s_(above_22C)", "Average_humid_60s_(below_45%)", "Average_humid_60s_(above_45%)",
                 "Average_lux_120s", 'Average_spl_a_120s', "Average_score_120s", "Average_temp_120s",
                 'Average_humid_120s', "Average_co2_120s", "Average_voc_120s", "Average_pm10_est_120s",
                 "Average_pm25_120s",
                 "Average_spl_a_120s_(below_50_dB)", "Average_spl_a_120s_(above_50_dB)",
                 "Average_temp_120s_(below_22C)", "Average_temp_120s_(above_22C)", "Average_humid_120s_(below_45%)",
                 "Average_humid_120s_(above_45%)",
                 "Average_lux_300s", "Average_spl_a_300s", "Average_score_300s", "Average_temp_300s",
                 "Average_humid_300s", "Average_co2_300s", "Average_voc_300s", "Average_pm10_est_300s",
                 "Average_pm25_300s",
                 "Average_spl_a_300s_(below_50_dB)", "Average_spl_a_300s_(above_50_dB)",
                 "Average_temp_300s_(below_22C)", "Average_temp_300s_(above_22C)", "Average_humid_300s_(below_45%)",
                 "Average_humid_300s_(above_45%)",
                 "Average_lux_600s", "Average_spl_a_600s", "Average_score_600s", "Average_temp_600s",
                 "Average_humid_600s", "Average_co2_600s", "Average_voc_600s", "Average_pm10_est_600s",
                 "Average_pm25_600s",
                 "Average_spl_a_600s_(below_50_dB)", "Average_spl_a_600s_(above_50_dB)",
                 "Average_temp_600s_(below_22C)", "Average_temp_600s_(above_22C)", "Average_humid_600s_(below_45%)",
                 "Average_humid_600s_(above_45%)",
                 "Average_lux_1800s", "Average_spl_a_1800s", "Average_score_1800s", "Average_temp_1800s",
                 "Average_humid_1800s", "Average_co2_1800s", "Average_voc_1800s", "Average_pm10_est_1800s",
                 "Average_pm25_1800s",
                 "Average_spl_a_1800s_(below_50_dB)", "Average_spl_a_1800s_(above_50_dB)",
                 "Average_temp_1800s_(below_22C)", "Average_temp_1800s_(above_22C)", "Average_humid_1800s_(below_45%)",
                 "Average_humid_1800s_(above_45%)",
                 "Average_lux_3600s", "Average_spl_a_3600s", "Average_score_3600s", "Average_temp_3600s",
                 "Average_humid_3600s", "Average_co2_3600s", "Average_voc_3600s", "Average_pm10_est_3600s",
                 "Average_pm25_3600s",
                 "Average_spl_a_3600s_(below_50_dB)", "Average_spl_a_3600s_(above_50_dB)",
                 "Average_temp_3600s_(below_22C)", "Average_temp_3600s_(above_22C)", "Average_humid_3600s_(below_45%)",
                 "Average_humid_3600s_(above_45%)",
                 "Average_lux_7200s", "Average_spl_a_7200s", "Average_score_7200s", "Average_temp_7200s",
                 "Average_humid_7200s", "Average_co2_7200s", "Average_voc_7200s", "Average_pm10_est_7200s",
                 "Average_pm25_7200s",
                 "Average_spl_a_7200s_(below_50_dB)", "Average_spl_a_7200s_(above_50_dB)",
                 "Average_temp_7200s_(below_22C)", "Average_temp_7200s_(above_22C)", "Average_humid_7200s_(below_45%)",
                 "Average_humid_7200s_(above_45%)",
                 ]

data = data[selected_cols]

num_nans = data.isna().sum().sum()

data = data.fillna(method='ffill').fillna(method='bfill')

data["Timestamp"] = pd.to_datetime(data["Timestamp"])

data['Day'] = data['Timestamp'].apply(lambda x: x.strftime('%Y-%m-%d'))

def calculate_sma(data, window):
    sma_features = []
    for i in range(len(data)):
        if i < window:
            sma = np.mean(data[:i + 1])
        else:
            sma = np.mean(data[i - window + 1:i + 1])
        sma_features.append(sma)
    return sma_features

def get_hr_data(path):
    with open(path) as file:
        data = json.load(file)
    data = data['activities-heart-intraday']["dataset"]
    data = pd.DataFrame(data)
    if data.empty:
        raise ValueError("No data found in the file")
    data["sma_5"] = calculate_sma(data["value"], 5)
    data["sma_10"] = calculate_sma(data["value"], 10)
    data["sma_15"] = calculate_sma(data["value"], 15)
    data["sma_30"] = calculate_sma(data["value"], 30)
    data["sma_60"] = calculate_sma(data["value"], 60)
    data["sma_120"] = calculate_sma(data["value"], 120)
    data["sma_300"] = calculate_sma(data["value"], 300)
    data = data.to_numpy()
    return data

def get_hr_path(x):
    t = x["Timestamp"].strftime('%Y-%m-%d')
    fname = t + '_hr.json'
    tid = x["ID"]
    fpath = os.path.join(downloads_folder, tid, "fitbit_data", fname)
    return fpath

data["hr_path"] = data.apply(get_hr_path, axis=1)

data_arr = []
for i in list(data["hr_path"]):
    try:
        if os.path.exists(i):
            data_arr.append(get_hr_data(i))
            print("Success")
        else:
            print("File not found")
    except Exception as e:
        print("Error: " + str(e))
        continue

def get_audio_img(path):
    cols = ["mfcc[1]","mfcc[2]","mfcc[3]","mfcc[4]","mfcc[5]","mfcc[6]","mfcc[7]","mfcc[8]","mfcc[9]","mfcc[10]","mfcc[11]","mfcc[12]"]
    data = pd.read_csv(path,sep=';',usecols=cols)
    mfcc_image = data.to_numpy()
    mfcc_image = mfcc_image / np.max(mfcc_image)
    mfcc_image = np.resize(mfcc_image, (224, 224))
    return mfcc_image

def get_audio_path(x):
    t_d = x["Timestamp"].strftime('%Y-%m-%d')
    t_t = x["Timestamp"].strftime('%H-%M-%S')
    root_path = os.path.join(downloads_folder, x["ID"], "audio", t_d)

    # Check if root path exists
    if not os.path.exists(root_path):
        return None

    # Check if there's a subfolder with the same name
    subfolders = os.listdir(root_path)
    subfolder_paths = [os.path.join(root_path, subfolder) for subfolder in subfolders if
                       os.path.isdir(os.path.join(root_path, subfolder))]

    # Look for subfolders with the same name
    matching_subfolders = [subfolder for subfolder in subfolder_paths if t_d in os.path.basename(subfolder)]

    if matching_subfolders:
        root_path = matching_subfolders[0]

    root_path = os.path.join(root_path, "csv")

    # Check if root path exists
    if not os.path.exists(root_path):
        return None

    fnames = os.listdir(root_path)

    # Check if .DS_Store file is present in fnames list
    if '.DS_Store' in fnames:
        fnames.remove('.DS_Store')

    target_timestamp = datetime.datetime.strptime(t_t, '%H-%M-%S')
    ts = [datetime.datetime.strptime(i.split('_')[-1][:-4], '%H-%M-%S') for i in fnames]
    closest_timestamp = min(ts, key=lambda x: abs(x - target_timestamp))

    fpath = os.path.join(root_path, fnames[ts.index(closest_timestamp)])
    return fpath


data["audio_path"] = data.apply(get_audio_path, axis=1)

path = r"D:\Downloads\ID107\audio\2023-09-29\audio_C300000A0E98_16-22-11.csv"
mfcc_im = get_audio_img(path)
mfcc_im
plt.imshow(mfcc_im, cmap='gray')
plt.axis('off')  # Turn off axis
plt.show()
data.to_csv('modified_merged1.csv', index=False)

