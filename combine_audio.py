# %%
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import sys
import pytz  # Import pytz



# BASE_FEATURES_DIR = '/Users/abdulmk/Multimodal/Project/TILES'
BASE_FEATURES_DIR = '/project/msoleyma_1026/TILES/tiles-phase2-opendataset-audio/'


def combine_audio_features(worker_id, target_time, window_size=None):
    features_path = os.path.join(BASE_FEATURES_DIR, 'raw-features-named', worker_id)
    all_features = []
    for csv_file in os.listdir(features_path):
        file_timestamp_naive = datetime.strptime(csv_file[:-4], '%Y-%m-%d %H-%M-%S')
        local_tz = pytz.timezone('US/Pacific') 
        file_timestamp = local_tz.localize(file_timestamp_naive, is_dst=None)  
        one_hour_ago = target_time - timedelta(hours=3)
        end_t = target_time + timedelta(minutes=30)
        if file_timestamp > one_hour_ago and file_timestamp <= end_t:
            data = pd.read_csv(os.path.join(features_path, csv_file))
            

            if window_size:
                windows = split_data_windows(data, window_size)
                window_features = [calculate_features(w) for w in windows]
                all_features.extend(window_features) 
            else:
                all_features.append(calculate_features(data))
    if all_features:
        final_feature_vector = np.row_stack(all_features)
        final_feature_vector = np.nanmean(final_feature_vector, axis=0)
        print(f"Final feature vector shape: {final_feature_vector.shape} for worker: {worker_id} at timestamp: {target_time}")
    else:
        final_feature_vector = np.zeros(116)
        print(f"No audio features found for worker: {worker_id} at timestamp: {target_time}")
        return None
    return final_feature_vector

def split_data_windows(data, window_size):
    num_windows = int(data['frameTime'].max() / window_size) 
    windows = []
    for i in range(num_windows):
        start_time = i * window_size
        end_time = start_time + window_size
        window_data = data[(data['frameTime'] >= start_time) & (data['frameTime'] < end_time)]
        windows.append(window_data)
    return windows 

def calculate_features(data_or_window):
    numeric_cols = [col for col in data_or_window.columns if pd.api.types.is_numeric_dtype(data_or_window[col])]
    mean_features = data_or_window[numeric_cols].mean()
    std_features = data_or_window[numeric_cols].std()
    max_features = data_or_window[numeric_cols].max()



    all_features = np.concatenate([mean_features, std_features, max_features])  
    all_features = np.pad(all_features, (0, 87 - len(all_features)), mode='constant')
    return all_features

def process_worker_audio(worker_id, timestamp, survey_table, window_size=None):
    features_path = os.path.join(BASE_FEATURES_DIR, 'raw-features-named', worker_id)

    if os.path.exists(features_path):
        print(f"Processing audio features for worker: {worker_id} and timestamp: {timestamp}")
        audio_features = combine_audio_features(worker_id, timestamp, window_size)
        if audio_features is None:
            return 
        d = pd.DataFrame(audio_features).T
        d.columns = [f"audio_{i}" for i in range(87)]
        relevant_row = survey_table[(survey_table['id'] == worker_id) & 
                                (survey_table['started_ts'] == timestamp)]
        if not relevant_row.empty:
            audio_feature_cols = d.columns
            if not set(audio_feature_cols).issubset(survey_table.columns):
                for col in audio_feature_cols:
                    survey_table[col] = np.nan  # Initialize columns 

            survey_table.loc[(survey_table['id'] == worker_id) & 
                                (survey_table['started_ts'] == timestamp)
                                , audio_feature_cols] = audio_features
        else:
            print(f"Audio data not found for worker: {worker_id} at timestamp: {timestamp}")
    else: 
        print(f"Audio feature directory not found for worker: {worker_id}")
    return 



# %%
# survey_table = pd.read_csv('/Users/abdulmk/Multimodal/Project/TILES/EMA/daily_ema.csv')
survey_table = pd.read_csv('/project/msoleyma_1026/TILES/tiles-phase2-opendataset/surveys/scored/EMA/daily_ema.csv')

# %%
survey_table['started_ts']= pd.to_datetime(survey_table['started_ts'])

# %%

for index, row in survey_table.iterrows():
    process_worker_audio(row['id'], row['started_ts'], survey_table, window_size=None)
        
# %%
# survey_table.to_csv('/Users/abdulmk/Multimodal/Project/TILES/EMA/daily_ema_with_audio.csv', index=False)
survey_table.to_csv('/project/msoleyma_1026/TILES/tiles-phase2-opendataset/surveys/scored/EMA/daily_ema_with_audio.csv', index=False)

# %%



