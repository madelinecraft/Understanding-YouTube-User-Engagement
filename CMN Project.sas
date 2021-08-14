* import comments analyzed for sentiment;
proc import datafile = "C:\Users\mcraft\Desktop\CMN\DDBB_sent_emo (2).csv"
out = sent_emo dbms = csv replace; run;
* create a file with renamed videos for the two-part model;
data twopart;
	set sent_emo;
	Subject = .;
	if Video = "WrestleMania" then Subject = 1;
	else if Video = "Venezuela" then Subject = 2;
	else if Video = "Taylor4Apple" then Subject = 3;
	else if Video = "Statue" then Subject = 4;
	else if Video = "Sneakers" then Subject = 5;
	else if Video = "Samsung" then Subject = 6;
	else if Video = "Rogan" then Subject = 7;
	else if Video = "Rkelly" then Subject = 8;
	else if Video = "RedTable" then Subject = 9;
	else if Video = "Ramsay" then Subject = 10;
	else if Video = "Obama" then Subject = 11;
	else if Video = "Nike" then Subject = 12;
	else if Video = "Neverland" then Subject = 13;
	else if Video = "NatGeo" then Subject = 14;
	else if Video = "Makeup" then Subject = 15;
	else if Video = "Magnets" then Subject = 16;
	else if Video = "Lebron" then Subject = 17;
	else if Video = "KylieReunite" then Subject = 18;
	else if Video = "Kavanaugh" then Subject = 19;
	else if Video = "Jlo" then Subject = 20;
	else if Video = "Jaguar" then Subject = 21;
	else if Video = "Gucci" then Subject = 22;
	else if Video = "Football" then Subject = 23;
	else if Video = "FoodSwitch" then Subject = 24;
	else if Video = "Flo" then Subject = 25;
	else if Video = "DrOz" then Subject = 26;
	else if Video = "Diet" then Subject = 27;
	else if Video = "Debates" then Subject = 28;
	else if Video = "BlaseyonFox" then Subject = 29;
	else if Video = "ASMR" then Subject = 30;
run;
* likes are skewed, so take the log of the likes + 1;
data twopart;
	set twopart;
	loglikes = .;
	loglikes = log(likes + 1);
	logloglikes = log(loglikes + 1);
run;
* determine whether a multilevel model is necessary--unconditional multilevel model;
proc mixed data = new_sent_emo;
	class Subject;
	model likes = /s;
	random int / subject = Subject type = un;
run;
** explore effects of covariates;
* simple MLM-Sentiment;
proc mixed data=sent_emo;
	class Video;
	model likes = sent_score / s;
	random int / subject=Video type=un;
run;
* simple MLM-Sadness;
proc mixed data=sent_emo;
	class Video;
	model likes = sadness / s;
	random int / subject=Video type=un;
run;
* simple MLM-Joy;
proc mixed data=sent_emo;
	class Video;
	model likes = joy / s;
	random int / subject=Video type=un;
run;
* simple MLM-Fear;
proc mixed data=sent_emo;
	class Video;
	model likes = fear / s;
	random int / subject=Video type=un;
run;
* simple MLM-Disgust;
proc mixed data=sent_emo;
	class Video;
	model likes = disgust / s;
	random int / subject=Video type=un;
run;
* simple MLM-Anger;
proc mixed data=sent_emo;
	class Video;
	model likes = anger / s;
	random int / subject=Video type=un;
run;
* create subset and plot zero-inflated Poisson data;
data subvideos;
	set twopart;
	where Video = "Nike" or Video = "Statue" or Video = "Venezuela"
	or Video = "Samsung" or Video = "Gucci" or Video = "Diet";
run;
title 'Histograms of Zero-Inflated Likes';
proc sgpanel data = subvideos;
	panelby Video / onepanel layout = panel;
	vbar likes;
	colaxis label = "YouTube Comment Like Counts" Fitpolicy = thin;
run;
title 'Histograms of Logged Zero-Inflated Likes';
proc sgpanel data = subvideos;
	panelby Video / onepanel layout = panel;
	vbar logloglikes;
	colaxis label = "YouTube Comment Like Counts" Fitpolicy = thin;
run;
title 'Single Histogram Logged Likes for Nike';
proc sgplot data = twopart;
	where Video = "Nike";
	vbar loglikes / groupdisplay = cluster baselineintercept=.0000001;
	yaxis type = log logbase = 10;
run;
title 'Histograms of Zero-Inflated Replies';
proc sgpanel data = subvideos;
	panelby Video / onepanel layout = panel;
	vbar numberOfReplies;
	colaxis label = "YouTube Comment Reply Counts" Fitpolicy = thin;
