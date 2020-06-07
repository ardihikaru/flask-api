from datetime import timedelta, datetime  # , date
import os
from functools import reduce
import operator
import simplejson as json
from sqlalchemy import inspect


def masked_json_template(resp, code):
    try:
        if resp["response"]:
            return resp, 200
        else:
            return resp, code
    except:
        return get_json_template(message="Data not found."), 404


def get_json_template(response=False, results=None, total=0, message=None):
    result = {
        "response": response,
        "message": message,
        "results": results,
        "total": total
    }

    if results == -1:
        result.pop('results', None)
    else:
        if total == 0 and isinstance(results, (list,)):
            result["total"] = len(results)

        if results is None:
            result["message"] = "Data Not Found."
            if message:
                result["message"] = message
                # else:
        #     result["response"]      = True

    if total == -1:
        result.pop('total', None)
    if message is None:
        result.pop('message', None)
    return result


def get_var_datatype(var):
    if var is None:
        return None
    return type(var).__name__


def setLabels(is_labelled, result):
    cont = 0
    if is_labelled:
        for idx, val in enumerate(result["results"]):
            cont += 1
            result["results"][idx]['no'] = str(cont)
    return result


def jsonifyResultV2(col, data, stringify_date=False):
    result = []
    for itm in data:
        dt = {}
        i = 0
        for val in itm:
            if stringify_date and str(type(val)) == "<class 'datetime.datetime'>":
                dt[col[i]] = date_to_str(val)
                i = i + 1
            else:
                dt[col[i]] = val
                i = i + 1

        result.append(dt)
    return result


def jsonifyResult(cursor_desc, data):
    # source: https://stackoverflow.com/questions/5010042/mysql-get-column-name-or-alias-from-query
    fields = map(lambda x: x[0], cursor_desc)
    jsonified_data = [dict(zip(fields, row)) for row in data]
    if (len(data) == 0):
        jsonified_data = None
    result = {
        "response": True,
        "total": len(data),
        "results": jsonified_data
    }
    return result


def setQueryLimit(idx, max):
    limit = ''
    if int(max) > 0:
        limit = ' limit ' + str(idx) + ', ' + str(max)
    return limit


def setQueryOptWhere(oldQuery, AddedQuery, varResp):
    opt_sql = ''
    if varResp is not None:
        opt_sql = oldQuery + AddedQuery + "'" + str(varResp) + "'"
    return opt_sql


def get_timestamp(is_str=False, date=None):
    if date is not None:
        tstamp = date.timestamp()
    else:
        tstamp = datetime.now().timestamp()

    if is_str:
        str_ts = str(tstamp).replace('.', '')
        return str_ts
    return tstamp


def get_today(date_format="%Y-%m-%d %H:%M:%S", is_str=True):
    today = datetime.now().strftime(date_format)
    if is_str:
        return today
    else:
        return str_to_date(today, date_format)


def str_to_date(str_date, date_format="%Y-%m-%d %H:%M:%S"):
    return datetime.strptime(str_date, date_format)


def date_to_str(date, date_format="%Y-%m-%d %H:%M:%S"):
    return date.strftime(date_format)


def is_date_valid(str_date, date_format="%Y-%m-%d %H:%M:%S"):  # input: String
    try:
        tryit = str_to_date(str_date, date_format)
        resp = get_json_template(response=True, message="Date is Valid", results=-1, total=-1)
    except ValueError:
        resp = get_json_template(response=False, message="Date is Not Valid", results=-1, total=-1)
    return resp


def get_first_day_of_week(date):
    # isocalendar calculates the year, week of the year, and day of the week.
    # dow is Mon = 1, Sat = 6, Sun = 7
    year, week, dow = date.isocalendar()
    # Find the first day of the week.
    if dow == 7:
        # Since we want to start with Sunday, let's test for that condition.
        first_day_in_this_week = date
    else:
        # Otherwise, subtract `dow` number days to get the first day
        first_day_in_this_week = date - timedelta(dow)
    return first_day_in_this_week


