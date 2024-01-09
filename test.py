

def test_conversion_to_timestamp():

    data_filepath = "artifacts/data/raw/2nd_test/2004.02.12.10.32.39"

    from datetime import datetime

    date_string = "2004.02.12.10.32.39"
    # Define the format of the input string
    format_string = "%Y.%m.%d.%H.%M.%S"

    # Convert the string to a datetime object
    dt_object = datetime.strptime(date_string, format_string)

    # Convert the datetime object to a string in a desired format
    formatted_date_string = dt_object.strftime("%Y-%m-%d %H:%M:%S")

    print(formatted_date_string)


if __name__ == "__main__":
    test_conversion_to_timestamp()

