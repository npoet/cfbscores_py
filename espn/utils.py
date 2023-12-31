def convert_time(timestring):
    """
    convert_time is a convoluted time string converter for ESPN shortDetail times (if you're reading this I am so sorry)
    :param timestring: ESPN shortDetail time as string, i.e. "10/14 - 11:00 PM EDT"
    :return: replacement string converted to pacific time, i.e. "10/14 - 8:00 PM PDT"
    """
    t = timestring.split(" - ")
    start = t[1]    # "8:15 PM EST"
    n = start.split(" ")
    # get pacific hour
    p_h = str(int(n[0].split(":")[0]) - 3)
    if int(p_h) == 0:
        p_h = "12"
    elif int(p_h) == -1:
        p_h = "11"
    elif int(p_h) == -2:
        p_h = "10"
    elif int(p_h) < -2:
        p_h = str(0 - int(p_h))
    # create pacific time str
    p_t = p_h + ":" + n[0].split(":")[1]
    # set AM PM
    a_p = n[1]
    if int(n[0].split(":")[0]) < 3:
        a_p = "AM"
    if int(n[0].split(":")[0]) == 12:
        a_p = "AM"
    dst = n[2]
    # set proper time
    if dst == "EST":
        dst = "PST"
    else:
        dst = "PDT"
    # return combined
    return t[0] + " - " + p_t + " " + a_p + " " + dst