def week_range(date=None, date_format="%Y-%m-%d %H:%M:%S"):
    """Find the first/last day of the week for the given day.
    Assuming weeks start on Sunday and end on Saturday.

    date        : ``String``. 

    date_format : ``String`` ( Default = ``YYYY-mm-dd HH:MM:SS`` ).

    Returns a tuple of ``(start_date, end_date)``.
    """
    if date is None:
        date = str_to_date(datetime.now().strftime('%Y-%m-%d'), date_format)
        # date    = str_to_date(f"{datetime.now():%Y-%m-%d}", date_format) # py3.6++
    else:
        date = str_to_date(date, date_format)

    start_date = get_first_day_of_week(date)
    end_date = start_date + timedelta(6)

    start_date = date_to_str(start_date, date_format)
    end_date = date_to_str(end_date, date_format)
    return {
        "start_date": start_date,
        "end_date": end_date
    }


def prev_week(date=None, date_format="%Y-%m-%d %H:%M:%S"):
    this_week_r = week_range(date=date, date_format=date_format)
    last_week_edate = date_to_str(str_to_date(this_week_r["start_date"], date_format) - timedelta(days=1), date_format)
    return week_range(last_week_edate, date_format)


def is_folder_exist(folder_path):
    return os.path.isdir(folder_path)


def is_file_exist(file_path):
    return os.path.exists(file_path)


def create_new_dir(dir_name):
    os.makedirs(dir_name)


def truncate(logger_file):
    if is_file_exist(logger_file):
        file_size = os.path.getsize(logger_file)
        open(logger_file, 'w').close()


def diff_dates_in_seconds(date_now, date_old):
    return (date_now - date_old).total_seconds()


def diff_dates_in_hours(date_now, date_old):
    secs = diff_dates_in_seconds(date_now, date_old)
    hours = round((secs / 3600), 2)
    return hours


def get_avg(list_data):
    return reduce(lambda x, y: x + y, list_data) / len(list_data)


def get_total(list_data):
    return reduce(lambda x, y: x + y, list_data)


def get_last_n_list_data(data, n_data):
    return data[-(n_data):]


def get_first_n_list_data(data, n_data):
    return data[(n_data):]


def get_operator(str_op):
    if str_op == "<":
        return operator.lt
    elif str_op == ">":
        return operator.gt
    elif str_op == "==":
        return operator.eq
    elif str_op == "!=":
        return operator.ne
    elif str_op == ">=":
        return operator.ge
    elif str_op == "<=":
        return operator.le
    elif str_op == "+":
        return operator.add
    elif str_op == "-":
        return operator.add
    elif str_op == "*":
        return operator.mul
    elif str_op == "/":
        return operator.div
    elif str_op == "%":
        return operator.mod
    elif str_op == "^":
        return operator.xor


def change_rate(cur_val, last_val):
    try:
        if cur_val == last_val:
            return 0.0
        else:
            return round(((last_val - cur_val) / last_val * 100), 2) * -1
    except:
        return cur_val  # e.g. KETIKA last_val = 0; cur_val = 10 (POSITIVE)


def get_last_digit(val):
    res = str(val).replace('.', '')
    last_digit = int(res[-1])
    return last_digit


def remove_1st_index_in_list(list_data):
    list_data.pop(0)
    return list_data


def update_limited_list(list_data, max_list, new_val):
    list_data.append(new_val)

    if len(list_data) > max_list:
        list_data.pop(0)

    return list_data


def count_digit_in_list(list_data, compared_digit):
    total = list_data.count(compared_digit)
    return total


def is_date_expired(exp):
    now = datetime.now()
    timestamp = int(str(datetime.timestamp(now)).split(".")[0])
    # print("NOW(%s) vs EXPIRED(%s)" % (timestamp, exp))
    if timestamp > exp:
        return True
    else:
        return False


