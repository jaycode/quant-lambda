OWNERSHIP_STRUCTURES = 0
LOCAL_MF_OWNERSHIPS = 1
CASH_LEVELS = 2

def check_sheet_type(key):
    if 'ownership_structures' in key or \
       'ownership structure' in key.lower():
        return OWNERSHIP_STRUCTURES
    elif 'local_mf_ownerships' in key or \
       'local mf ownership' in key.lower():
        return LOCAL_MF_OWNERSHIPS
    elif 'cash_levels' in key or \
        'cash level' in key.lower():
        return CASH_LEVELS
    else:
    	return None