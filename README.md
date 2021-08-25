# dcase2021_task2_evaluator
The **dcase2021_task2_evaluator** is a script for calculating the AUC, pAUC, precision, recall, and F1 scores from the anomaly score list for the [evaluation dataset](https://zenodo.org/record/4884786) in DCASE 2021 Challenge Task 2 "Unsupervised Anomalous Sound Detection for Machine Condition Monitoring under Domain Shifted Conditions".

http://dcase.community/challenge2021/task-unsupervised-detection-of-anomalous-sounds

## Description

The **dcase2021_task2_evaluator** consists of only one script:
- `dcase2021_task2_evaluator.py`
    - This script outputs the AUC and pAUC scores by using: 
      - Ground truth of the normal and anomaly labels
      - Anomaly scores for each wave file listed in the csv file for each macine type, section, and domain
      - Detection results for each wave file listed in the csv file for each macine type, section, and domain

## Usage
### 1. Clone repository
Clone this repository from Github.

### 2. Prepare data
- Ground truth
    - Download the ground truth included in this repository (the directory `ground_truth_data`)
- Anomaly scores
    - Generate csv files `anomaly_score_<machine_type>_section_<section_index>_<domain>_test.csv` and `decision_result_<machine_type>_section_<section_index>_<domain>_test.csv` by using a system for the [evaluation dataset](https://zenodo.org/record/4884786). (The format information is described [here](http://dcase.community/challenge2021/task-unsupervised-detection-of-anomalous-sounds#submission).) 
- Rename the directory containing the csv files to a team name
- Move the directory into `./teams/`

### 3. Check directory structure
- ./dcase2021_task2_evaluator
    - /dcase2021_task2_evaluator.py
    - /ground_truth_data
        - ground_truth_fan_section_03_source_test.csv
        - ground_truth_fan_section_03_target_test.csv
        - ...
    - /teams
        - /<team_name_1>
            - anomaly_score_fan_section_03_source_test.csv
            - anomaly_score_fan_section_03_target_test.csv
            - ...
            - decision_result_valve_section_05_source_test.csv
            - decision_result_valve_section_05_target_test.csv
        - /<team_name_2>
            - anomaly_score_fan_section_03_source_test.csv
            - anomaly_score_fan_section_03_target_test.csv
            - ...
            - decision_result_valve_section_05_source_test.csv
            - decision_result_valve_section_05_target_test.csv
        - ...
    - /teams_result
        - *<team_name_1>_result.csv*
        - *<team_name_2>_result.csv*
        - ...
    - /README.md


### 4. Change parameters
The parameters are defined in the script `dcase2021_task2_evaluator.py` as follows.
- **MAX_FPR**
    - The FPR threshold for pAUC : default 0.1
- **RESULT_DIR**
    - The output directory : default `./teams_result/`

### 5. Run script
Run the script `dcase2021_task2_evaluator.py`
```
$ python dcase2021_task2_evaluator.py
```
The script `dcase2021_task2_evaluator.py` calculates the AUC, pAUC, precision, recall, and F1 scores for each machine type, section, and domain and output the calculated scores into the csv files (`<team_name_1>_result.csv`, `<team_name_2>_result.csv`, ...) in **RESULT_DIR** (default: `./teams_result/`).

### 6. Check results
You can check the AUC, pAUC, precision, recall, and F1 scores in the `<team_name_N>_result.csv` in **RESULT_DIR**.
The AUC, pAUC, precision, recall, and F1 scores for each machine type, section, and domain are listed as follows:

`result_<team_name_N>.csv`
```
fan
section,domain,AUC,pAUC,precision,recall,F1 score
03,source,0.6669,0.5273684210526316,0.6458333333333334,0.31,0.41891891891891897
04,source,0.7014,0.52,0.6097560975609756,0.25,0.3546099290780142
05,source,0.5834,0.5352631578947369,0.6041666666666666,0.29,0.3918918918918919
03,target,0.5229,0.49315789473684213,0.44680851063829785,0.21,0.2857142857142857
04,target,0.5357,0.5063157894736842,0.5925925925925926,0.32,0.41558441558441556
05,target,0.448452380952381,0.4805764411027569,0.25,0.2833333333333333,0.265625
arithmetic mean,,0.5764587301587302,0.5104469507101085,0.524859533465311,0.27722222222222226,0.35539074019792105
harmonic mean,,0.5634700058286667,0.5097204125946903,0.46988231547812126,0.27161121188342247,0.3442384874315228

pump
section,domain,AUC,pAUC,precision,recall,F1 score
03,source,0.7691000000000001,0.5810526315789474,0.7333333333333333,0.55,0.6285714285714286
04,source,0.6904,0.52,0.5849056603773585,0.31,0.40522875816993464
05,source,0.6524000000000001,0.5326315789473685,0.6326530612244898,0.31,0.4161073825503356
03,target,0.5727,0.5273684210526316,0.5735294117647058,0.39,0.46428571428571425
04,target,0.5555,0.521578947368421,0.5164835164835165,0.94,0.6666666666666667
05,target,0.6652,0.5468421052631579,0.6727272727272727,0.37,0.4774193548387097
arithmetic mean,,0.6508833333333334,0.5382456140350877,0.6189387093184461,0.47833333333333333,0.5097132175137983
harmonic mean,,0.6430137021761633,0.5374559270729756,0.6109851844715204,0.4109468072022102,0.49138771043892926

...

,,AUC,pAUC,precision,recall,F1 score
"arithmetic mean over all machine types, sections, and domains",,0.5942282426736373,0.5299541719896269,0.5711009241953706,0.3449928942043095,0.40727750568532234
"harmonic mean over all machine types, sections, and domains",,0.5776591410233997,0.527685553045072,0.5382056230057072,0.22529948927941607,0.31763363477051193
```

## 7. Citation
If you use this system, please cite all the following three papers:
- Yohei Kawaguchi, Keisuke Imoto, Yuma Koizumi, Noboru Harada, Daisuke Niizumi, Kota Dohi, Ryo Tanabe, Harsh Purohit, and Takashi Endo, "Description and Discussion on DCASE 2021 Challenge Task 2: Unsupervised Anomalous Sound Detection for Machine Condition Monitoring under Domain Shifted Conditions," in arXiv e-prints: 2106.04492, 2021. [URL](https://arxiv.org/abs/2106.04492)
- Noboru Harada, Daisuke Niizumi, Daiki Takeuchi, Yasunori Ohishi, Masahiro Yasuda, Shoichiro Saito, "ToyADMOS2: Another Dataset of Miniature-Machine Operating Sounds for Anomalous Sound Detection under Domain Shift Conditions," in arXiv e-prints: 2106.02369, 2021. [URL](https://arxiv.org/abs/2106.02369)
- Ryo Tanabe, Harsh Purohit, Kota Dohi, Takashi Endo, Yuki Nikaido, Toshiki Nakamura, and Yohei Kawaguchi, "MIMII DUE: Sound Dataset for Malfunctioning Industrial Machine Investigation and Inspection with Domain Shifts due to Changes in Operational and Environmental Conditions," in arXiv e-prints: 2105.02702, 2021. [URL](https://arxiv.org/abs/2105.02702)
