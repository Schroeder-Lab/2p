# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 09:35:05 2022

@author: LABadmin
"""
from suite2p import default_ops
import pandas as pd

# define directories # Change to a different file
def define_directories():
    """
    Creates variables which contain the strings of important directory paths needed for the preprocessing.
    Note that the directory paths specified by the user can be of any shape and does not have to abide by
    the default input seen below (i.e using double backslash).

    Returns
    -------
    csvDir : str ["YourDirectoryPath\preprocess.csv"]
        The preprocess csv file location and name. Ths file has to contain the following information:
           - Name of the Animal.
           - Date of the experiment (YYYY-MM-DD).
           - ZStack directory number (within each experiment, which folder contains the Z stack).
           - IgnorePlanes (which planes to ignore, such as the flyback plane).
           - Save directory (where to save the preprocessed files, if left blank will save in the suite2p folder).
           - Whether to process the specified experiment or not (TRUE or FALSE).
           Please also have a look at the example csv on github (named example_preprocess.csv)
           
    s2pDir : str ["YourDirectoryPath"]
        The main directory where the suite2p folders are located; The assumed folder structure for the 
        subfolders in this directory is: s2pDir\\[animal]\\[date]\\suite2p\\[folders for each plane]\\
            The folders for each plane have to contain these files:
            - Registered movie in the form of a binary file (data.bin). Make sure this is
              present as it is IMPORTANT FOR Z STACK REGISTRATION but bear in mind it is a very large file.
            - Fluorescence traces for each ROI (F.npy).
            - Neuropil traces for each ROI (Fneu.npy).
            - The iscell file which indicates whether an ROI was classified as a cell or not (iscell.npy).
            - The ops file which indicates all the suite2p input settings specified by the user (ops.npy).
            - The stat file which indicates all the suite2p metadata (such as ROI locations in XY plane) (stat.npy).
        
            
    zstackDir : str ["YourDirectoryPath"]
        The main folder where the zStack is located. IMPORTANT Z STACK REGISTRATION
        
    metadataDir : str ["YourDirectoryPath"]
        The main folder where the metadata is located. This should contain:
        - NiDaqInput*.bin : the data from the NiDaq which contains information about: 
          photodiode, frameclock, pockel and piezo feedback and the sync signal to sync with Arduino
        - niDaqChannels*.csv : csv file which contains the names of the NiDaq channels
        - ArduinoInput*.csv : the data from the Arduino which contains information about:
          rotary encoder (forward movement), rotary encoder (backward movement), camera1, camera2 and
          sync signal to sync with NiDaq
        - arduinoChannels*.csv : csv file which contains the names of the Arduino channels  
        - props*.csv : what type of experiment it is and what parameters are used. For example,
          for moving gratings these would be: Ori (orientation), SFreq (spatial frequency), TFreq (temporal frequency)
          and Contrast
          Note: These files should be generated automatically when using the Bonsai scripts within this repository.

    """

    directoryDb = {
        "dataDefFile": "D:\\preprocess.csv",
        "preprocessedDataDir": "Z:\\ProcessedData\\",
        # "preprocessedDataDir": "Z://ProcessedData//",
        "zstackDir": "Z:\\RawData\\",
        "metadataDir": "Z:\\RawData\\",
    }
    return (
        directoryDb  # dataDefFile, preprocessedDataDir, zstackDir, metadataDir
    )


def create_2p_processing_ops():
    """
        Creates the processing settings which includes:
    <<<<<<< Updated upstream
        - debug: Whether or not to debug (if True, lets you see exactly at which
          lines errors occur, but parallel processing won't be done so processing
          will be slower).
        - plot: For each sorted ROI whether to plot the uncorrected, corrected,
        normalised traces, Z location and Z profile.
        - f0_percentile: The F0 percentile which determines which percentile of
        the lowest fluorescence distribution to use.
        - f0_window: The length of the rolling window in time (s) over which to
        calculate F0.
        - zcorrect_mode: The mode of Z correction such as with the Z stack
        ("Stack").
    =======
        - debug: Whether or not to debug (if True, lets you see exactly at which lines errors occur,
          but parallel processing won't be done so processing will be slower).
        - plot: For each sorted ROI whether to plot the uncorrected, corrected, normalised traces,
          Z location and Z profile.
        - f0_percentile: The F0 percentile which determines which percentile of the lowest fluorescence distribution to use.
        - f0_window: The length of the rolling window in time (s) over which to calculate F0.
        - zcorrect_mode: The mode of Z correction such as with the Z stack ("Stack").
    >>>>>>> Stashed changes
        - remove_z_extremes: Whether or not to remove the Z extremes in the traces.
        - absZero: if None takes the default value. If a number that would be the zero for the sessions
        Please note: to change preprocessing settings, change the values in pops
        in this function.
        Returns
        -------
        pops : dictionary [6]
            The dictionary pops which contains all the above mentioned options.


    """
    pops = {
        "debug": True,
        "plot": True,
        "f0_percentile": 8,
        "f0_window": 300,
        "Npil_f0_window": 60,
        "zcorrect_mode": "Stack",
        "remove_z_extremes": False,
        "process_suite2p": False,
        "process_bonsai": True,
        "absZero": None,
    }
    return pops


def create_ephys_processing_ops():
    pass


def create_ops_boutton_registration(filePath):
    ops = default_ops()
    ops["data_path"] = filePath[1:]

    ops["look_one_level_down"] = False
    ops["ignore_flyback"] = [0]
    ops["nchannels"] = 1
    ops["nplanes"] = 8
    ops["functional_chan"] = 1

    # registration ops
    ops["keep_movie_raw"] = True
    ops["align_by_chan"] = 1

    ops["block_size"] = [256, 256]
    ops["nonrigid"] = True
    # run for only X number frames
    # ops['frames_include'] = 1000

    # set save folder
    ops["save_path0"] = filePath[0]

    # localised optioed
    ops["delete_extra_frames"] = False
    ops["run_registration"] = True
    ops["run_detection"] = True

    # detection settings
    ops["allow_overlap"] = True
    ops["max_overlap"] = 0.2
    ops["max_iterations"] = 100

    return ops


def create_fitting_ops():
    ops = {
        "debug": False,
        "plot": True,
        "active_quantile": 0.2,
        "quiet_quantile": 0.01,
        "save_dir": r"D:\fitting_test\plots",
    }

    return ops


def directories_to_register():
    dirDefs = [
        # {
        #     "Name": "Io",
        #     "Date": "2023-02-20",
        #     "Experiments": [1],
        # }
        # {
        #     "Name": "Io",
        #     "Date": "2023-02-15",
        #     "Experiments": [2, 3, 4, 5, 6, 7],
        # },
        # {
        #     "Name": "Io",
        #     "Date": "2023-02-20",
        #     "Experiments": [1, 3, 4, 5, 6, 7],
        # },
        # {
        #     "Name": "Io",
        #     "Date": "2023-05-22",
        #     "Experiments": [2, 3, 4, 5, 6],
        # },
        # {
        #     "Name": "Janus",
        #     "Date": "2023-02-14",
        #     "Experiments": [2, 3, 4, 5, 6, 7],
        # },
        # {
        #     "Name": "Janus",
        #     "Date": "2023-02-22",
        #     "Experiments": [1, 3, 4, 5, 6, 7],
        # },
        ############################
        {
            "Name": "Io",
            "Date": "2023-01-18",
            "Experiments": [1, 2, 3, 4, 5],
        },
        {
            "Name": "Io",
            "Date": "2023-02-01",
            "Experiments": [1, 2, 3, 4, 5],
        },
        {
            "Name": "Io",
            "Date": "2023-02-02",
            "Experiments": [1, 2, 3, 4, 5, 6, 7],
        },
        {
            "Name": "Io",
            "Date": "2023-02-07",
            "Experiments": [1, 2, 3],
        },
        #############################################
    ]
    return pd.DataFrame(dirDefs)


def directories_to_fit():
    # boutons
    dirDefs = [
        # {
        #     "Name": "Io",
        #     "Date": "2023-02-13",
        #     "SpecificNeurons": [],
        # },
        # {"Name": "Io", "Date": "2023-02-15", "SpecificNeurons": []},
        {"Name": "Io", "Date": "2023-02-20", "SpecificNeurons": []},
        # {"Name": "Io", "Date": "2023-05-22", "SpecificNeurons": []},
        # {"Name": "Janus", "Date": "2023-02-14", "SpecificNeurons": []},
        # {"Name": "Janus", "Date": "2023-02-22", "SpecificNeurons": []},
        # # # neurons
        # {"Name": "Giuseppina", "Date": "2023-01-24", "SpecificNeurons": []},
        # # weird updated file for both below
        # {"Name": "Ladon", "Date": "2023-04-17", "SpecificNeurons": []},
        # {"Name": "Lotho", "Date": "2023-04-18", "SpecificNeurons": []},
        # # done
        # {"Name": "Ladon", "Date": "2023-07-07", "SpecificNeurons": []},
        # {"Name": "Giuseppina", "Date": "2023-01-06", "SpecificNeurons": []},
        # {"Name": "Lotho", "Date": "2023-04-12", "SpecificNeurons": []},
        # ### to much running
        # # weird updated file for both below
        # {"Name": "Lotho", "Date": "2023-04-18", "SpecificNeurons": []},
        # {
        #     "Name": "Lotho",
        #     "Date": "2023-04-20",
        # },
        # # done
        # {"Name": "Giuseppina", "Date": "2023-01-06", "SpecificNeurons": []},
        # {"Name": "Lotho", "Date": "2023-04-12", "SpecificNeurons": []},
        # {"Name": "Quille", "Date": "2023-07-24", "SpecificNeurons": []},
        # {"Name": "Quille", "Date": "2023-08-24", "SpecificNeurons": []},
        # {"Name": "Quille", "Date": "2023-09-07", "SpecificNeurons": []},
    ]

    return dirDefs


def get_sparsenoise_info():
    session = pd.DataFrame(
        [
            {
                "Name": "Giuseppina",
                "Date": "2023-05-11",
                "Experiments": [4],
                "Plane": 1,
            }
        ]
    ).iloc[0]

    tempDir = "D:\\sparseTemp\\"
    return session, tempDir