run;
* create variable needed for fitting a two-part model;
data twopart;
	set twopart;
	P_u = 1;
	if likes = 0 then P_u = 0;
	else if likes = . then P_u = .;
	P_m = .;
	if P_u = 1 then P_m = likes;
run;
* export dataset for use in R;
proc export data = twopart dbms = csv outfile = "C:\Users\mcraft\Desktop\CMN\comments.csv" replace;
	putnames = yes;
run;

*****model fitting for number of likes*****;
title 'Starting Values for Two-part Parameters';
proc genmod data = twopart;
	class Subject;
	model likes = sent_score / dist = zip;
	zeromodel sent_score / link = logit;
run;
title 'Starting Values for Random-effects Parameters';
proc glimmix data = twopart noclprint method = laplace;
	class Subject;
	model likes = sent_score / s dist = poisson;
	random int / subject = Subject;
run;
title "Starting Values for the Random Effects Logistic Portion Only";
proc nlmixed data = twopart method = gaus qpoints = 5 maxfunc = 3000
maxiter = 10000 noad gconv = 0 absconv = 0;
	parms a0 = 1.9445 a1 = 0.6282 vara = 1.6906;
	u = P_u;
	m = P_m;

	*Binary part;
	ueta = a0 + a1*sent_score + au;
	expeta = exp(ueta);
	p = expeta/(1+expeta);
	LL1 = log((1-p)**(1-u)) + log(p**(u));
	
	model likes ~ general(LL1);
	random au ~ normal (0, vara) subject = Subject;
	bounds vara >= 0;
run;
title "Starting Values for the Fixed Effects Logistic Portion Only";
proc nlmixed data = twopart method = gaus qpoints = 5 maxfunc = 3000
maxiter = 10000 noad gconv = 0 absconv = 0;
	parms a0 = 1.9445 a1 = 0.6282;
	u = P_u;
	m = P_m;

	*Binary part;
	ueta = a0 + a1*sent_score;
	expeta = exp(ueta);
	p = expeta/(1+expeta);
	LL1 = log((1-p)**(1-u)) + log(p**(u));
	
	model likes ~ general(LL1);
run;
title "Starting Values for the Poisson Portion Only";
proc nlmixed data = twopart method = gaus qpoints = 5 maxfunc = 3000
maxiter = 10000 noad gconv = 0 absconv = 0;
	parms b10 = 1.9445 b11 = 0.6282 varb = 1.6906;
	u = P_u;
	m = P_m;

	*Poisson part;
 	mu = exp(b10 + b11*sent_score + bu);
	LL2 = likes*log(mu) - mu - lgamma(likes + 1);

	model likes ~ general(LL2);
	random bu ~ normal (0, varb) subject = Subject;
	bounds varb >= 0;
run;
title "Two-part RANDOM Logistic and Poisson Model";
proc nlmixed data = twopart noad method = gaus qpoints = 50 maxfunc = 3000 
maxiter = 10000 gconv = 0 absconv = 0;
parms b10 = 3.7300 b11 = 0.6063
a0 = -1.1279 a1 = -0.05894
varb = 0.6573 vara = 0.4526 covab = 0.2944;
pi = arcos(-1);
u = P_u;
m = P_m;

ueta = a0 + a1*sent_score + au; *logistic model with time varying predictor;
expeta = exp(ueta);
p = expeta/(1+expeta);
LL1 = log((1-p)**(1-u)) + log(p**(u)); *loglikelihood for a binary dist;

if likes > 0 then do;
mu = exp(b10 + b11*sent_score + bu); *Poisson model with time varying predictor;
LL2 = likes*log(mu) - mu - lgamma(likes + 1); *loglikelihood for a Poisson dist;
end;

if likes = 0 then Loglik = LL1;
else if likes > 0 then Loglik = LL1+LL2;

model likes ~ general(Loglik);
random au bu ~ normal ([0,0],[vara, covab, varb]) subject = Subject;
bounds vara >= 0, varb >= 0;
run;
title "Two-part FIXED Logistic and Poisson Model";
proc nlmixed data = twopart noad method = gaus qpoints = 50 maxfunc = 3000 
maxiter = 10000 gconv = 0 absconv = 0;
parms b10 = 3.7300 b11 = 0.6063
a0 = -1.1279 a1 = -0.05894;
pi = arcos(-1);
u = P_u;
m = P_m;

ueta = a0 + a1*sent_score; *logistic model with time varying predictor;
expeta = exp(ueta);
p = expeta/(1+expeta);
LL1 = log((1-p)**(1-u)) + log(p**(u)); *loglikelihood for a binary dist;

