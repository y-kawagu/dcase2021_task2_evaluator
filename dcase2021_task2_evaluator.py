import os
import sys
import csv
import glob
import re
import numpy
import itertools
import scipy.stats
from sklearn import metrics

##############################################################################
# static values
##############################################################################
# Expected directory structure
# ./dcase2021_evaluator/
#       ./teams "Directory containing team results"
#               ./<team name> "Directory containing anomaly score and decision result"
#       ./ground_truth_data "Directory where the true value is stored"
#       ./teams_result "Directory created after execution."

# directory path
TEAMS_ROOT_DIR = "./teams"
RESULT_DIR = "./teams_result"
GROUND_TRUTH_DATA_DIR = "./ground_truth_data"

# variables that do not change
DOMAINS = ["source_test", "target_test"]
MAX_FPR = 0.1
SCORE_COL = 1

##############################################################################
# common def
##############################################################################
# save csv
def save_csv(save_file_path, save_data):
    with open(save_file_path, "w", newline="") as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(save_data)

# extract machine types from ground truth
def get_machines(load_dir, ext=".csv"):
    query = os.path.abspath("{base}/ground_truth_*{ext}".format(base=load_dir,
                                                                ext=ext))
    machines = sorted(glob.glob(query))
    machines = [os.path.basename(f).split("_")[2] for f in machines]
    machines = sorted(list(set(machines)))
    return machines

# extract section id from anomaly score csv
def get_section_ids(target_dir, ext=".csv"):
    query = os.path.abspath("{target_dir}/ground_truth_*{ext}".format(target_dir=target_dir,
                                                                      ext=ext))
    paths = sorted(glob.glob(query))
    ids = sorted(list(set(itertools.chain.from_iterable(
        [re.findall('section_[0-9][0-9]', ext_id) for ext_id in paths]
    ))))
    return ids

# read score from csv
def read_score(file_path):
    with open(file_path) as score_file:
        score_list = list(csv.reader(score_file))
    score_data = [float(score[SCORE_COL]) for score in sorted(score_list)]

    return score_data

# [main] output the result from the specified directory and machine type
def output_result(target_dir, machines, section_ids):
    print(target_dir)
    csv_lines = []
    performance_over_all = []
    for machine_idx, target_machine in enumerate(machines):
        print("[{idx}/{total}] machine type : {target_machine}".format(target_machine=target_machine,
                                                                       idx=machine_idx+1,
                                                                       total=len(machines)))
        csv_lines.append([target_machine])
        csv_lines.append(["section", "domain", "AUC", "pAUC", "precision", "recall", "F1 score"])
        performance = []
        for domain in DOMAINS:
            print("===", domain, "===")
            for section_id in section_ids:
                print(section_id)
                # y_pred y_true_decision load
                # append AUC and pAUC to lists
                anomaly_score_path = "{dir}/anomaly_score_{machine}_{section}_{domain}.csv".format(dir=target_dir,
                                                                                                   machine=target_machine,
                                                                                                   section=section_id,
                                                                                                   domain=domain)
                decision_result_path = "{dir}/decision_result_{machine}_{section}_{domain}.csv".format(dir=target_dir,
                                                                                                       machine=target_machine,
                                                                                                       section=section_id,
                                                                                                       domain=domain)
                ground_truth_path = "{dir}/ground_truth_{machine}_{section}_{domain}.csv".format(dir=GROUND_TRUTH_DATA_DIR,
                                                                                                 machine=target_machine,
                                                                                                 section=section_id,
                                                                                                 domain=domain)

                y_pred = read_score(os.path.abspath(anomaly_score_path))
                y_true = read_score(os.path.abspath(ground_truth_path))
                decision_result_data = read_score(os.path.abspath(decision_result_path))

                if len(y_true) != len(y_pred) or len(y_true) != len(decision_result_data):
                    print("number of reference elements:", len(y_true))
                    print("anomaly score element count:", len(y_pred), " path:", anomaly_score_path)
                    print("decision data element count:", len(decision_result_data), " path:", decision_result_path)
                    print("some elements are missing")
                    return -1

                # calc result
                print("\n================= START OF EVALUATION FOR A SECTION ==================\n")
                auc = metrics.roc_auc_score(y_true, y_pred)
                p_auc = metrics.roc_auc_score(y_true, y_pred, max_fpr=MAX_FPR)
                tn, fp, fn, tp = metrics.confusion_matrix(y_true, decision_result_data).ravel()
                prec = tp / numpy.maximum(tp + fp, sys.float_info.epsilon)
                recall = tp / numpy.maximum(tp + fn, sys.float_info.epsilon)
                f1 = 2.0 * prec * recall / numpy.maximum(prec + recall, sys.float_info.epsilon)
                csv_lines.append([section_id.split("_", 1)[1], domain.split("_", 1)[0], auc, p_auc, prec, recall, f1])
                performance.append([auc, p_auc, prec, recall, f1])
                performance_over_all.append([auc, p_auc, prec, recall, f1])
                print("AUC : {}".format(auc))
                print("pAUC : {}".format(p_auc))
                print("precision : {}".format(prec))
                print("recall : {}".format(recall))
                print("F1 score : {}".format(f1))
                print("\n================= END OF EVALUATION FOR A SECTION ==================\n\n")

        amean_performance = numpy.mean(numpy.array(performance, dtype=float), axis=0)
        csv_lines.append(["arithmetic mean", ""] + list(amean_performance))
        hmean_performance = scipy.stats.hmean(numpy.maximum(numpy.array(performance, dtype=float), sys.float_info.epsilon), axis=0)
        csv_lines.append(["harmonic mean", ""] + list(hmean_performance))
        csv_lines.append([])

    csv_lines.append(["", "", "AUC", "pAUC", "precision", "recall", "F1 score"])
    # calculate averages for AUCs and pAUCs
    amean_performance = numpy.mean(numpy.array(performance_over_all, dtype=float), axis=0)
    csv_lines.append(["arithmetic mean over all machine types, sections, and domains", ""] + list(amean_performance))
    hmean_performance = scipy.stats.hmean(numpy.maximum(numpy.array(performance_over_all, dtype=float), sys.float_info.epsilon), axis=0)
    csv_lines.append(["harmonic mean over all machine types, sections, and domains", ""] + list(hmean_performance))
    csv_lines.append([])

    # output results
    os.makedirs(RESULT_DIR, exist_ok=True)
    result_file_path = "{result_dir}/{target_dir}_result.csv".format(result_dir=RESULT_DIR,
                                                                     target_dir=os.path.basename(target_dir))
    print("results -> {}".format(result_file_path))
    save_csv(save_file_path=result_file_path, save_data=csv_lines)
    return 0


##############################################################################
# main
##############################################################################
if __name__ == "__main__":
    machine_types = get_machines(load_dir=GROUND_TRUTH_DATA_DIR)
    section_ids = get_section_ids(target_dir=GROUND_TRUTH_DATA_DIR)

    team_dirs = glob.glob("{root_dir}/*".format(root_dir=TEAMS_ROOT_DIR))
    if os.path.isdir(RESULT_DIR):
        print("the result directory exist")
        sys.exit(-1)

    for idx, team_dir in enumerate(team_dirs):
        print("[{idx}/{total}] team name : {team_dir}".format(team_dir=os.path.basename(team_dir),
                                                              idx=idx+1,
                                                              total=len(team_dirs)))
        if os.path.isdir(team_dir):
            normal_end_flag = output_result(team_dir, machine_types, section_ids)
            if normal_end_flag == -1:
                print("abnormal termination")
                sys.exit(-1)
        else:
            print("{} is not directory.".format(team_dir))


