import pandas as pd
# from scipy.stats import chi2
from reliability.Fitters import Fit_Weibull_3P,Fit_Gamma_3P,Fit_Exponential_1P
# import os
from reliability.Distributions import Weibull_Distribution,Gamma_Distribution,Exponential_Distribution
from reliability.Reliability_testing import chi2test
import warnings
warnings.filterwarnings('ignore')
#readind data
d1=pd.read_excel('2/clean_data.xlsx',sheet_name='D1',header=None)
d2=pd.read_excel('2/clean_data.xlsx',sheet_name='D2',header=None)
d3=pd.read_excel('2/clean_data.xlsx',sheet_name='D3',header=None)
#convert pandas DF to lists
data1=list(d1[0])
data2=list(d2[0])
data3=list(d3[0])

#fit and test weibull dist for D1
wb1 = Fit_Weibull_3P(failures=data1)
# print('alpha:',wb1.alpha,'\nbeta:',wb1.beta,'\ngamma:',wb1.gamma)
dist_w_1 = Weibull_Distribution(alpha=wb1.alpha,beta=wb1.beta,gamma=wb1.gamma)
# dist_w_1.inverse_SF(0.25)
# dist_w_1.CDF(247.23352197423867)
bins_w1=[0.001]
for i in range(10):
    bins_w1.append(dist_w_1.inverse_SF(1 - (i + 1) * 0.1))
chi2_test_w1=chi2test(dist_w_1,data=data1,significance=0.05,bins=bins_w1)


'''e1 = Fit_Exponential_1P(failures=data1)
# print('alpha:',wb1.alpha,'\nbeta:',wb1.beta,'\ngamma:',wb1.gamma)
dist_e_1 = Exponential_Distribution(0.00562002)
# dist_w_1.inverse_SF(0.25)
# dist_w_1.CDF(247.23352197423867)
bins_e1=[0.001]
for i in range(15):
    bins_e1.append(dist_e_1.inverse_SF(1 - (i + 1) * 0.0625))
chi2_test_e1=chi2test(dist_w_1,data=data1,significance=0.1,bins=bins_w1)
'''
'''
#binning by weibul dist
hist1w={}
d1c=d1.copy()
for i in range(15):
    tresh = dist_w_1.inverse_SF(1 - (i + 1) * 0.0625)
    hist1w[i]=len(d1c[d1c[0]<tresh])
    d1c=d1c[d1c[0]>=tresh]
hist1w[15]=len(d1c)
hist1w_df = pd.DataFrame(hist1w.items(), columns=['bin', 'Oi'])
hist1w_df['Ei']=len(d1)/16
hist1w_df['sqr_err']=(hist1w_df['Oi']-hist1w_df['Ei'])**2
hist1w_df['sqr_err/Ei']=hist1w_df['sqr_err']/hist1w_df['Ei']
sum_of_errs_w1=hist1w_df['sqr_err/Ei'].sum()
1-chi2.cdf(sum_of_errs_w1,16-1-3)
'''

#fit and test Gamma dist for D1
gm1 = Fit_Gamma_3P(failures=data1)
# print('alpha:',gm1.alpha,'\nbeta:',gm1.beta,'\ngamma:',gm1.gamma)
dist_g_1 = Gamma_Distribution(alpha=gm1.alpha,beta=gm1.beta,gamma=gm1.gamma)
# dist_g_1.inverse_SF(0.25)
# dist_g_1.CDF(0.890839752681416)
bins_g1=[0.001]
for i in range(10):
    bins_g1.append(dist_g_1.inverse_SF(1 - (i + 1) * 0.1))
chi2_test_g1=chi2test(dist_g_1,data=data1,significance=0.05,bins=bins_g1)


#fit and test weibull dist for D2
wb2 = Fit_Weibull_3P(failures=data2)
dist_w_2 = Weibull_Distribution(alpha=wb2.alpha,beta=wb2.beta,gamma=wb2.gamma)
bins_w2=[0.001]
for i in range(10):
    bins_w2.append(dist_w_2.inverse_SF(1 - (i + 1) * 0.1))
