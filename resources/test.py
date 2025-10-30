
"""
test.py
middleware for hypothesis testing 
"""

class InvalidKeyError(Exception):
    """Raised when invalid type is passed as a key """
    pass 

class InvalidKeyValueError(Exception):
    """Raised when invalid type is passed as a key """
    pass 

class InvalidSampleSize(Exception):
    """Raised when invalid type is passed as a key """
    pass 

class InvalidHypothesisType(Exception):
    """Raised when invalid type is passed as a key """
    pass 

class InvalidHypothesisConfiguration(Exception):
    """Raised when invalid type is passed as a key """
    pass 

class InvalidArgumentPassed(Exception):
    """Raised when invalid type is passed as a key """
    pass 


class Test:
    def __init__(self) -> None:
        self.type = '' # type of test: difference of mean(diff), mean(mean), or proportional(prop) 
        self.tail = '' # type of test 
        self.mu = 0
        self.sigma1 = 0 # population standard deviation 
        self.sigma2 = 0
        self.N = 0
        self.n1 = 0 # sample 1
        self.n2 = 0 # sample 2 (for diff of means)
        self.xbar1 = 0 # sample mean 1
        self.xbar2 = 0 # sample of mean 2 for diff of mean
        self.p = 0 # proportion of population 
        self.p_hat = 0 # sample proportion 
        self.s1 = 0 # sample standard deviation 
        self.s2 = 0 # sample standard deviation for diff mean
        self.observed_value = 0 # The observed value in an trial, usually an observed mean or proportion from a sample 
        self.hypothesize_diff = 0 # hypothesized value
        self.cl = 0 # confidence level
        self.alpha = 0 # 
        self.lower_alpha = 0 
        self.upper_alpha = 0
        self.equal_variances = None  # diff of mean value check if variances are equal  
        self.var1 = 0  # sample variance 
        self.var2 = 0 # sample variance for diff of mean 
        self.diff_of_means = 0 # diff or means for diff of mean hypo testing
        self.pooled_variance = 1 # pooled variance (S_p) - I set this to 1 so that even if its called without calc no harm
        self.std_err = 0
        self.df = 0 # degrees of freedom
        self.q = 0 # area , used to calculate a, and t values
        self.ci = 0 # confidence interval 
        self.a = 0 # confidence interval lower value 
        self.b = 0 # confidence interval upper value 
        self.critical_value = 0 # critical value of z or t test 
        self.critical_value_two = False
        self.critical_value_upper = False
        self.critical_value_lower = False
        self.test_statistic = 0 # diff of mean - hypothesized diff of mean / standard error 
        self.p_value = 0
        self.p1 = 0
        self.p2 = 0
        self.t_test = 0
        self.significance = None # if p-value < 0.5 then true else false
        self.frac1 = 0
        self.frac2 = 0
        self.me = 0 # margin of error used to calculate minimum sample size required for confidence interval SDSM 
        self.min_n = 0 # minimal sample size for sample mean test 
        self.mar_err_min_n = 0 # the suggested margin of error when calculating minimum sample size
        self.replacement = False
        self.fpc = 0 
        self.z = True
        self.size = '' # large or small sample size - calculated
        self.sample_ratio = 0 # calculated n/N 
        self.successes = 0
        self.failures = 0
        self.data = {}
        self.null_hypo = ''
        self.alt_hypo = ''
        self.auc = 0 # used to calculate critical value, derived from 1 - alpha 
        self.statement = False # print the hypothesis statement
        self.visual = False # plot the hypothesis
        self.prop_sample_isnormal = False # is the proportion sample normalized 
    
        import sys
        sys.path.insert(0, '..')
        import resources.datum as datum 
        self.datum = datum.Data()
        


    def make_hypothesis_test(self, info : dict = {}):
        
        
        self.validate_sample_data(info = info)
        self.calculate_hypothesis_test_statisics()
        #pretty print hypothesis test
        if self.statement:
            import sys
            sys.path.insert(0, '..')
            import resources.message as message
            state = message.Statement(self.data)
            state.create_statement()
        # display hypothesis plot 
        if self.visual:
            import sys
            sys.path.insert(0, '..')
            import resources.plot as plot 
            hypothesis_plot = plot.Plot(self.data)
            hypothesis_plot.create_plot()
        if not self.statement and not self.visual:
            if self.type == 'mean':
                msg = f'N: {self.N}\nn: {self.n1}\nxbar: {self.xbar1}\nmu: {self.mu}\nSigma: {self.sigma1}\nCL: {self.cl}\n'
                msg = msg + f's: {self.s1}\ncritical_value:{self.critical_value}\np-value: {self.p_value}\n'
                print(msg)
            if self.type == "diff_of_mean":
                msg = f'Hypothesis Test: {self.type}\n'
                msg = f'sigma1: {self.sigma1}\nsigma2: {self.sigma2}\nxbar1: {self.xbar1}\nxbar2: {self.xbar2}\ns1: {self.s1}\ns2: {self.s2}\n'
                msg = msg + f'var1: {self.var1}\nvar2: {self.var2}\nn1: {self.n1}\nn2: {self.n2}\nstandard error: {self.std_err}\n'
                msg = msg + f'pooled varience: {self.pooled_variance}\ncritical_value: {self.critical_value}\nmargin of error: {self.me}\n'
                msg = msg + f'(a, b) = ({self.a}, {self.b})'
                print(msg)
            if self.type == 'prop':
                msg = f'N: {self.N}\nn: {self.n1}\nsample ratio: {self.sample_ratio}\nsuccesses: {self.successes}\n'
                msg = msg + f'failures: {self.failures}\np_hat: {self.p_hat}\nconfidence level: {self.cl}\nstandard error: {self.std_err}\n'
                msg = msg + f'critical value: {self.critical_value}\nfpc: {self.fpc}\nmargin of error: {self.me}\n'
                msg = msg + f'(a, b) = ({self.a}, {self.b})'
                print(msg)


    def validate_sample_data(self, info : dict = {}):
        validate = {}
        keyList = ['test','type', 'tail', 'replacement', 'mu', 'N', 'sigma1', 'sigma2', 'var1', 'var2', 'n1', 'n2', 'xbar1', 'xbar2', 'statement', 'visual', 
                    'p', 'p_hat', 'p1', 'p2', 'successes', 'hypothesize_diff', 's1', 's2', 'cl', 'mar_err_min_n', 'null_hypo', 'alt_hypo', 'observed_value']
        for key in keyList:
            validate[key] = None 
        if isinstance(info, dict) and len(info.keys()) > 0:
            for key, val in info.items():
                if key not in ['x_data', 'y_data']:
                    if key in validate: 
                        if key == "type":
                            if not isinstance(val, str):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg) 
                            else:
                                if info['type'].lower() in ["diff_of_mean", 'mean', 'prop']:
                                    self.type = info['type'].lower()
                                else:
                                    err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                    raise InvalidKeyValueError(err_msg) 
                        if key == "statement":
                            if not isinstance(val, bool):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg) 
                            else:
                                self.statement = info['statement']
                        if key == "visual":
                            if not isinstance(val, bool):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg) 
                            else:
                                self.visual = info['visual']
                        if key == "tail":
                            if not isinstance(val, str):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg) 
                            else:
                                self.tail = info['tail']
                                
                        if key == "replacement":
                            if not isinstance(val, bool):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg) 
                            else:
                                self.replacement = info['replacement']

                        if key == "mar_err_min_n":
                            if not isinstance(val, int):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg) 
                            else:
                                self.mar_err_min_n = info['mar_err_min_n']     

                        if key == "N":
                            if not isinstance(val, int | float):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg) 
                            else:
                                self.N = info['N']

                        if key == "mu":
                            if not isinstance(val, int | float):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg) 
                            else:
                                self.mu = info['mu']                       
                                
                        if key == "sigma1":
                            if not isinstance(val, int | float):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg) 
                            else:
                                self.sigma1 = info['sigma1']

                        if key == "sigma2":
                            if not isinstance(val, int | float):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg)  
                            else:
                                self.sigma2 = info['sigma2']
                        if key == "n1":
                            if not isinstance(val, int):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg) 
                            else: 
                                self.n1 = info['n1']
                        if key == "n2":
                            if not isinstance(val, int):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg) 
                            else: 
                                self.n2 = info['n2']
                        if key == "xbar1":
                            if not isinstance(val, int | float):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg) 
                            else: 
                                self.xbar1 = info['xbar1']
                        if key == "xbar2":
                            if not isinstance(val, int | float):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg) 
                            else: 
                                self.xbar2 = info['xbar2']  
                        if key == "observed_value":
                            if not isinstance(val, int | float):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg) 
                            else: 
                                self.observed_value = info['observed_value']  
                        if key == "p":
                            if not isinstance(val, int | float):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg) 
                            else: 
                                self.p = info['p']             
                        if key == "p_hat":
                            if not isinstance(val, int | float):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg) 
                            else: 
                                self.p_hat = info['p_hat']  
                        if key == "p2":
                            if not isinstance(val, int | float):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg) 
                            else: 
                                self.p2 = info['p2'] 
                        if key == "p1":
                            if not isinstance(val, int | float):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg) 
                            else: 
                                self.p1 = info['p1'] 
                                
                        if key == "successes":
                            if not isinstance(val, int | float):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg) 
                            else: 
                                self.successes = info['successes']  
                        if key == "s1":
                            if not isinstance(val, int | float):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg)  
                            else: 
                                self.s1 = info['s1']  
                        if key == "s2":
                            if not isinstance(val, int | float):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg)   
                            else: 
                                self.s2 = info['s2']
                        if key == "var1":
                            if not isinstance(val, int | float):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg)   
                            else: 
                                self.var1 = info['var1']
                        if key == "var2":
                            if not isinstance(val, int | float):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg)   
                            else: 
                                self.var2 = info['var2']
                        if key == "cl":
                            if not isinstance(val, int | float):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg)                      
                            else: 
                                self.cl = info['cl']
                                # calculate alpha 
                                self.alpha = ((self.cl - 1) / 2) if (self.tail == "two") else (1 - self.cl)
                                self.auc = 1 - self.alpha 
                                
                        if key == "hypothesize_diff":
                            if not isinstance(val, int | float):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg)  
                            else: 
                                self.hypothesize_diff = info['hypothesize_diff']
                        if key == "null_hypo":
                            if not isinstance(val, str):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg) 
                            self.null_hypo = info['null_hypo']
                        if key == "alt_hypo":
                            if not isinstance(val, str):
                                err_msg = f'Key: "{key}", contains an invalid value: {val}.'             
                                raise InvalidKeyValueError(err_msg) 
                            else: 
                                self.alt_hypo = info['alt_hypo']       
                        # no validation on plot lists x, y 
                        self.data['x_data'] = info['x_data']
                        self.data['y_data'] = info['y_data']                    
                    else:
                        from colorama import Fore, Style
                        print(Fore.RED, Style.BRIGHT + f'KEY {key} IN DICTIIONARY NOT DEFINED')
                        Style.RESET_ALL    
                        raise InvalidKeyError      
        else:
            err_msg = 'INFO DICTIIONARY NOT DEFINED'
            raise InvalidKeyError(err_msg)  
        
        # validate  confidence level
        if self.cl < 0.01 or self.cl > .99:
            from colorama import Fore, Style
            err_msg =  f'Invalid Confidence Level Value2: {self.cl}'
            raise InvalidKeyValueError(err_msg)
        
        # if type is not proportion sigma1 or xbar
        if self.type != 'prop' and self.sigma1 == 0 and self.xbar1 == 0:
            from colorama import Fore, Style
            print(Fore.RED, Style.BRIGHT + 'both population standard deviation and sample standard deviation cannot be 0')
            print(Style.RESET_ALL)
            raise InvalidHypothesisType
        
        if self.type == "diff_of_mean":
            # check to see if both sigma values are present of both s values are present
            if self.sigma1 == 0 and self.sigma2 == 0:
                if self.xbar1 == 0 and self.xbar2 == 0:
                    from colorama import Fore, Style
                    print(Fore.RED, Style.BRIGHT + 'both population standard deviation 1 and 2OR both sample standard devations 1 and 2 must be provided')
                    print(Style.RESET_ALL)
                    raise InvalidHypothesisType   
                
            # validate xbar1 and xbar2 require valid values 
            if self.n1 == 0 and self.n2 == 0:
                from colorama import Fore, Style
                err_msg = (Fore.RED, Style.BRIGHT) + 'sample size 1 and sample size 2 are required for difference of mean test'
                raise InvalidHypothesisType(err_msg)

            #determine sample size  
            if (self.n1 > 30) and (self.n2 > 30):
                self.size = 'large'
            elif(self.n1 > 4) and (self.n2 > 4):
                self.size = 'small'
                self.df = self.n1 - 1
            else:
                err_msg = f'sample size n1 ({self.n1}) or n2 ({self.n2}) are too small for difference of mean hypothesis testing'
                raise InvalidSampleSize(err_msg)   
        # mean hypothesis  
        if self.type == 'mean':
            if self.n1 < 4:
                err_msg = f'sample size n1 ({self.n1}) is too small for mean hypothesis testing'
                raise InvalidSampleSize(err_msg)  
            if self.xbar1 < 1:  
                err_msg = f'sample mean ({self.xbar1}) must be greater than or equal to 1'   
                raise InvalidArgumentPassed(err_msg)             
            #determine sample size  
            if (self.n1 > 30):
                self.size = 'large'
            elif(self.n1 > 4):
                self.size = 'small'
                self.df = self.n1 - 1
            else:
                err_msg = f'sample size ({self.n1}) is too small for difference of mean hypothesis testing'
                raise InvalidSampleSize(err_msg)   
        #proportional hypothesis 
        if self.type == 'prop':
            if all([(self.p > 0), (self.successes > 0), (self.n1 > 0)]):
                # check for sample normalcy 
                normal_test1 = self.n1 * self.p
                normal_test2 = self.n1 * (1 - self.p)
                if normal_test1 > 5 and normal_test2 > 5:
                    self.prop_sample_isnormal = True
                else:
                    err_msg0 = 'Both n * p and n * (1 - p) must be greater than 5'
                    err_msg1 = f'n * p = {normal_test1}'
                    err_msg2 = f'n * (1 - p )= {normal_test2}'
                    err_msg = err_msg0 + '\n\t' + err_msg1 + '\n' + err_msg2
                    raise InvalidHypothesisType(err_msg)
            else:
                err_msg = f'Values for p ({self.p}), successes ({self.successes}), and n ({self.n1}) must all have valid values'
                raise InvalidKeyValueError(err_msg)
        if self.type == "diff_of_props":
            if all([self.p1 != 0, self.p2 != 0, self.n1 > 0, self.n2 > 0]):
                ...
            else:
                err_msg = f'Values for p1 ({self.p1}), p2 ({self.p2}), n1 ({self.n1})and n2 ({self.n2} must all have valid values'
                raise InvalidKeyValueError(err_msg)
                
            
                    
                
    def calculate_hypothesis_test_statisics(self,):   
        import numpy as np     
            
        # if type is difference of mean
        if self.type == "diff_of_mean":
            self.diff_of_means = self.xbar1 - self.xbar2
            if self.sigma1 > 0 and self.sigma2 > 0: 
                frac1 = self.sigma1**2 / self.n1
                frac2 = self.sigma2**2 / self.n2
                self.std_err = np.sqrt((frac1 + frac2))
                # sample size to consider with known population standard deviations  so use z table for 
                self.critical_value = self.datum.get_z_confidencd_level_critical_value(x = self.cl)
                self.me = self.critical_value * self.std_err
                self.a, self.b = (self.diff_of_means + self.me) , (self.diff_of_means - self.me)

            elif self.sigma1 == 0 and self.sigma2 == 0:
                # check to see if this a diff_of mean with unknown sigmas
                #calculate difference of mean
                self.diff_of_means = (self.xbar1 - self.xbar2)               
                # determine if variances are mostly equal 
                if ((self.s1**2 / self.s2**2) > 2) or ((self.s2**2 / self.s1**2) > 2):
                    self.equal_variances = False
                    frac1 = (self.s1**2 / self.n1)
                    frac2 = (self.s2**2 / self.n2)
                    self.std_err = np.sqrt((frac1 + frac2))
                    if self.size == 'large':
                        self.critical_value = self.datum.get_z_confidencd_level_critical_value(x = self.cl)
                    else: 
                        nom = (frac1 + frac2)**2
                        denom = ((1 / (self.n1 - 1)) * (frac1)**2) + ((1 / (self.n2 - 1)) * (frac2)**2)  
                        self.df = np.floor(nom / denom )
                        self.critical_value = self.datum.get_t_confidencd_level_critical_value(x = self.cl, df = self.df)
                    self.me = self.critical_value * self.std_err
                else:
                    self.equal_variances = True 
                    sp = ((self.n1 - 1) * self.var1) + ((self.n2 - 1) *  self.var2) / (self.n1 + self.n2 - 2)
                    self.pooled_variance = np.sqrt(sp)
                    frac1 = 1 / self.n1
                    frac2 = 1 / self.n2
                    self.std_err = np.sqrt((frac1 + frac2))

                    if self.size == 'large':
                        self.critical_value = self.datum.get_z_confidencd_level_critical_value(x = self.cl)
                    else:
                        self.df = self.n1 + self.n2 - 2
                        self.critical_value = self.datum.get_t_confidencd_level_critical_value(x= self.cl, df = self.df)
                          
                    self.me = self.critical_value * self.pooled_variance * self.std_err

            else:
                from colorama import Fore, Style
                print(Fore.RED, Style.BRIGHT + f'Bad parameter configuration for {self.type} test')
                print(Style.RESET_ALL)
                raise InvalidHypothesisType
            
        # TYPE = MEAN
        elif self.type == 'mean':   
            # USE CASE: Hypothesis Test for one or two tail test to analyzing mu - xbar comparison 
            if self.sigma1 > 0:
                # use formula to calculate z for mu - xbar comparison when sigma is known:
                # (xbar - x_observed) / (sigma / square root of n)

                # the critical_value in this case is how many standard deviations alpha is from the mean 
                self.critical_value = self.datum.get_z_critical_value(x = self.auc)
                
                self.test_statistic = round(self.datum.get_z_score(self.xbar1, self.observed_value, self.sigma1, self.n1), 4)
                self.p_value = round(self.datum.get_z_auc(self.test_statistic), 4)
                if self.p_value <= self.alpha:
                    self.significance = True
                else: 
                    self.significance = False
            elif self.sigma1 == 0 and self.s1 > 0:
                if self.size == "large":
                    self.critical_value = self.datum.get_z_confidencd_level_critical_value(x = self.cl)
                else:
                    self.critical_value = self.datum.get_t_critical_value(tail = self.tail, q = self.alpha, df = self.df)
                
                # # I NEEDED TO CONFIRM TO MY SELF THAT CRITICAL VALUE WAS CORRECT 
                # validate_critical_value_alpha = self.datum.get_x_axis_index(x = self.data["x_data"], auc = self.alpha, mu = self.observed_value, sigma = self.s1)
                # validate_critical_value_std_dev = self.datum.get_x_axis_index(x = self.data["x_data"], std_dev = self.critical_value, mu = self.observed_value, sigma = self.s1)
                # print(f'CRITICAL VALUE: {self.critical_value}\nVALIDATE CRITICAL VALUE ALPHA: {self.data["x_data"][validate_critical_value_alpha]}\nVALIDATE CRITICAL VALUE STD_DEV: {self.data["x_data"][validate_crtical_value_std_dev]}')

                self.test_statistic = round(self.datum.get_z_score(self.xbar1, self.observed_value, self.s1, self.n1), 4)
                ######
                self.data['ts_index'] = self.datum.get_x_axis_index(x = self.data['x_data'], std_dev = self.test_statistic, mu = self.xbar1, sigma = self.s1 )
    
                # calculate critical value test based on tail
                # true = within rejection region, false outside rejection region 
                # critical value for upper tail
                #self.data['lower_reg_rej'] = self.data['x_data'][ : self.data['x_data'].index(self.datum.get_closest(lst = self.data["x_data"], x = self.critical_value))]
                if self.tail == "upper":
                    # set the upper region of rejection 
                    self.data['upper_reg_rej']= self.datum.get_rejection_regions(x = self.data["x_data"], tail = 'upper', alpha = self.alpha, observed_value = self.observed_value, sigma = self.s1)

                    # upper critical value upper test
                    # if the ts is greater than cv then in the 
                    self.critical_value_upper = self.datum.is_in_rejection_region(tail = 'upper', test_statistic = self.test_statistic, critical_value = self.critical_value, mu = self.xbar1)                  

                elif self.tail == "lower":
                    # set the lower region of rejection 
                    self.data['lower_reg_rej'] = self.datum.get_rejection_regions(x = self.data["x_data"], tail = 'lower', alpha = self.alpha, observed_value = self.observed_value, sigma = self.s1)

                    # upper critical value upper test
                    # if the ts is greater than cv then in the 
                    self.critical_value_lower = self.datum.is_in_rejection_region(tail = 'lower', test_statistic = self.test_statistic, critical_value = self.critical_value, mu = self.xbar1)
                else:
                    # upper and lower critical value two tail test
                    lower_alpha = self.alpha / 2
                    # need to calculate lower first
                    self.data['lower_reg_rej'] = self.datum.get_rejection_regions(x = self.data["x_data"], tail = 'lower', alpha = lower_alpha, observed_value = self.observed_value, sigma = self.s1)
                    
                    # use the difference between x and the lower rejection region to get the index of the upper region 
                    upper_critical_value_index =  len(self.data["x_data"]) - len(self.data['lower_reg_rej'])                     
                    self.data['upper_reg_rej'] = self.data['x_data'][upper_critical_value_index : ]
                    
                    self.critical_value_two = self.datum.is_in_rejection_region(tail = 'two', test_statistic = self.test_statistic, critical_value = self.critical_value, mu = self.xbar1)                  
                    
                         
                 
                # sigma unknown large sample size 
                if self.size == 'large':
                    # formula replaces sigma with s
                    self.p_value = round(self.datum.get_z_auc(self.test_statistic), 4)
                    if self.p_value <= self.alpha:
                        self.significance = True
                    else:
                        self.significance = False
                else:
                    # small sample size
                    # use student t distribution 
                    self.p_value = self.datum.get_t_auc(self.test_statistic, self.df, self.xbar1)
                    if self.p_value <= self.alpha:
                        self.significance = True
                    else:
                        self.significance = False
            
            else:
                err_msg = 'Arguments are not configured correctly for Single Mean Hypothesis test\n'
                err_msg = err_msg + 'Requirements are Sigma or s, observed_value, xbar, n'
                raise InvalidHypothesisConfiguration(err_msg)    
        elif self.type == 'prop':
            if self.prop_sample_isnormal:
                self.critical_value = self.datum.get_z_confidencd_level_critical_value(x = self.cl)
                self.failures = self.n1 - self.successes
                self.p_hat = self.successes / self.n1
                self.test_statistic = self.datum.get_sample_proportion_zscore(p = self.p, p_hat = self.p_hat, n = self.n1)
                self.data['ts_index'] = self.datum.get_x_axis_index(x = self.data['x_data'], std_dev = self.test_statistic, mu = self.mu, sigma = self.s1 )
                value = self.data["x_data"][self.data["ts_index"]]
                self.p_value = self.datum.get_z_auc(z = self.test_statistic)
                
                # calculate critical value test based on tail
                # true = within rejection region, false outside rejection region 
                # critical value for upper tail
                #self.data['lower_reg_rej'] = self.data['x_data'][ : self.data['x_data'].index(self.datum.get_closest(lst = self.data["x_data"], x = self.critical_value))]
                if self.tail == "upper":
                    # set the upper region of rejection 
                    self.data['upper_reg_rej']= self.datum.get_rejection_regions(x = self.data["x_data"], tail = 'upper', alpha = self.alpha, observed_value = self.p, sigma = self.s1)

                    # upper critical value upper test
                    # if the ts is greater than cv then in the 
                    self.critical_value_upper = self.datum.is_in_rejection_region(tail = 'upper', test_statistic = self.test_statistic, critical_value = self.critical_value, mu = self.mu)                  

                elif self.tail == "lower":
                    # set the lower region of rejection 
                    self.data['lower_reg_rej'] = self.datum.get_rejection_regions(x = self.data["x_data"], tail = 'lower', alpha = self.alpha, observed_value = self.p, sigma = self.s1)

                    # upper critical value upper test
                    # if the ts is greater than cv then in the 
                    self.critical_value_lower = self.datum.is_in_rejection_region(tail = 'lower', test_statistic = self.test_statistic, critical_value = self.critical_value, mu = self.mu)
                else:
                    # upper and lower critical value two tail test
                    lower_alpha = self.alpha / 2
                    # need to calculate lower first
                    self.data['lower_reg_rej'] = self.datum.get_rejection_regions(x = self.data["x_data"], tail = 'lower', alpha = lower_alpha, observed_value = self.p, sigma = self.s1)
                    
                    # use the difference between x and the lower rejection region to get the index of the upper region 
                    upper_critical_value_index =  len(self.data["x_data"]) - len(self.data['lower_reg_rej'])                     
                    self.data['upper_reg_rej'] = self.data['x_data'][upper_critical_value_index : ]
                    
                    self.critical_value_two = self.datum.is_in_rejection_region(tail = 'two', test_statistic = self.test_statistic, critical_value = self.critical_value, mu = self.mu)     
        elif self.type == 'diff_of_props':
            if self.datum.check_proportion_distro_for_normality(self.p1, self.p2, self.n1, self.n2):
                self.p_hat = self.datum.get_phat_for_proportion(self.p1, self.p2, self.n1, self.n2) 
                
        else:
            ...
                  
        self.data['type'] = self.type
        self.data['tail'] = self.tail
        self.data['replacement'] = self.replacement
        self.data['mu'] = self.mu
        self.data['sigma1'] = self.sigma1
        self.data['sigma2'] = self.sigma2
        self.data['n1'] = self.n1
        self.data['n2'] = self.n2
        self.data['xbar1'] = self.xbar1
        self.data['xbar2'] = self.xbar2
        self.data['observed_value'] = self.observed_value
        self.data['p_hat'] = self.p_hat
        self.data['p'] = self.p 
        self.data['s1'] = self.s1
        self.data['s2'] = self.s2
        self.data["var1"] = self.var1
        self.data["var2"] = self.var2
        self.hypothesize_diff = 0 # hypothesized value
        self.data['cl'] = self.cl
        self.data['alpha'] = self.alpha # 
        self.data['lower_alpha'] = self.lower_alpha
        self.data['upper_alpha'] = self.upper_alpha
        self.data['equal_variances'] = self.equal_variances # diff of mean value check if variances are equal  
        self.data['var1'] = self.var1  # sample variance 
        self.data['var2'] = self.var2 # sample variance for diff of mean 
        self.data['diff_of_means'] = self.diff_of_means  # diff or means for diff of mean hypo testing
        self.data['pooled_variance'] = self.pooled_variance  # pooled variance for diff of mean (S_p)
        self.data['std_err'] = self.std_err
        self.data['df'] = self.df # degrees of freedom
        self.data['q'] = self.q # area , used to calculate a, and t values
        self.data['ci'] = self.ci # confidence interval 
        self.data['a'] = self.a # confidence interval lower value 
        self.data['b'] = self.b # confidence interval upper value 
        self.data['test_statistic'] = self.test_statistic
        self.data['p_value'] = self.p_value
        self.data["p1"] = self.p1
        self.data["p2"] = self.p2
        self.data['critical_value'] = self.critical_value # critical value of z or t test 
        self.data['frac1'] = self.frac1
        self.data["frac2"] = self.frac2
        self.data['min_n'] = self.min_n  
        self.data['mar_err_min_n'] = self.mar_err_min_n
        self.data['null_hypo'] = self.null_hypo
        self.data['alt_hypo'] = self.alt_hypo
        self.data["auc"] = self.auc 
        self.data["critical_value_two"] = self.critical_value_two 
        self.data["critical_value_upper"] = self.critical_value_upper
        self.data["critical_value_lower"] = self.critical_value_lower
        self.data["prop_sample_isnormal"] = self.prop_sample_isnormal
        self.data["successes"] = self.successes
        self.data["failures"] = self.failures 
        

        