if likes > 0 then do;
mu = exp(b10 + b11*sent_score); *Poisson model with time varying predictor;
LL2 = likes*log(mu) - mu - lgamma(likes + 1); *loglikelihood for a Poisson dist;
end;

if likes = 0 then Loglik = LL1;
else if likes > 0 then Loglik = LL1+LL2;

model likes ~ general(Loglik);
run;
title "Two-part RANDOM Logistic and Truncated Poisson Model";
proc nlmixed data = twopart noad method = gaus qpoints = 50 maxfunc = 3000 
maxiter = 10000 gconv = 0 absconv = 0;
parms b10 = 21.4195 b11 = 0.6178 b12 = -0.1109
a0 = 0.5792 a1 = -0.04402 a2 = -0.01279
vara = 0.2053 covab = -0.1852 varb = 1.1959;
pi = arcos(-1);
u = P_u;
m = P_m;

ueta = a0 + a1*sent_score + a2*short_timestamp + au; *logistic model with time varying predictor;
expeta = exp(ueta);
p = expeta/(1+expeta);
LL1 = log((1-p)**(1-u)) + log(p**(u)); *loglikelihood for a binary dist;

if likes > 0 then do;
log_lambda = b10 + b11*sent_score + b12*short_timestamp + bu; *Poisson model with time varying predictor;
lambda = exp(log_lambda); 
*LL2 = likes*log_lambda - lambda - log(1-exp(-lambda)) - lgamma(likes+1);*loglikelihood for a truncated Poisson dist;	
*or;
LL2 = log(pi) - log(1-exp(-lambda)) - lambda - lgamma(likes+1) + likes*log(lambda);
end;

if likes = 0 then Loglik = LL1;
else if likes > 0 then Loglik = LL1+LL2;

model likes ~ general(Loglik);
random au bu ~ normal ([0,0],[vara, covab, varb]) subject = Subject;
bounds vara >= 0, varb >= 0;
run;
title "Two-part FIXED Logistic and Truncated Poisson Model";
proc nlmixed data = twopart noad method = gaus qpoints = 50 maxfunc = 3000 
maxiter = 10000 gconv = 0 absconv = 0;
parms b10 = 3.6721 b11 = 0.6060 b12 = 0
a0 = -1.3528 a1 = -0.04973 a2 = 0;
pi = arcos(-1);
u = P_u;
m = P_m;

ueta = a0 + a1*sent_score + a2*short_timestamp; *logistic model with time varying predictor;
expeta = exp(ueta);
p = expeta/(1+expeta);
LL1 = log((1-p)**(1-u)) + log(p**(u)); *loglikelihood for a binary dist;

if likes > 0 then do;
log_lambda = b10 + b11*sent_score + b12*short_timestamp; *Poisson model with time varying predictor;
lambda = exp(log_lambda); 
*LL2 = likes*log_lambda - lambda - log(1-exp(-lambda)) - lgamma(likes+1);*loglikelihood for a truncated Poisson dist;	
*or;
LL2 = log(pi) - log(1-exp(-lambda)) - lambda - lgamma(likes+1) + likes*log(lambda);
end;

if likes = 0 then Loglik = LL1;
else if likes > 0 then Loglik = LL1+LL2;

model likes ~ general(Loglik);
run;
title1 "Two-part Random Poisson Model with LSM";
proc nlmixed data = twopart method = gaus qpoints = 5 maxfunc = 3000 
maxiter = 10000 noad gconv = 0 absconv = 0;
parms b10 = 3.6455 b11 = 0.6063
a0 = -1.2902 a1 = -0.05574
lnvarb = -0.05858 /*lnvara = -1.5474*/ tau1 = 1;

pi = arcos(-1);
u = P_u;
m = P_m;

ueta = a0 + a1*sent_score + au; *logistic model with time varying predictor;
expeta = exp(ueta);
p = expeta/(1+expeta);
LL1 = log((1-p)**(1-u)) + log(p**(u)); *loglikelihood for a binary dist;

if likes > 0 then do;
log_lambda = b10 + b11*sent_score + bu; *Poisson model with time varying predictor;
lambda = exp(log_lambda); 
*LL2 = likes*log_lambda - lambda - log(1-exp(-lambda)) - lgamma(likes+1);*loglikelihood for a truncated Poisson dist;	
*or;
LL2 = log(pi) - log(1-exp(-lambda)) - lambda - lgamma(likes+1) + likes*log(lambda);
varb = EXP(lnvarb + tau1*avg_sent); *LSM;
end;

