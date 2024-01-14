from src.components.data_transformation import DataTransformation




if __name__ == "__main__":

    dt = DataTransformation()

    # Extract the data from the individual files
    data = dt.extract_data_file(data_filepath='artifacts/data/raw/2nd_test/2004.02.12.11.02.39', bearing_num=0)

    features_list = dt.featurize_all(data_dir="artifacts/data/raw/2nd_test", sampling_rate=20480, bearing_num=0, num_files=100)

    df = dt.transform_to_df(features_list, save=False)

    print(df)

