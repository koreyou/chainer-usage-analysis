import re
from langdetect import detect
import fnmatch
import os
from collections import Counter

texts = open("repos/5/FewShotRecommend/models.py").read()           
list(re.findall(r"class ([^\(]*)\([^\)]*Chain", texts))

functions = [
  "leaky_relu",
  "relu",
]

def recursive_glob(base_path, ext):
    # recursive globbing is only available from 3.5>
    matches = []
    ext = "*.%s" % ext
    for root, dirnames, filenames in os.walk(base_path):
        for filename in fnmatch.filter(filenames, ext):
            matches.append(os.path.join(root, filename))
    return matches


def count(keywords, paths):
    re_pats = {k: re.compile("[^a-zA-Z0-9_]%s\(" % k) for k in keywords}
    counts = Counter({k: 0 for k in keywords})
    for path in paths:
        if os.path.islink(path):
            continue
        with open(path) as fin:
            text = fin.read()
        counts += Counter({
            k: len(pat.findall(text))
            for k, pat in re_pats.items()
        })
    return counts

count(functions, recursive_glob("repos/106", "py")) 

def has_pat(re_pat, paths):
    for path in paths:
        if os.path.islink(path):
            continue
        with open(path) as fin:
            text = fin.read()
        if re_pat.find(text):
            return True
    return False

has_pat(r"(import)|(from) *chainer", recursive_glob("repos/106", "py"))

detect(texts)

# likes
# users
# posts per users

import glob

cnt = 0
chainer_repos = []
for i in range(3313):
    if not has_pat(r"(import)|(from) *chainer", recursive_glob("repos/%d" % i,"py")):
    #print(i)
    cnt += 1
    chainer_repos.append(i)
print(cnt)

for path in glob("repos/*"):
    with open(os.path.join(path, "api.json")) as fin:
        api_json = json.load(fin)

function_names = [
    "clipped_relu",
    "crelu",
    "elu",
    "hard_sigmoid",
    "leaky_relu",
    "log_softmax",
    "lstm",
    "maxout",
    "prelu",
    "relu",
    "selu",
    "sigmoid",
    "slstm",
    "softmax",
    "softplus",
    "swish",
    "tanh",
    "tree_lstm",
    "broadcast",
    "broadcast_to",
    "cast",
    "concat",
    "copy",
    "depth2space",
    "dstack",
    "expand_dims",
    "flatten",
    "flip",
    "fliplr",
    "flipud",
    "get_item",
    "hstack",
    "im2col",
    "pad",
    "pad_sequence",
    "permutate",
    "repeat",
    "reshape",
    "resize_images",
    "rollaxis",
    "scatter_add",
    "select_item",
    "separate",
    "space2depth",
    "spatial_transformer_grid",
    "spatial_transformer_sampler",
    "split_axis",
    "squeeze",
    "stack",
    "swapaxes",
    "tile",
    "transpose",
    "transpose_sequence",
    "vstack",
    "where",
    "bilinear",
    "convolution_2d",
    "convolution_nd",
    "deconvolution_2d",
    "deconvolution_nd",
    "depthwise_convolution_2d",
    "dilated_convolution_2d",
    "embed_id",
    "linear",
    "local_convolution_2d",
    "n_step_bigru",
    "n_step_bilstm",
    "n_step_birnn",
    "n_step_gru",
    "n_step_lstm",
    "n_step_rnn",
    "shift",
    "accuracy",
    "binary_accuracy",
    "classification_summary",
    "f1_score",
    "precision",
    "r2_score",
    "recall",
    "absolute_error",
    "bernoulli_nll",
    "black_out",
    "connectionist_temporal_classification",
    "contrastive",
    "crf1d",
    "argmax_crf1d",
    "cross_covariance",
    "decov",
    "gaussian_kl_divergence",
    "gaussian_nll",
    "hinge",
    "huber_loss",
    "mean_absolute_error",
    "mean_squared_error",
    "negative_sampling",
    "sigmoid_cross_entropy",
    "softmax_cross_entropy",
    "squared_error",
    "triplet",
    "absolute",
    "arccos",
    "arcsin",
    "arctan",
    "arctan2",
    "argmax",
    "argmin",
    "average",
    "batch_inv",
    "batch_l2_norm_squared",
    "batch_matmul",
]


   chainer.function_hooks.CUDAProfileHook
   chainer.function_hooks.CupyMemoryProfileHook
   chainer.function_hooks.PrintHook
   chainer.function_hooks.TimerHook
