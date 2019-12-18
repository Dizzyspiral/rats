import os
import glob

def get_recent_files(directory, num_hours, num_candidates):
    """
    Gets num_files number of recent files' names from directory, sorts the 
    names by file modified time, and returns them
    """
    num_files = num_hours * num_candidates
    files = list(filter(os.path.isfile, glob.glob(directory + os.sep + "*.json")))
    files.sort(key=lambda x: os.path.getmtime(x))

    # XXX Hack: we don't want to include the most recent hour, as we're still 
    # scraping tweets for it. So we adjust the slicing. This function doesn't 
    # really do what it's described to. Probably we should post-process the 
    # value returned from it instead of hamfisting this in here.
    slice_begin = 0 - num_files - num_candidates
    slice_end = 0 - num_candidates
    recent = files[slice_begin:slice_end]

    return recent
