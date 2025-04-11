f:{[t;c]
    dmap:(distinct desc t[c])!100*(0,((count distinct t[c])-1)#sums value (count each group desc t[c]))%count t;
    newcol:`$(string c),"pct";
    ![t;();0b;(enlist newcol)!enlist(`dmap;c)]}

fp:{[t;c]
    dmap:(distinct desc t[c])!100*(0,((count distinct t[c])-1)#sums value (count each group desc t[c]))%count t;
    flip (c;`pctl)!(key dmap;value dmap)}

// ################# mode = 15 second #################

pct15:("ISFFFFZ";enlist ",") 0: read0 `$"/home/conner/SpeedTyping/MonkeyTypeLeaderboard/leaderboard_15sec.csv"
pct15:update diff:raw-wpm from pct15

pct15:f[pct15;`wpm]
pct15:f[pct15;`raw]
pct15:f[pct15;`acc]
pct15:f[pct15;`consistency]
pct15:f[pct15;`diff]
pct15:f[pct15;`datetime]
pct15:update delta:wpmpct-accpct from pct15
pct15:f[pct15;`delta]
save `:pct15.csv

wpm15:fp[pct15;`wpm]
raw15:fp[pct15;`raw]
acc15:fp[pct15;`acc]
cons15:fp[pct15;`consistency]
diff15:fp[pct15;`diff]
datetime15:fp[pct15;`datetime]
delta15:fp[pct15;`delta]

save `wpm15.csv
save `raw15.csv
save `acc15.csv
save `cons15.csv
save `diff15.csv
save `datetime15.csv
save `delta15.csv

// ################# mode = 60 second #################

pct60:("ISFFFFZ";enlist ",") 0: read0 `$"/home/conner/SpeedTyping/MonkeyTypeLeaderboard/leaderboard_60sec.csv"
pct60:update diff:raw-wpm from pct60


pct60:f[pct60;`wpm]
pct60:f[pct60;`raw]
pct60:f[pct60;`acc]
pct60:f[pct60;`consistency]
pct60:f[pct60;`diff]
pct60:f[pct60;`datetime]
pct60:update delta:wpmpct-accpct from pct60
pct60:f[pct60;`delta]
save `:pct60.csv

wpm60:fp[pct60;`wpm]
raw60:fp[pct60;`raw]
acc60:fp[pct60;`acc]
cons60:fp[pct60;`consistency]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
diff60:fp[pct60;`diff]
datetime60:fp[pct60;`datetime]
delta60:fp[pct60;`delta]

save `wpm60.csv
save `raw60.csv
save `acc60.csv
save `cons60.csv
save `diff60.csv
save `datetime60.csv
save `delta60.csv

wpmtab:update mult:wpm15%wpm60,gap:wpm15-wpm60 from (select wpm60:max wpm by .5 xbar pctl from wpm60)lj(select wpm15:max wpm by .5 xbar pctl from wpm15)
rawtab:update mult:raw15%raw60,gap:raw15-raw60 from (select raw60:max raw by .5 xbar pctl from raw60)lj(select raw15:max raw by .5 xbar pctl from raw15)
acctab:update mult: acc15%acc60,gap:acc15-acc60 from (select acc60:max acc by .5 xbar pctl from acc60)lj(select acc15:max acc by .5 xbar pctl from acc15)
constab:update mult:cons15%cons60,gap:cons15-cons60 from (select cons60:max consistency by .5 xbar pctl from cons60)lj(select cons15:max consistency by .5 xbar pctl from cons15)
difftab:update mult:diff15%diff60,gap:diff15-diff60 from (select diff60:max diff by .5 xbar pctl from diff60)lj(select diff15:max diff by .5 xbar pctl from diff15)
datetab:update mult:datetime15%datetime60,gap:datetime15-datetime60 from (select datetime60:max datetime by .5 xbar pctl from datetime60)lj(select datetime15:max datetime by .5 xbar pctl from datetime15)
deltatab:update mult:delta15%delta60,gap:delta15-delta60 from (select delta60:max delta by .5 xbar pctl from delta60)lj(select delta15:max delta by .5 xbar pctl from delta15)

save `wpmtab.csv
save `rawtab.csv
save `acctab.csv
save `constab.csv
save `difftab.csv
save `datetab.csv
save `deltatab.csv  
