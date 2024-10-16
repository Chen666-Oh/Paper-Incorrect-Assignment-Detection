import argparse
import json
import logging
from os.path import join

import numpy as np
from sklearn.metrics import roc_auc_score, average_precision_score, accuracy_score, f1_score

'''
System evaluation script execution command:
python eval_test_ind.py -hp ind_valid_author_submit.json -rf ind_valid_author_ground_truth.json -l tmp_log.txt
python your_script.py -hp hypothesis.csv -rf reference.csv -l result.log
Where: your_script.py -hp [Submission File] -rf [Answer File] -l [Result File]
The format of the result file: A) If the evaluation is successful, write the score and additional information separated by ### (three hashes) into the result file. e.g. 0.938100
Please note: We currently only accept Python 3 scripts.
'''

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


def load_json(rfdir, rfname):
    logger.info('loading %s ...', rfname)
    with open(join(rfdir, rfname), 'r', encoding='utf-8') as rf:
        data = json.load(rf)
        logger.info('%s loaded', rfname)
        return data


def format_check(submit_fname, gt_fname):
    data_dir = "./"
    flag = True
    info_json = {"err_code": 0, "err_msg": "[success] submission success"}

    try:
        data_dict = load_json(data_dir, submit_fname)
    except Exception as e:
        with open(args.l, "w", encoding="utf-8") as f:
            error_code = 1
            err_msg = "JSON load error"
            other_info = str(e)
            info_json = {"error_code": error_code, "err_msg": err_msg, "other_info": other_info}
            return False, info_json

    labels_dict = load_json(data_dir, gt_fname)

    for aid in labels_dict:
        cur_normal_data = labels_dict[aid]["normal_data"]
        cur_outliers = labels_dict[aid]["outliers"]
        for item in cur_normal_data + cur_outliers:
            if aid not in data_dict:
                error_code = 2
                err_msg = "Author ID not in submission file"
                other_info = "Author ID: " + aid
                info_json = {"error_code": error_code, "err_msg": err_msg, "other_info": other_info}
                return False, info_json
            elif item not in data_dict[aid]:
                error_code = 3
                err_msg = "Paper ID not in author profile in submission file"
                other_info = "Author ID: " + aid + " Paper ID: " + item
                info_json = {"error_code": error_code, "err_msg": err_msg, "other_info": other_info}
                return False, info_json
            else:
                try:
                    v = float(data_dict[aid][item])
                except Exception as e:
                    error_code = 4
                    err_msg = "Value error (Not a number)"
                    other_info = "Author ID: " + aid + " Paper ID: " + item
                    info_json = {"error_code": error_code, "err_msg": err_msg, "other_info": other_info}
                    return False, info_json

    return flag, info_json


def weighted_metric(pred_score, label):
    num_pred = [len(i) for i in pred_score]
    num_label = [len(i) for i in label]
    assert all(a == b for a, b in zip(num_pred, num_label))

    pred_label = []
    for i in pred_score:
        pred_label.append([1 if j >= 0.5 else 0 for j in i])

    acc_pred = [accuracy_score(l, p) for l, p in zip(label, pred_label)]
    f1_pred = [f1_score(l, p) for l, p in zip(label, pred_label)]
    ap = [average_precision_score(l, p) for l, p in zip(label, pred_score)]
    auc = [roc_auc_score(l, p) for l, p in zip(label, pred_score)]

    profile_metric = list(zip(auc, ap, acc_pred, f1_pred))

    num0 = np.array([i.count(0) for i in label])
    weight = num0 / np.array(num0.sum())

    mean_AUC = sum(weight * auc)
    mAP = sum(weight * ap)
    weighted_acc = sum(weight * acc_pred)
    weighted_f1 = sum(weight * f1_pred)

    return mean_AUC, mAP, weighted_acc, weighted_f1, profile_metric


def compute_metric(ground_truth, res):
    pred_list = []
    label_list = []

    for author, pubs in ground_truth.items():
        sub_res = res[author]
        keys = pubs['normal_data'] + pubs['outliers']
        res_keys = list(res[author].keys())
        assert set(keys) == set(res_keys)

        label = [1] * len(pubs['normal_data']) + [0] * len(pubs['outliers'])
        pred = [res[author][i] for i in keys]

        pred_list.append(pred)
        label_list.append(label)

    mean_AUC, mAP, acc, f1, profile_metric = weighted_metric(pred_list, label_list)

    res = zip(ground_truth.keys(), profile_metric)
    with open('metric_pair.json', 'w') as f:
        json.dump(list(res), f)

    return mean_AUC, mAP, acc, f1


def cal_overall_auc(submit_fname, gt_fname, log_fname):
    data_dir = "./"
    flag, info_json = format_check(submit_fname, gt_fname)
    if not flag:
        with open(log_fname, "w", encoding="utf-8") as f:
            f.writelines(str(info_json))
        return 0

    data_dict = load_json(data_dir, submit_fname)
    labels_dict = load_json(data_dir, gt_fname)

    mean_AUC, mAP, acc, f1 = compute_metric(labels_dict, data_dict)

    with open(log_fname, "w", encoding="utf-8") as f:
        f.writelines(f"mean_AUC: {mean_AUC}, mAP: {mAP}, accuracy: {acc}, F1: {f1}###submission success")
    return 0


parser = argparse.ArgumentParser(description='Test for argparse')
parser.add_argument('-hp', help='Submission file')
parser.add_argument('-rf', help='Answer file')
parser.add_argument('-l', help='Result file')
args = parser.parse_args()

if __name__ == "__main__":
    try:
        auc = cal_overall_auc(args.hp, args.rf, args.l)
        print(auc)
    except Exception as e:
        with open(args.l, "w", encoding="utf-8") as f:
            f.write(str(e))
