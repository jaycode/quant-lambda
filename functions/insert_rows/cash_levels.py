from log_helper import *
import queries as q
FILE_XLS = 0
FILE_XLSX = 1

def find_cell(sheet, key, max_row=10, max_col=10):
    # Find a cell in a search space (max_row and max_col)
    col_idx = 0
    row_idx = 1
    found = False
    for row in sheet.iter_rows(min_row=1, min_col=0, max_col=max_col, max_row=max_row, values_only=True):
        for i in range(max_col):
            col_idx = i
            if str(row[i]).strip() == key:
                found = True
                break
        if found:
            break
        row_idx += 1
    return (row_idx, col_idx+1)


def insert_cl(sheet, file_type):
    insert_str = ""
    inputs = []
    num_fields = 9
    if file_type == FILE_XLS:
        log_err('XLS not implemented. Please upload an XLSX file instead.')
    elif file_type == FILE_XLSX:
        row_idx, col_idx = find_cell(sheet, 'Date', max_row=5, max_col=5)
        row_idx += 1
        for row in sheet.iter_rows(min_row=row_idx, min_col=col_idx, max_col=col_idx+num_fields-1, values_only=True):
            row = list(row)
            row[0] = row[0].strftime('%Y-%m-01')
            inputs.extend(row)
            newrow_str = "(" + ", ".join(['%s']*len(row)) + ")"
            insert_str += newrow_str + ", \n"
            row_idx += 1
        insert_str = insert_str[:-3]
        insert_str = q.insert_cl_rows.format(insert_str)
        print(inputs)
    return (insert_str, inputs)