def write_to_file(file_path, data):
    try:
        with open(file_path, 'w') as fp:
            json.dump(data, fp)
        return True
    except:
        return False
    # print("now writing to ", file_path, "with @ ", data)


def load_file(file_path):
    try:
        if is_file_exist(file_path):
            with open(file_path, 'r') as file:
                return file.read().replace('\n', '')
    except:
        pass
    return None


def delete_file(file_path):
    try:
        os.remove(file_path)
    except:
        pass
    return None


def sqlresp_to_dict(obj):
    result = []
    if isinstance(obj, (list,)):
        for data in obj:
            result.append(
                {c.key: str(getattr(data, c.key))
                 for c in inspect(data).mapper.column_attrs}
            )
    else:
        result = {c.key: str(getattr(obj, c.key))
                  for c in inspect(obj).mapper.column_attrs}
    return result


def sql_to_dict_resp(obj):
    result = get_json_template()
    data = sqlresp_to_dict(obj)

    if (len(data) > 0):
        result["response"] = True
        result["results"] = data
        result["total"] = len(data)

    return result

# data = [0.02, 0.02, -0.35, 0.02, -2.1, 0.02, 0.02]
# total = get_total(data)
# print(total)

# val = 242.5713
# last_digit = get_last_digit(val)
# print(last_digit)

# numbers = [1, 2, -3, 3, -7, 5, 4, 1, 4, 5]
# numbers.pop(0)
# total = numbers.count(1)
# print(total)
# print(numbers)

# date_format     = "%H"
# cur_hour = int(date_to_str(datetime.now(), date_format))

# print(cur_hour)

# numbers = [1, 2, -3, 3, -7, 5, 4, -1, 4, 5]
# hasil = sum(1 for number in numbers if number < 0)
# print(hasil)

# tick_list = [-6.0, 2.0, 8.0, 0.0, 0.0, -12.0, -2.0, -10.0]
# # print(tick_list[-6])
# total_negatives = sum(1 for negt in tick_list[-6:] if negt < 0.0) 
# print(total_negatives)

# # data = [-38.0, -42.0, -24.0, -34.0]
# data = [{'value': 4.0, 'tick': 4}, {'value': 16.0, 'tick': 5}, {'value': 18.0, 'tick': 6}, {'value': 30.0, 'tick': 7}, {'value': 16.0, 'tick': 8}, {'value': 22.0, 'tick': 9}, {'value': 8.0, 'tick': 10}, {'value': 26.0, 'tick': 11}, {'value': 16.0, 'tick': 12}, {'value': 2.0, 'tick': 13}, {'value': 2.0, 'tick': 26}, {'value': 22.0, 'tick': 27}]

# items = []
# for itm in data:
#     val = itm["value"]
#     items.append(val)

# print(get_avg(items))

# last_val = -14
# cur_val = -5

# rate = change_rate(cur_val, last_val)
# print(rate)

# -0.03 = -22 %

# listd = [1,2,3,10]

# print(get_total(listd))

# date_format     = "%Y-%m-%d %H:%M:%S"
# date_now        = str_to_date(date_to_str(datetime.now(), date_format), date_format)
# date_old        = str_to_date("2019-01-22 16:23:13", date_format)
# print("this date = " + str(date_now))
# print("date_old = " + str(date_old))

# diff_in_sec = (date_now-date_old).total_seconds()
# print("diff_in_sec = " + str(diff_in_sec))

# date_format     = "%Y-%m-%d"
# date            = "2019-01-14"
# print("this date = " + str(date))
# print("this week = ")
# print(week_range(date, date_format))
# print(week_range(date_format=date_format))
# print("prev_week = ")
# print(prev_week(date_format=date_format))
# print("this_week @ " + str(date))
# print(week_range(date=date, date_format=date_format))
# print("prev_week @ " + str(date))
# print(prev_week(date=date, date_format=date_format))
