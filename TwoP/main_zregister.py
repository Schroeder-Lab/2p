# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 08:41:43 2023
This script runs the z-registration over a selected number of files
IMPORTANT: Edit registration_defs to choose which files would be edited and changing the ops
"""
from zregister_function import *
from registration_defs import *
from joblib import Parallel, delayed
from runners import run_single_registration

#
#


dataEntries = directories_to_register()

Parallel(n_jobs=1, verbose=5)(
    delayed(run_single_registration)(dataEntries.iloc[i])
    for i in range(len(dataEntries))
)
