### This program will calculate quality of work of a classifier.
***

#### Usage:
* Install local requirements in addition to [global requirements](../../README.md):
```bash
cd tasks/task_1
pip install -U -r t1_requirements.txt
```
* Run tool:
```bash
./count_quality.py file1 file2
```
	
Where:
- `file1` - File with test samples.
- `file2` - File with correct answers for provided sample.

For example:
- `./count_quality.py ./data/LogisticRegression_pred.csv ./data/test_labels.csv`
- `./count_quality.py ./data/NaiveBayes_pred.csv ./data/test_labels.csv`
