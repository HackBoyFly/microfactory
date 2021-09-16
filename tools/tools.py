from benedict import benedict  
import re

def dictSelector(d, key_list):
    out = {}
    # if not already benedict, convert elese keep
    bd = benedict(d) if not isinstance(d, benedict) else d
    # Loop all possible keys
    for bKey in  bd.keypaths(indexes=True):
        # Create clean key stripped from indexes
        cKey = re.sub(r'\[\d\]','',bKey)
        # Check if clean key in key_list
        if cKey in key_list:
            # if clean key not in result, add
            if cKey not in out: 
                out[cKey] = []
            # Append bKey to clean key object list
            out[cKey].append(bKey)

    return out
