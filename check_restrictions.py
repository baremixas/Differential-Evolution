from func_from_str import func_read

def check_restrictions(element, num_arg, func_list, bounds):
    valid = True

    for i in range(num_arg):
        if len(bounds[i]) != 0:
            if bounds[i][0] <= element[i] <= bounds[i][1]:
                continue
            else:
                valid = False
        else:
            if -5 <= element[i] <= 5:
                continue
            else:
                valid = False

        if len(func_list) != 0:
            for value in func_read(func_list, element):
                if value > 0:
                    valid = False

    return valid
