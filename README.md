
## About

This repositories collects files used to analyze Deep Learning Framework Chainer community.
This project was used in Chainer meetup #7 on 9th June, 2018.
 
## Analyzed result

The analyzed result are assembled into [presentation](./presentation).
The analysis precedure can be found in [repository_analysis.ipynb](./repository_analysis.ipynb).
Note that there are mismatch between the presentation and the notebook right now.
You should visit [presentation tag](https://github.com/koreyou/chainer-usage-analysis/tree/presentation) to confirm the result.

I have included `found_all_*.txt`, list of crawled or sampled repositories that uses deep learning frameworks, to the project.
Also, I have uploaded cloned projects ([Chainer](https://drive.google.com/file/d/1IpCo1DIMgIMC5L87IdV3eAHmYR7pEVsT/view?usp=sharing), [TensorFlow](https://drive.google.com/file/d/1E905ExyOuiuSGmXJ8oaUwRlzCV7tncFq/view?usp=sharing) and [PyTorch](https://drive.google.com/open?id=1E905ExyOuiuSGmXJ8oaUwRlzCV7tncFq)).
*I am redistributing files for research purpose, regarding projects as crawled texts. Please respect each repository's license if you are using the actual code.*

## How to run

### Prerequisite

You need python 2.7 to run the code. Since some code runs shell command, you probably need Linux to run the code.
My environment was Ubuntu 16.04 with Python 2.7.12.

Run following command to install requirements.
```
pip install -r requirements.txt
```

### Create access tokens

You need private access token to have full access to Github search
API.
Generate your access token in [here](https://github.com/settings/tokens)
you don't need to tick on any access permission because you are not
modifying your private repositories.


### Sample or collect project repositories

First, search and retrive project repositories.

For chainer retrive ALL repositories by splitting repositories by their sizes.
It is because GitHub does not have API to let you download all search results at once.

To do so, run following command. Note that it may take few hours to a day to run the command.


```bash
python find_chainer_usage.py
```

It will output `found_all.txt`.

For PyTorch and TensorFlow, we sample some repositories.
Since GitHub does not allow sampling of repositories, I decided I sample few weeks since the those frameworks are created and query for repositories added at that time span.

```bash
python find_other_frameworks_usage.py
```

It will output `found_all_tensorflow.txt` and `found_all_pytorch.txt`.

### Clone found repositoires

Next, clone all the found repositories. Since saving all files result in very large disk consumption, files other than python script and README is deleted.

Note that it may take **about one week**.

```bash
python clone_repos.py --filter chainer found_all.txt repos
python clone_repos.py --filter pytorch found_all_pytorch.txt repos_pytorch
python clone_repos.py --filter tensorflow found_all_tensorflow.txt repos_tensorflow
```

It will produce `repos/`, `repos_pytorch/` and `repos_tensorflow/`, each containing a cloned repository per a directory.

### Run analysis

Open `repository_analysis.ipynb` with jupyter notebook.

