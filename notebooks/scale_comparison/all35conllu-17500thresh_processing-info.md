running slurm script: /share/compling/projects/sanpi/slurm/compare-adv-by-scale.slurm.sh
JOB ID: 222753
JOB NAME: scale-compare
started @ 2023-04-19 20:14:28 from /share/compling/projects/sanpi/notebooks/scale_comparison/logs
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
running on luxlab-cpu-03 with 1 cores
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
time python $PROG $N_FILES
time python /share/compling/projects/sanpi/notebooks/scale_comparison/compare-adv-by-scale.py 35
Comparing Adverbs by Scale Type for:
35 files & a frequency threshold of 17500

## loading data...
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-PccVa_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-PccTe_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Apw_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Nyt1_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc06_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc19_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc18_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc08_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc12_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc20_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc23_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc00_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc16_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc22_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc24_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc05_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc03_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc28_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc04_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc01_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc09_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc17_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc11_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc25_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc07_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc10_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc21_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc14_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc02_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc29_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc13_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc15_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc27_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Pcc26_all-RB-JJs_hits.pkl.gz
  + ../sanpi/2_hit_tables/advadj/with-context/bigram-Nyt2_all-RB-JJs_hits.pkl.gz
  > Time to create composite hits dataframe via loop: 00:29:06.97
