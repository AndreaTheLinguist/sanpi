
# Running `script/makeTable.sh`
_Checking for required packages..._
```
pyconll package not found:
pip3 install pyconll
Requirement already satisfied: pyconll in /home/andrea/anaconda3/lib/python3.8/site-packages (2.3.3)
Requirement already satisfied: requests>=2.21 in /home/andrea/anaconda3/lib/python3.8/site-packages (from pyconll) (2.25.1)
Requirement already satisfied: certifi>=2017.4.17 in /home/andrea/anaconda3/lib/python3.8/site-packages (from requests>=2.21->pyconll) (2021.5.30)
Requirement already satisfied: idna<3,>=2.5 in /home/andrea/anaconda3/lib/python3.8/site-packages (from requests>=2.21->pyconll) (2.10)
Requirement already satisfied: urllib3<1.27,>=1.21.1 in /home/andrea/anaconda3/lib/python3.8/site-packages (from requests>=2.21->pyconll) (1.26.6)
Requirement already satisfied: chardet<5,>=3.0.2 in /home/andrea/anaconda3/lib/python3.8/site-packages (from requests>=2.21->pyconll) (4.0.0)
 
pandas package not found:
pip3 install pandas
Requirement already satisfied: pandas in /home/andrea/anaconda3/lib/python3.8/site-packages (1.3.0)
Requirement already satisfied: numpy>=1.17.3 in /home/andrea/anaconda3/lib/python3.8/site-packages (from pandas) (1.20.3)
Requirement already satisfied: python-dateutil>=2.7.3 in /home/andrea/.local/lib/python3.8/site-packages (from pandas) (2.8.1)
Requirement already satisfied: pytz>=2017.3 in /home/andrea/anaconda3/lib/python3.8/site-packages (from pandas) (2021.1)
Requirement already satisfied: six>=1.5 in /home/andrea/anaconda3/lib/python3.8/site-packages (from python-dateutil>=2.7.3->pandas) (1.16.0)
```
## >> Searching `quicktest.conll/` for `devel` patterns
 
- started by: `andrea`
- run from: `/home/andrea/litotes`
- timestamp: `Tue Aug  3 10:34:53 EDT 2021`
 
```
Output directory data/devel already exists and contains these relevant files:
data/devel/quicktest.try_this/nyt_eng_199912.json
data/devel/quicktest.try_this/nyt_eng_199912.raw.json
 
* If pattern or corpus files have not changed since these files were created, skipping the grew corpus search is recommended (n).
 
--> Run grew search on quicktest again and overwrite any corresponding files? y/n 