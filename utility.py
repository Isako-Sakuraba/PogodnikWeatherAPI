def find_in_csv_dict_table(frame, key):
    result = []
    for i in range(len(frame.values)):
        if frame.values[i][0] == key:
            result = frame.values[i][1]

    return result


def check_in_csv_dict_table(frame, key):
    result = False
    for i in range(len(frame.values)):
        if frame.values[i][0] == key:
            result = True

    return result