if likes = 0 then Loglik = LL1;
else if likes > 0 then Loglik = LL1+LL2;

model likes ~ general(Loglik);
random au bu ~ normal ([0,0],[vara, covab, varb]) subject = Subject;
*bounds vara >= 0, varb >= 0;
run;
*LSM does not converge;

*****model fitting for number of responses*****;
title 'Starting Values for Two-part Parameters';
proc genmod data = twopart;
	class Subject;
	model numberOfReplies = sent_score / dist = zip;
	zeromodel sent_score / link = logit;
run;
title 'Starting Values for Random-effects Parameters';
proc glimmix data = twopart noclprint method = laplace;
	class Subject;
	model numberOfReplies = sent_score / s dist = poisson;
	random int / subject = Subject;
run;

title1 "Two-part Random Poisson Model";
proc nlmixed data = twopart method = gaus qpoints = 25 maxfunc = 3000 maxiter = 10000;
parms b10 = 1.6596 b11 = 0.0689
a0 = 1.9769 a1 = 0.1912
varb = 0.8201;

logit0 = a0 + a1*sent_score; *logistic model with time varying predictor;
prob0 = 1 / (1 + exp(-logit0));
mu = exp(b10 + b11*sent_score + bu); *Poisson model with time varying predictor;

if numberOfReplies = 0 then
	LL = log(prob0 + (1-prob0)*exp(-mu)); *loglikelihood for a binary dist;
else
	LL = numberOfReplies*log(mu) - mu - lgamma(numberOfReplies + 1); *loglikelihood for a poisson dist;
model numberOfReplies ~ general(LL);
random bu ~ normal (0,varb) subject = Subject;
run;
*Note: I tried putting a random effect in the logistic portion but couldn't 
get it to converge;

title1 "Two-part Random Poisson Model with LSM";
proc nlmixed data = twopart method = gaus qpoints = 25 maxfunc = 3000 maxiter = 10000;
parms b10 = 1.5829 b11 = 0.08175
a0 = 20.2278 a1 = 1.1711
lnvarb = -1.033387 tau1 = 0;

logit0 = a0 + a1*sent_score; *logistic model with time varying predictor;
prob0 = 1 / (1 + exp(-logit0));
mu = exp(b10 + b11*sent_score + bu); *Poisson model with time varying predictor;
varb = EXP(lnvarb + tau1*avg_replies);

if numberOfReplies = 0 then
	LL = log(prob0 + (1-prob0)*exp(-mu)); *loglikelihood for a binary dist;
else
	LL = numberOfReplies*log(mu) - mu - lgamma(numberOfReplies + 1); *loglikelihood for a poisson dist;

model numberOfReplies ~ general(LL);
random bu ~ normal (0,varb) subject = Subject;
run;
*plots;
proc freq data = twopart;
	table likes;
run;
*histogram;
title 'Youtube Comment Likes';
proc univariate data = twopart;
	where likes between 0 and 500;
	var likes;
	histogram / odstitle = "Distribution of YouTube Comment Likes" ;
quit;
*spaghetti plot;
*export fixed and random effects to data sets;
ods output solutionf=sf(keep=effect estimate  
                                 rename=(estimate=FE));
ods output solutionr=sr(keep=effect M2ID estimate
                                 rename=(estimate=RE));
proc mixed data=twopart;
	class Subject;
    model likes = / s outp = pred;
    random int / s g gcorr type=un subject=Subject;
run; quit;
ods output close;
*create random subsets of data for plotting;
data subpred;
	set pred;
	where Video = "Nike" or Video = "Venezuela" or Video = "Neverland" or 
	Video = "NatGeo" or Video = "Football" or Video = "Diet";
run;
ods graphics off;
proc reg data = twopart;
	model likes = ;
	ods output ParameterEstimates=PE;
run;
data _null_;
	set PE;
	if _n_ = 1 then call symput('Int', put(estimate, BEST6.));
	else			call symput('Slope', put(estimate, BEST6.));
run;
proc sgpanel data=subpred;
	panelby Video / columns=3 spacing=5 /*novarname*/;
	styleattrs datacolors=(GRAY4F);
	series x = numid y = likes;
	scatter x = numid y = likes;
	rowaxis label = "# of YouTube Comment Likes";
	colaxis label = " " display = all;
	series x = numid y = pred / lineattrs = (color = black) 
	legendlabel = "Fitted Values";
	*reg x=b2dday y=b2dnegav/ cli clm;
	title "Fitted Intercepts for a Random Subsample of Six Individuals";
run;