chi2_test_w2=chi2test(dist_w_2,data=data2,significance=0.05,bins=bins_w2)

#fit and test Gamma dist for D2
gm2 = Fit_Gamma_3P(failures=data2)
dist_g_2 = Gamma_Distribution(alpha=gm2.alpha,beta=gm2.beta,gamma=gm2.gamma)
bins_g2=[0.001]
for i in range(10):
    bins_g2.append(dist_g_2.inverse_SF(1 - (i + 1) * 0.10))
chi2_test_g2=chi2test(dist_g_2,data=data2,significance=0.05,bins=bins_g2)

#fit and test weibull dist for D3
wb3 = Fit_Weibull_3P(failures=data3)
dist_w_3 = Weibull_Distribution(alpha=wb3.alpha,beta=wb3.beta,gamma=wb3.gamma)
bins_w3=[0.001]
for i in range(10):
    bins_w3.append(dist_w_3.inverse_SF(1 - (i + 1) * 0.1))
chi2_test_w3=chi2test(dist_w_3,data=data3,significance=0.05,bins=bins_w3)


#fit and test Gamma dist for D3
gm3 = Fit_Gamma_3P(failures=data3)
dist_g_3 = Gamma_Distribution(alpha=gm3.alpha,beta=gm3.beta,gamma=gm3.gamma)
bins_g3=[0.001]
for i in range(10):
    bins_g3.append(dist_g_3.inverse_SF(1 - (i + 1) * 0.10))
chi2_test_g3=chi2test(dist_g_3,data=data3,significance=0.05,bins=bins_g3)

print('\t\t\t\thypothesis\tchisquared_statistic\tchisquared_critical_value')
print('weibull for d1:',chi2_test_w1.hypothesis ,f"\t\t{chi2_test_w1.chisquared_statistic}",f'\t\t{chi2_test_w1.chisquared_critical_value}')
print('gamma for d1:  ',chi2_test_g1.hypothesis ,f'\t\t{chi2_test_g1.chisquared_statistic}',f'\t\t{chi2_test_g1.chisquared_critical_value}')
print('weibull for d2:',chi2_test_w2.hypothesis ,f'\t\t{chi2_test_w2.chisquared_statistic}',f'\t\t{chi2_test_w2.chisquared_critical_value}')
print('gamma for d2:  ',chi2_test_g2.hypothesis ,f'\t\t{chi2_test_g2.chisquared_statistic}',f'\t\t{chi2_test_g2.chisquared_critical_value}')
print('weibull for d3:',chi2_test_w3.hypothesis ,f'\t\t{chi2_test_w3.chisquared_statistic}',f'\t\t{chi2_test_w3.chisquared_critical_value}')
print('gamma for d3:  ',chi2_test_g3.hypothesis ,f'\t\t{chi2_test_g3.chisquared_statistic}',f'\t\t{chi2_test_g3.chisquared_critical_value}')

print('\t\t\t\talpha\t\t\t\tbeta\t\t\t\tgamma\t\t\t\tmean\t\t\t\tstdev')
print('gamma for d1:  ',dist_g_1.alpha ,f'\t{dist_g_1.beta}',f'\t{dist_g_1.gamma}',f'\t{dist_g_1.mean}',f'\t{dist_g_1.standard_deviation}')
print('gamma for d2:  ',dist_g_2.alpha ,f'\t{dist_g_2.beta}',f'\t{dist_g_2.gamma}',f'\t{dist_g_2.mean}',f'\t{dist_g_2.standard_deviation}')
print('gamma for d3:  ',dist_g_3.alpha ,f'\t{dist_g_3.beta}',f'\t{dist_g_3.gamma}',f'\t{dist_g_3.mean}',f'\t{dist_g_3.standard_deviation}')