removing duplicates
| scale_type   |   % of selection |
|:-------------|-----------------:|
| OPEN         |             79.3 |
| UP_CLOSE     |              7.2 |
| TOT_CLOSE    |              6   |
| LOW_CLOSE    |              5.1 |
| NON_G        |              2.5 |
| adv_lemma       |   NON_G |   OPEN |   LOW_CLOSE |   UP_CLOSE |   TOT_CLOSE |   total_ratio |   total_count |
|:----------------|--------:|-------:|------------:|-----------:|------------:|--------------:|--------------:|
| very            |   0.106 |  1.122 |       0.756 |      0.691 |       0.34  |         0.19  |       1206032 |
| too             |   0.026 |  1.174 |       0.716 |      0.271 |       0.219 |         0.094 |        594880 |
| much            |   0.778 |  1.174 |       0.042 |      0.561 |       0.125 |         0.073 |        465197 |
| so              |   0.341 |  1.063 |       0.673 |      0.715 |       1.067 |         0.062 |        393336 |
| as              |   0.377 |  1.027 |       0.71  |      1.505 |       0.55  |         0.061 |        388004 |
| more            |   0.91  |  0.661 |       2.842 |      1.428 |       3.459 |         0.055 |        351276 |
| not             |   3.714 |  0.754 |       0.677 |      2.494 |       1.599 |         0.039 |        246366 |
| relatively      |   0.006 |  1.162 |       0.032 |      0.918 |       0.195 |         0.032 |        202847 |
| really          |   0.586 |  1.134 |       0.559 |      0.573 |       0.284 |         0.032 |        202321 |
| most            |   0.352 |  0.681 |       5.947 |      1.552 |       0.666 |         0.031 |        197244 |
| even            |   0.411 |  1.185 |       0.399 |      0.296 |       0.157 |         0.03  |        189681 |
| pretty          |   0.18  |  1.067 |       0.366 |      1.254 |       0.684 |         0.023 |        143045 |
| still           |  16.867 |  0.451 |       1.013 |      0.397 |       2.294 |         0.022 |        139995 |
| extremely       |   0.041 |  1.061 |       1.934 |      0.725 |       0.145 |         0.022 |        137965 |
| quite           |   0.563 |  1.048 |       0.856 |      0.939 |       0.738 |         0.014 |         91140 |
| less            |   0.182 |  0.969 |       1.495 |      1.53  |       0.707 |         0.014 |         86282 |
| slightly        |   0.032 |  1.155 |       0.791 |      0.234 |       0.444 |         0.012 |         77757 |
| fairly          |   0.032 |  1.066 |       0.152 |      1.55  |       0.592 |         0.01  |         63664 |
| far             |   0.02  |  1.209 |       0.053 |      0.496 |       0.046 |         0.01  |         60785 |
| significantly   |   0.003 |  1.246 |       0.034 |      0.148 |       0.007 |         0.009 |         56186 |
| also            |   1.215 |  0.813 |       0.935 |      1.152 |       3.248 |         0.009 |         55361 |
| how             |   0.088 |  1.104 |       0.678 |      0.966 |       0.32  |         0.009 |         54755 |
| now             |   6.47  |  0.238 |       0.18  |      2.405 |       7.786 |         0.008 |         49581 |
| rather          |   0.096 |  1.142 |       0.55  |      0.536 |       0.435 |         0.008 |         47859 |
| incredibly      |   0.056 |  1.086 |       1.234 |      0.824 |       0.27  |         0.007 |         45048 |
| particularly    |   0.06  |  1.071 |       2.226 |      0.36  |       0.193 |         0.007 |         44664 |
| already         |   8.349 |  0.724 |       0.662 |      0.621 |       2.294 |         0.007 |         43430 |
| just            |   0.901 |  1.041 |       0.465 |      0.67  |       1.339 |         0.007 |         42037 |
| always          |   0.544 |  0.481 |       1.173 |      1.948 |       6.763 |         0.006 |         39837 |
| super           |   0.114 |  1.05  |       0.295 |      1.928 |       0.192 |         0.006 |         38964 |
| completely      |   1.894 |  0.051 |       0.256 |      7.24  |       6.329 |         0.006 |         35903 |
| wide            | nan     |  0.002 |     nan     |      0.004 |      16.63  |         0.005 |         32283 |
| that            |   0.023 |  1.201 |       0.37  |      0.26  |       0.17  |         0.005 |         32269 |
| unusually       |   0.012 |  1.181 |       0.366 |      0.432 |       0.238 |         0.005 |         30963 |
| potentially     |   0.127 |  0.378 |      13.371 |      0.167 |       0.163 |         0.005 |         28659 |
| often           |   0.256 |  0.973 |       1.984 |      0.441 |       1.504 |         0.004 |         25612 |
| second          |   0.005 |  1.255 |       0.015 |      0.047 |       0.016 |         0.004 |         25482 |
| no              |   0.019 |  1.233 |       0.03  |      0.276 |       0.01  |         0.004 |         25322 |
| almost          |   4.925 |  0.131 |       0.235 |      6.402 |       5.029 |         0.004 |         24157 |
| only            |   1.692 |  0.584 |       0.995 |      1.971 |       5.049 |         0.004 |         23787 |
| surprisingly    |   0.084 |  1.156 |       0.106 |      0.669 |       0.472 |         0.004 |         23034 |
| especially      |   0.105 |  1.01  |       3.164 |      0.341 |       0.206 |         0.004 |         22595 |
| increasingly    |   0.082 |  1.015 |       2.158 |      0.26  |       1.093 |         0.004 |         22271 |
| all             |   6.78  |  0.424 |       2.433 |      2.984 |       2.599 |         0.003 |         22112 |
| somewhat        |   0.199 |  1.049 |       0.955 |      1.007 |       0.714 |         0.003 |         20796 |
| exceptionally   |   0.015 |  1.089 |       0.548 |      1.415 |       0.119 |         0.003 |         18759 |
| generally       |   0.077 |  0.931 |       0.202 |      2.628 |       1.026 |         0.003 |         18659 |
| nearly          |   5.508 |  0.063 |       0.033 |      5.414 |       7.029 |         0.003 |         18558 |
| usually         |   0.474 |  0.922 |       0.442 |      1.348 |       2.306 |         0.003 |         17435 |
| actually        |   5.756 |  0.777 |       0.935 |      1.396 |       1.532 |         0.002 |         13860 |
| ridiculously    |   0.02  |  1.226 |       0.208 |      0.142 |       0.112 |         0.002 |         12065 |
| perfectly       |   0.202 |  0.091 |       0.056 |     12.296 |       0.638 |         0.002 |         11998 |
| truly           |   5.871 |  0.491 |       2.018 |      2.785 |       2.692 |         0.002 |         11946 |
| totally         |   2.585 |  0.1   |       0.54  |      6.608 |       5.912 |         0.002 |          9598 |
| extraordinarily |   0.094 |  1.143 |       1.009 |      0.427 |       0.174 |         0.001 |          8828 |
| reasonably      |   0.019 |  0.85  |       0.077 |      4.021 |       0.557 |         0.001 |          8431 |
| never           |   2.482 |  0.672 |       0.317 |      3.871 |       1.852 |         0.001 |          8253 |
| typically       |   0.104 |  1.066 |       0.316 |      0.941 |       1.147 |         0.001 |          8022 |
| yet             |   4.791 |  0.456 |       0.368 |      4.987 |       2.367 |         0.001 |          8020 |
| dangerously     |   0.08  |  1.216 |       0.184 |      0.181 |       0.199 |         0.001 |          7942 |
| overly          |   0.021 |  1.065 |       0.777 |      1.075 |       0.656 |         0.001 |          7387 |
| definitely      |   3.235 |  0.855 |       0.715 |      1.179 |       2.004 |         0.001 |          6061 |
| awfully         |   0.046 |  1.204 |       0.44  |      0.19  |       0.141 |         0.001 |          6027 |
| kinda           |   0.685 |  1.112 |       0.936 |      0.406 |       0.415 |         0     |          3129 |
| sorta           |   2.077 |  0.917 |       1.611 |      1.217 |       0.872 |         0     |           172 |

Most divergent adjectives (of 50% most frequent) for each scale type:
 ¤ actually
 ¤ all
 ¤ almost
 ¤ especially
 ¤ exceptionally
 ¤ nearly
 ¤ no
 ¤ only
 ¤ perfectly
 ¤ potentially
 ¤ ridiculously
 ¤ second
 ¤ totally
 ¤ truly
 ¤ unusually
Heatmap saved to:
  /share/compling/projects/sanpi/notebooks/scale_comparison/images/scale-type_examples_35-17500.heat-ex.png
Heatmap saved to:
  /share/compling/projects/sanpi/notebooks/scale_comparison/images/scale-type_examples_35-17500.heat-key.png
Heatmap saved to:
  /share/compling/projects/sanpi/notebooks/scale_comparison/images/scale-type_35-17500.heat-key.png
Heatmap saved to:
  /share/compling/projects/sanpi/notebooks/scale_comparison/images/scale-type_35-17500.heat_ppi_m-mod.png
Heatmap saved to:
  /share/compling/projects/sanpi/notebooks/scale_comparison/images/scale-type_35-17500.heat-ALL.png

real	30m35.368s
user	26m46.358s
sys	1m55.338s
