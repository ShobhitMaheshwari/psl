../../bin/learnwts -d -i smoking.mln -o smoking-out.mln -t lived_obs.txt -ne Knows
../../bin/infer -ms -i smoking.mln -r smoking.result -e lived_obs.txt -q Knows
