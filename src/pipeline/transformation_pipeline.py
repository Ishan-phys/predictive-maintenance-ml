import os

from src.components.data_transformation import DataTransformation


if __name__ == "__main__":
    data_dir = os.path.join('artifacts', 'data', 'raw', '2nd_test')
    sampling_rate = 20480
    bearing_num = 1

    data_transformation = DataTransformation()

    features_list = data_transformation.featurize_all(data_dir, sampling_rate, bearing_num)

    df = data_transformation.transform_to_df(features_list, save=True)

    data_transformation.split_data(df, train_size=400, save=True)