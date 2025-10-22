""" 
# datum.py
Data class contains functions to support statistical calculations
"""

from typing import Iterable, List, Dict, Tuple
import numpy as np
import pandas as pd 
import random
from scipy.stats import norm, poisson, binom, t, chi2 
from statsmodels import api 
import copy 
from IPython.display import display, Math, Markdown, HTML 
from dataclasses import dataclass
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression




class InvalidParamEntry(Exception):
    """Raised when invalid parameter is passed"""

class InvalidParamValue(Exception):
    """Raised when invalid parameter is passed"""

class InvalidTypeError(Exception):
    """Raised when invalid type passed as a parameter"""


class InvalidKeyError(Exception):
    """Raised when invalid type is passed as a key """


class InvalidDictError(Exception):
    """Raised when invalid object passed as dictionary """

class Data: 
    
    def __init__(self, N: int = 1, mu: float = 0 , sigma: float = 2, std_out: str = "N"):
        self.N = N
        self.mu = mu
        self.sigma = sigma 
        self.std_out = std_out


    def get_random_item(self, x: Iterable[int | float] = [], rng: Tuple[int, int, int] = (0, 0, 0), cnt: int = 1, replaced: bool = False, seed: int = 0):
        """
        Select random object from a list or random int from range
        
        Parameters
        ----------
        x : Iterable
            optional (x OR rng), default = [] - List of default types to chose from randomly 
        cnt: int
            optional, default = 1 - the count of how many random items to select from a x
        rng : Tuple
            optional (x OR rng) - select a random number from a range where [0] is start, [1] is stop, [3] is step

        seed : int
            int value 
            optional, default = 0, used to create a none-random array based on local host clock

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        Random value from list or range
        """
        if all([isinstance(x, Iterable), isinstance(rng, Tuple), isinstance(seed, int), isinstance(cnt, int), isinstance(seed, int)]):
            if len(x) > 0 and rng[1] > 0:
                err_msg = f'x ({len(x)}) AND rng ({rng}), both cannot be calculated'
                raise InvalidParamValue(err_msg)
            elif cnt < 1:
                err_msg = f'cnt ({len(cnt)}) must be greater than or equal to 1'
                raise InvalidParamValue(err_msg)            
            else: 
                res_array = []
                if seed > 0:
                    random.seed(seed)
                if len(x) > 0:
                    for i in range(cnt):
                        res_array.append(random.choice(x))
                elif rng[1] > 0:
                    if len(rng) == 3:
                        for i in range(cnt):
                            res_array.append(random.randrange(rng[0], rng[1], rng[2]))
                    elif len(rng) == 2:
                        for i in range(cnt):
                            res_array.append(int(random.randrange(rng[0], rng[1])))
                    else:
                        err_msg = f'rng {rng} is must be (x, x) or (x, x, x) lengths'
                        raise InvalidParamValue(err_msg)
                else:
                    for i in range(cnt):
                        res_array.append(random.random())
                return res_array
        else:
            err_msg = f'Invalid type for either x {len(x)}, rng {rng}, or seed {seed}'
            raise InvalidParamEntry(err_msg)

    
    
    def get_random_array(self, low: int | float, high: int | float, cnt: int = 1, dtype: str = 'i', seed: int = 0)-> Iterable:
        """
        Generate a random array of integers or floats
        
        Parameters
        ----------
        low : int | float
            mandatory - the minimum value of the array created
        high : int | float
            mandatory -  the maximum value of the array created

        cnt : int
            optional, default = 1 - the number of values to be included in the array
        dtype : str
            optional, default = i - "i" for integers, "f" for floats  

        Raises
        ======
            InvalidParamEntry

        Returns
            array or list or floats
        -------
        Rand
        """
        if all([isinstance(low, int | float), isinstance(high, int | float), isinstance(cnt, int ), isinstance(dtype, str), isinstance(seed, int)]):
            if seed > 0:
                np.random.seed(seed)
            if dtype.lower() == 'f': 
                return np.random.uniform(low, high, cnt)
            else:
                return np.random.randint(low, high, cnt)
        else:
            err_msg = "lwo, high, cnt, dytype, or seed is wrong type"
            raise InvalidTypeError(err_msg)



    def weigh_array(self, x_arr: Iterable, rng: Tuple, seed: int = 0)->Iterable:
        """
        add random weights to provided array based on provided tuple with low and high ranges
        
        Parameters
        ----------
        x_arr : list
            mandatory - the list to add weights 
        rng : tuple
            mandatory  - the size of each segment to be split
        
        Returns
        -------
        array | list 
            weighted array 
            
        Raises
        ======
        InvalidParamEntry
            Bad parameter passed
            
        """
        if seed > 0:
            random.seed(seed)
        arr = [i +  random.randrange(rng[0], rng[1]) for i in x_arr]
        return arr
        

    def get_chunks(self, chunks : List, size : int):
        """
        split list into equal size lengths based on parameter size
        
        Parameters
        ----------
        chunks : list
            mandatory - the list to be split
        size : int
            mandatory  - the size of each segment to be split
        
        Returns
        -------
        generator iterator 
            contains the split objects you that make up list parameter

        Execution Example
        -------
        chunk_list = []

        for chunk in get_chunks(test_list, test_size):
            chunk_list.append(chunk)
            
        Raises
        ======
        InvalidParamEntry
            Bad parameter passed
            
        """   

        if isinstance(chunks, list) and isinstance(size, int):
            import numpy as np 
            new_size = 0
            if len(chunks) > 250:
                new_size = int(np.ceil(len(chunks)/4))
            if new_size  > size:
                size = new_size
            for chunk in range(0, len(chunks), size):
                yield chunks[chunk:chunk + size]           
        else:
            err_msg = 'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)


    def get_closest(self, lst : list, x_arr : int | float):
        """
        Find the value in the list that is closest to the x_arr value passed as an argument
        
        Parameters
        ----------
        lst: list
            mandatory - a list that contains the values used to search for the closest value
            
        x_arr: int | float
            mandatory - the value used to search the list list 
            
        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        the mean of of the sample proportion 
        """ 
        if isinstance(lst, list) and isinstance(x_arr, int | float):
            ans = lst[min(range(len(lst)), key = lambda i : abs(lst[i] - x_arr))]
            return ans 
        else:
            err_msg = 'lst or x is wrong data type'
            raise InvalidParamEntry(err_msg)


    def make_data(self, N : int = 0, mu: int | float = 0, sigma : int | float = 0, seed : int = 1012):
        """
        create random normal ndarray using numpy.random.generator.integers() and return as a ndarray
        determined by size N, mu, sigma passed as parameters 
        calculate list, min_val, max_val, mu, sigma and count of the return ndarray
        
        Parameters
        ----------
        N : int
            mandatory - array size 
        mu : int | float
            mandatory - mean of the array
        sigma : int | float
            mandatory - standard deviation of the array
        seed : int
            int value used to create a none-random array

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        Series, min_val, max_val, mu, sigma and count of the return list
        """
        if isinstance(N, int) and isinstance(mu, (float, int)) and isinstance(sigma, (float, int)):
            import numpy as np
            rng = np.random.default_rng(seed)
            dist = rng.normal(loc = mu, scale = sigma, size = (N))
            x_arr = list(dist)
            min_val = np.min(x_arr)
            max_val = np.max(x_arr)
            mu = np.mean(x_arr)
            sigma = np.std(x_arr)
            cnt = len(x_arr)
            if self.std_out == 'Y':
                print(f'SAMPLE VALUES:\nsample count: {cnt}\nmin: {round(min_val, 3)}\
                    \nmax:{round(max_val, 3)}\nmean: {round(mu, 3)}\nstd: {round(sigma, 3)}')
            return cnt, min_val, max_val, mu, sigma, x_arr
        else:
            err_msg =  'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)
    

    
    def make_discrete_data(self, N : int = 0, mu: int | float = 0, sigma : float = 0, seed : int = 246810):
        """
        create random integers using numpy.random.generator.integers() and return as a list
        determined by size N, mu, sigma passed as parameters 
        calculate list, min_val, max_val, mu, sigma and count of the return list
        
        Parameters
        ----------
        N : int
            mandatory   
        mu : int | float
            mandatory
        sigma : float
            mandatory
        seed : int
            optional  
            
        Returns
        -------
        list, min_val, max_val, mu, sigma and count of the return list
        
        Raises
        ======
            InvalidParamEntry
        
        """
        if all([isinstance(N, int), isinstance(mu, float | int), isinstance(sigma, float | int), N > 0,  sigma > 0]):
            import numpy as np
            rng = np.random.default_rng(seed)
            low = (mu - (sigma * 2))
            high = (mu + (sigma * 2))
            x_arr = rng.integers(low=low, high=high, size= N)
            min_val = np.min(x_arr)
            max_val = np.max(x_arr)
            mu = np.mean(x_arr)
            sigma = np.std(x_arr)
            cnt = len(x_arr)
            
            if self.std_out == 'Y':
                print(f'SAMPLE VALUES:\nsample count: {cnt}\nmin: {round(min_val, 3)}\
                    \nmax:{round(max_val, 3)}\nmu: {round(mu, 3)}\nsigma: {round(sigma, 3)}')
            N, mu, sigma = 0, 0, 0
            return cnt, min_val, max_val, mu, sigma, x_arr
        else:
            err_msg =  'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)


    def convert_to_std_norm(self, x: Iterable):
        """
        Create a standardize normal distribution based on parameter x
        (i - mu)/sigma 
        
        Parameters 
        ----------
        x : Iterable - pandas.Series, numpy.ndarray, list 
            mandatory - An array that to convert to a standard normal list  
        Returns
        -------
        standard normal list 
        
        Raises
        ======
            InvalidParamEntry
        """
        z = list(x)
        mu = np.mean(z)
        sigma = np.std(z)
        return [(x - mu)/sigma for i in z]
    


    def get_normal_dist(self, x_arr, mu : int | float = 0.0, sigma : int | float = 10.0):
        """
        create a normal distribution based on the parameters x_arr, mu, sigma 
        and low, upp passed as parameters
        is x_arr is a single value, calculate the probability for that one value
        if x_arr is an array, return the calculations for each element in the array
        
        Parameters 
        ----------
        x_arr : list
            mandatory - A single value, or array that is the basis for the probability 
        mu : int | float
            mandatory - the mean used to calculate the probability
        sigma : int | float
            mandatory - the standard deviation used to calculate the probability 

        Returns
        -------
        (int | float) if x_arr is a single value , list if x_arr is an array
        
        Raises
        ======
            InvalidParamEntry
        """
        # $\displaystyle f(x, \mu, \sigma) = \dfrac{1}{\sigma \sqrt{2 \cdot \pi}} \cdot e^{\dfrac{-(x - \mu)^2}{2 \cdot \sigma^2}}$
        # f(x, \mu, \sigma) = (np.pi*sigma) * np.exp(-0.5*((x - mu)/sigma)**2)
        
        if all([isinstance(mu, int | float), isinstance(sigma, int | float)]): 
            import numpy as np 
            if isinstance(x_arr, int | float):
                i = (np.pi*sigma) * np.exp(-0.5*((x_arr - mu)/sigma)**2)
                return i
            else:  
                arr = []
                for i in x_arr:
                    arr.append((np.pi*sigma) * np.exp(-0.5*((i - mu)/sigma)**2)) 
                return arr
        else:
            err_msg = 'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)


    def make_normal_pdf(self, low : int | float , upp : int | float, N : int):
        """
        create a normal probability density distribution based on the parameters 
        lower value, upper value and the amount of elements in the distribution 
        and low, upp passed as parameters

        
        Parameters 
        ----------
        low : int | float
            mandatory - minimal value of the distribution 
        upp : int | float
            mandatory - maximum value of the distribution 
        N : int
            mandatory - the number of elements in the distribution 

        Returns
        -------
        ndarray - a pdf distribution 
        
        Raises
        ======
            InvalidParamEntry
        """
        if all([(isinstance(low, int | float)), (isinstance(upp, int | float)), (isinstance(N, int))]):
            
            import numpy as np
            x_arr = np.linspace(start=low, stop=upp, num = N )
            dist = norm.pdf(x_arr, self.mu, self.sigma)
            return dist
        else:
            err_msg = 'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)           
      
    
    def get_central_tendency(self, data_set: list):
        """
        calculate the count, mean, standard deviation, minimum, and maximum
    
        Parameters
        ----------
        data_set : list
            mandatory - array used to calculate central tendencies 
            
        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        count minimum, maximum, mean, standard deviation of the data_set parameter
        """
        if isinstance(data_set, list): 
            import numpy as np 
            # If data_set is larger than 250 split it in smaller arrays of 250 to manage memory consumption
            if len(data_set) > 250:
                chunk_list = []
                for chunk in self.get_chunks(data_set, 2):
                    chunk_list.append(chunk)
                tup = tuple(chunk_list)
                tup_set = np.vstack(tup)
                cnt = len(tup_set)
                mu = round(np.mean(tup_set), 4)
                sigma = round(np.std(tup_set), 4)
                min_val = np.min(tup_set)
                max_val = np.max(tup_set)  
            else:
                cnt = len(data_set)
                mu = round(np.mean(data_set), 4)
                sigma = round(np.std(data_set), 4)
                min_val = np.min(data_set)
                max_val = np.max(data_set)
            if self.std_out == 'Y':
                print(f'count: {cnt}\n\nmin_val: {min_val}\n\nmax_val: {max_val}\n\nmu: {mu}\n\nsigma: {sigma}')
                    
            return cnt, mu, sigma, min_val, max_val
        else:
            err_msg = 'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)    
        
        
    def get_frequencies(self, data_set: list):
        """
        calculate the unique values, and frequency of the data_set parameter

    
        Parameters
        ----------
        data_set : list
            mandatory More info to be displayed (default is None)

        Raises
        ======
            InvalidParamEntry
            
        Returns
        -------
        unique values, and frequency of the data_set parameter
        """
        if isinstance(data_set, list):
            import numpy as np 
            uniq, freq = np.unique(data_set, return_counts = True)
            return freq, uniq 
        else:
            err_msg = 'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)
    
    
    def get_poisson_distro(self, lam: int = 4, size: int = 1):
        """
        create an a poisson array using numpy's random generator with a seed set to 1016
            The size of the array is determined by:
            1. passing value greater than 1 as the size parameter
            2. setting the class N parameter value class creation
            
        Parameters
        ----------
        lam : int
            Mandatory - the mean of the distribution 

        size: int
            Mandatory  = size fo the distribution 
        
        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        returns a ndarray of N size with a mean of the lambda parameter
        """
        if isinstance(lam, int) and isinstance(size, int):
            import numpy as np 
            rng = np.random.default_rng(1016)
            if lam == 4 and self.mu > 0:
                lam = self.mu
            if size == 1 and self.N > 1:
                size = self.N
            dist =  rng.poisson(lam = lam, size = self.N)
            self.mu = 0
            self.N = 1
            return dist
        else:
            err_msg = 'Invalid Argument passed'
            raise InvalidParamEntry(err_msg) 
    
    
    def get_poisson_pmf_distro(self, mu: int | float, loc: int | float, n: int):
        # mu = expected value as well as lambda in the poisson pmf equation 
        """
        create an array of pmf values based on poisson location, distribution mean and distribution size
        An x-axis array is created first with the range of N
        scipy.stats.poisson.pmf() is used to create the y-axis values (probabilities)
    
        Parameters
        ----------
        mu : int | float
            mandatory - the Expected Value of the distribution mandatory
        loc : int | float
            mandatory - Used the shift of the poisson distribution 
        n : int
            mandatory - The size fo the distribution 
            
        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        x: mandatory - an numpy array of 0 to N values, y: a scipy pmf array of probabilities based on x
        """
        if isinstance(loc, int | float):
            import numpy as np 
            x_arr = np.arange(0, n, 1)
            y = poisson.pmf(x_arr, mu, loc)
            return x_arr, y
        else:
            err_msg = 'Invalid Argument passed'
            raise InvalidParamEntry(err_msg) 


    def get_poisson_pmf_value(self, k: int):
        """
        Calculates the probability mass function of a specific value.

    
        Parameters
        ----------
        k : int
            mandatory - More info to be displayed (default is None)

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        probability of k value 
        """
        if isinstance(k, int):
            return poisson.pmf(k, self.mu)
        else:
            err_msg = 'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)             
    

    def get_poisson_cdf_value(self, k: int):
        """
        Calculates the cumulative density function of a specific range given as a parameter.
    
        Parameters
        ----------
        k : int, 
            mandatory - More info to be displayed (default is None)

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        probability of k value 
        """
        if isinstance(k, int):
            return poisson.cdf(k, self.mu)   
        else:
            err_msg = 'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)        
        

    def get_poisson_ppf_value(self, k : int = 0, mu : int | float = 0 ):
        """
        the percent point function takes the probability value and returns cumulative value 
        corresponding to probability value of the distribution
        
        Parameters
        ----------
            k : int
                mandatory
            mu: float
                mandatory

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        inverse of cdf — in percentiles 
        """
        if isinstance(k, int) and isinstance(mu, int | float):        
            if mu == 0 and self.mu > 0:
                mu = self.mu
            if k == 0:
                raise InvalidParamEntry
            ppf =  poisson.ppf(k,mu)
            k = 0
            return ppf 
        else:
            err_msg = 'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)      
        
            
    
    def get_poisson_prob(self, info : Dict, std_out : str = "N"):
        """
        Calculate the probability of a poisson distribution based on lambda 
        
        Parameters
        ----------
        parameters passed in dictionary info
            
        lambda : int | float
            mandatory - based on the mean of the distribution
        x: int
            mandatory - the number of occurrences observed 
        item: str
            mandatory - the item being calculated. used in the return IPython return 

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        if std_out equals "N": return probability as float value
        If std_out equals "Y": return IPython.display statement describing the probability 
        """
        if isinstance(info, Dict):
            for key, val in info.items():
                if key == "measure":
                    if not isinstance(val, str):
                        raise InvalidKeyError
                elif key == "item":
                    if not isinstance(val, str):
                        raise InvalidKeyError
                elif key == "x":
                    if not isinstance(val, int):
                        raise InvalidKeyError
                elif key == "lambda":
                    if not isinstance(val, int | float):
                        raise InvalidKeyError
            import math
            import numpy as np 
            from IPython.display import display, Math 
            e = math.e 
            dis_e = round(math.e, 3)
            num = round((info["lambda"]**info["x"] * e**(-info["lambda"])), 3)
            den = np.math.factorial(info["x"])

            ans = round((info["lambda"]**info["x"] * e**(-info["lambda"]))/np.math.factorial(info["x"]), 4)
            dis_ans = round(ans * 100, 2)
            if std_out == "N":
                msg = "\\textbf{ }\\lambda = %s\\\\~\\\\"
                msg = msg + '\\textbf{Interval are %s}\\~\\'
                msg = msg + "x = %s\\~\\"
                msg = msg + "P(Y) = \\dfrac{\\lambda^y e^{- \\lambda}}{y!} = \\dfrac{%s^%s %s^{- %s}}{%s!} = \
                            \\dfrac{%s}{%s} = %s\\~\\"
                msg = msg + "\\color{dodgerblue}\\textbf{There was a %s percent chance of observing exactly %s~%s in %s %s}"
                display(Math(msg%(info["lambda"]
                                ,info["measure"]
                                ,info["x"]
                                , info["lambda"], info["x"], dis_e, info["lambda"], info["x"]
                                , num, den, ans
                                , dis_ans, info["x"], info["item"], info["lambda"], info["measure"]))
                        )
            else:
                return dis_ans
            
        else:
            err_msg = 'Invalid Dictionary passed'
            raise InvalidDictError(err_msg)


    
    def get_exp_prob(self, mu : int | float, x : int | float) -> int | float:
        """
        calculate the waiting time between events
     
        Parameters
        ----------
        mu : int | float
            mandatory - expected number of events in time period
        x : int | float
            mandatory - number of events within a certain time frame 

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        probability in int | float format 
        """
        if isinstance(mu, int | float) and isinstance(x, int | float):
            from math import e 
            lam = 1/mu
            return 1 - e**(-lam * x)
        else:
            err_msg = 'Invalid Dictionary passed'
            raise InvalidDictError(err_msg)
            

    def get_var(self, data_set : list): 
        """
        calculate the variance of the data_set parameter
     
        Parameters
        ----------
        data_set : list, mandatory
            More info to be displayed (default is None)
            
        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        standard deviation of the data_set parameter as a int | float
        """
        if isinstance(data_set, list): 
            # 1 - get the mu
            mu = sum(data_set)/len(set)

            # 2 - get the deviations 
            dev_lst = [x - mu for x in data_set]

            # 3 - square the deviations 
            sqrd_dev = [x**2 for x in dev_lst]

            # 4 - sum the deviations 
            sum_sqrd_dev = sum(sqrd_dev)

            # 5 - get variance by dividing the sum of the deviations by the population or sample count
            var = sum_sqrd_dev / len(data_set)
            return var
        else:
            err_msg = 'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)
        

    def get_mean(self, data_set: List):
        
        """
        calculate the mean of the data_set parameter
     
        Parameters
        ----------
        data_set : list
            mandatory - a data set for which the mean will be calculated

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        mean of the data_set parameter as a int | float
        """   
        if isinstance(data_set, list):
            return np.mean(data_set)
        else:
            err_msg = 'Invalid Argument passed to get_mean()'
            raise InvalidParamEntry(err_msg)


    def get_sigma(self, data_set : List)-> int | float:
        """
        calculate the standard deviation of the data_set parameter
     
        Parameters
        ----------
        data_set : list
            mandatory - a data set for which the standard deviation  will be calculated

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        standard deviation of the data_set parameter as a int | float
        """
        if isinstance(data_set, list): 
            # the code below works but I decided to use numpy for efficiency 
            # import math 
            # var = self.get_var(set)
            # # 6 - get standard deviation by squaring variance 
            # sigma = math.sqrt(var)
            # return sigma
            return np.std(data_set)
        else:
            err_msg =  'Invalid Argument passed get_sigma'
            raise InvalidParamEntry(err_msg)   


    def get_median(self, data_set: list):
        """
        calculate the median of the data_set parameter
        median is defined as the middle of the dataset
    
        Parameters
        ----------
        data_set : list
            mandatory - More info to be displayed (default is None)

        Raises
        ======
            InvalidParamEntry        

        Returns
        -------
        median of the data_set parameter as a list
        """
        
        if isinstance(data_set, list):
            import math
            set_len = len(data_set)
            if set_len % 2 == 0:
                x = data_set[int(set_len/2 - 1)]
                y = data_set[int(set_len/2)]
                z = (x + y) / 2
            else:
                z = data_set[(int(math.ceil(set_len/2)) - 1)]
            return round(z, 3)
        else:
            err_msg =  'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)  
   
   
    def get_mode(self, data_set: list):
        """
        mode - the number in the set that appears the most often
        calculate the mode of the data_set parameter
    
        Parameters
        ----------
        data_set : list
            mandatory - More info to be displayed (default is None)
            
        Raises
        ======
            InvalidParamEntry
            
        Returns
        -------
        mode of the data_set parameter as a list
        """
        
        if isinstance(data_set, list):
            import collections 
            data_dict = dict(collections.Counter(data_set))

            max_value = max(list(data_dict.values()))

            mode_val = [num for num, freq in data_dict.items() if freq == max_value]

            if len(mode_val) == len(data_set):
                return 0
            else:
                return mode_val
        else:
            err_msg =  'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)   
        
        
    def convert_to_std_dev(self, x : int | float, mu : int | float, sigma : int | float, std_out : str = "N"):
        """
        Convert a data point on the x axis of a distribution to a standard deviation 
        x = (data_point - mu) / sigma 
        
        Parameters
        ----------
        x : float
            mandatory - data point of interest\n
        mu : float
            mandatory - mean of the distribution. 
        sigma : int | float
            mandatory - the standard deviation of the distribution.
        std_out: str
            optional - IPython.display print out of the result.
            
        Raises
        ======
            InvalidParamEntry
            
        Returns
        -------
        int | float as the z score
        """
        if isinstance(x, int | float) and isinstance(mu, int | float) and isinstance(sigma, int | float):
            z = (x - mu)/sigma
            if std_out.upper() == "Y":
                from IPython.display import display, Math
                msg = '\\displaystyle \\text{x %s is %s standard deviations from the mean %s}'
                
                return display(Math(msg%(x, f'{z: .2f}', mu)))
            else:
                return z
        else:
            err_msg = 'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)
        
        
    def get_x_axis_value(self, z : int | float = 0, sigma : int | float = 0, mu : int | float = 0):
        """
        calculate the value along the x-axis of a normal distribution based on z-score, sigma, and mu
        x = (data_point - mu) / sigma 
        
        Parameters
        ----------
        z : float
            mandatory - z-score / critical value 
        mu : int | float
            mandatory - mean of the distribution 
        sigma : int | float
            mandatory - the standard deviation of the distribution 

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        int | float as the value along the x - axis of normal distribution 
        """
        if all([(isinstance(z, int | float)), (isinstance(sigma, int | float)), (isinstance(mu, int | float))]):
            x = z * sigma + mu
            return x 
        else:
            err_msg = f'Invalid paramete type passed\nz type: {type(z)}, sigma type: {type(sigma)}, mu type: {type(mu)}'
            raise InvalidParamEntry(err_msg)
        
        
    def get_x_axis_index(self, x : list = [], std_dev : int | float = 0, auc : float = 0, mu : int | float = 0, sigma : int | float = 0)-> int:
        """
        calculate the the index if std_dev, that resides within the list x
        1. first calculate the value of the standard deviation based on mu and sigma
        2. find the closest value within the list to the value calculated in step 1 
        
        Parameters
        ----------
        x : list
            mandatory - the list that contains the desired x-axis value 
        std_dev : int | float
            optional (either std_dev or auc) - standard deviation (z-score / critical value )
        auc : int | float
            optional ((either std_dev or auc)) - area under the curve related to the list x
        mu : int | float
            mean of the distribution 
        sigma : int | float
            the standard deviation of the distribution 
            
        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        int 
            value along the x - axis of normal distribution 
        """        
        if all([(isinstance(x, list)), (isinstance(std_dev, int | float)), (isinstance(auc, int | float)), 
                (isinstance(mu, int | float)), (isinstance(sigma, int | float))]):
            if (std_dev == 0 and auc != 0) or (std_dev != 0 and auc == 0): 
                # Use std_dev , not area under curve
                if std_dev != 0: 
                    res = x.index(self.get_closest(x, self.get_x_axis_value(z = std_dev, sigma = sigma, mu = mu)))
                    return res
                # Use area under curve, not std dev
                else:
                    # I dont think this is correct. testing with second line 
                    res = x.index(self.get_closest(x, self.get_x_axis_value(z = self.get_z_critical_value(x = auc), sigma = sigma, mu = mu)))
                    return res
            else:
                err_msg = f'Please provide std_dev {std_dev} OR auc {auc} as arguments. Not both'
                raise InvalidParamEntry(err_msg)   
        else:
            err_msg = f'Invalid paramete type passed\nx type: {type(x)}, std_dev type: {type(std_dev)}, '
            err_msg = err_msg + f'auc: {auc}, sigma type: {type(sigma)}, mu type: {type(mu)}'
            raise InvalidParamEntry(err_msg)

            
    

    def get_z_auc(self, z : int | float, std_out : str = 'N')-> float:
        """
        renamed get_z_percentile to get get_z_auc
        calculate z-table area under the curve (auc) (the positive area above the z value) of a normal distribution where z 
        is as standard deviation value  
        
        Parameters
        ----------
        z : int | float
            mandatory - the standard deviation value used to calculate the normal distribution percentile 

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        float  as percentile
        """
        if isinstance(z, int | float):
            import math 
            if std_out == 'Y':
                
                auc = 0.5 * (math.erf(z/2 ** .5) + 1)
                
                from IPython.display import display, Math 
                msg = '\\displaystyle \\text{The z - score for critial value %s is %s}'
                return display(Math(msg%(f'{z: .2f}', f'{auc: .4f}')))
            else:
                auc =  0.5 * (math.erf(z/2 ** .5) + 1)

                return auc
        else:
            err_msg = 'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)    
        
        
        
        
    def get_z_critical_value(self, x : float, std_out : str = 'N'):
        """
        Z - Distribution critical value (Z - Table) calculation 
    
        Parameters
        ----------
        q: float
            mandatory - probability value of the critical value calculation  
       
       
        Raises
        ======
            InvalidParamEntry
       
        Returns
        -------
        returns the critical value of a z - distribution 
        """ 
        if isinstance(x, float):
            ans = round(norm.ppf(x), 4)
            if std_out == 'Y':
                from IPython.display import display, Math 
                msg = '\\displaystyle \\text{The z - critical value for a probabilility of %s is %s}'
                return display(Math(msg%(x, ans)))
            else:
                return ans 
        else:
            err_msg =  'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)        


    def get_z_confidencd_level_critical_value(self, x : float, std_out : str = 'N'):
        """
        calculate the z critical_value of confidence level based on CL and z-score 
        cv = z_critical_value((1 + cl)/2))
        
        Parameters
        ----------
        x: float
            mandatory - confidence level 
       
        Raises
        ======
            InvalidParamEntry
            
        Returns
        -------
        returns the confidence level critical value of a z - distribution 
        """ 
        if isinstance(x, float):
            cl = (1 + x)/2
            ans = round(norm.ppf(cl), 4)
            if std_out == 'Y':
                from IPython.display import display, Math 
                msg = '\\displaystyle \\text{The z - critical value for the confidence level of %s is %s}'
                return display(Math(msg%(x, ans)))
            else:
                return ans 
        else:
            err_msg = 'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)      


    def get_sample(self, data_set: list, count: int, replace: bool, seed: int = 0)-> list:
        """
        create a random generated sample from the parameter data_set where count parameter is size of sample. 
        If the replace parameter is set to True then an object in the data_set list can be repeated in sample
        
        Parameters
        ----------
        data_set: list
            mandatory - the set which the sample will be derived from 
        count: int
            mandatory - the size of the sample
        replace: bool
            mandatory - When true, if object is selected, it will be 
            replaced back into data_set and can be selected again
            
        seed: bool
            mandatory - if seed is True, default seed 1016 will be used 
            to generate the sample for repeatability

        Returns
        -------
        sample as a list 
        """       
        if all([isinstance(data_set, list ), isinstance(count, int), isinstance(replace, bool), count > 1]):
            import numpy as np
            if seed > 0:
                np.random.seed(seed)
            rnd_choices = np.random.choice(a = data_set, size = count, replace = replace)
            return rnd_choices
        else:
            err_msg =  'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)
        
        
    def get_binom_dist(self, n : int = 0, p : float = 0.5, loc : int | float = 0, size : int = 0, seed : int = 0):
        """
        create a binomial distribution based on parameters 
        
        Parameters
        ----------
        n: int
            mandatory - random variables, 0 based which means setting n to 1 will use list [0, 1] as its variates 
        p: float
            mandatory - probability of n[-1] variate 
        loc: int
            mandatory - the location of the returned array, 0 sets the location based on n[-1]
            replaced back into data_set and can be selected again
        size: int 
            mandatory - the size of the return array 
            
        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        sample as a list 
        """      
        
        if all([isinstance(n, int), isinstance(p, float), isinstance(loc, int | float), isinstance(size, int)]):
            import numpy as np
            if seed > 0:
                np.random.seed(seed)
            binom_arr = binom.rvs(n, p, loc, size)
            return binom_arr 
        else:
            err_msg = 'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)
        

    def get_binom_sigma(self, n_length : int, p : int | float):
        """
        calculate std dev for a binomial distribution  
        
        Parameters
        ----------
        n_length: int
            mandatory - the length of the sample 
        p: float
            mandatory =- probability of successes in n

        Raises
            InvalidParamEntry

        Returns
        -------
        standard deviation of n
        """ 
        if isinstance(n_length, int) and isinstance(p, int | float):
            import numpy as np
            resp = np.sqrt((n_length * p * (1 - p)))
            return resp
        else: 
            err_msg = 'Invalid Argument passed'
            return InvalidParamEntry(err_msg)
        
    
    # def get_successes(self, data_set : list)-> int:
    #     if isinstance(data_set, list):
    #         freq, uniq = self.get_frequencies(data_set)
    #         resp = freq[1]
    #         return resp
    #     else:
    #         from colorama import Fore
    #         print(Fore.RED + 'Invalid Argument passed')
    #         raise InvalidParamEntry()
    
        
    def test_sdsp_normalcy(self, n : int, p : float, std_out: str = "N")-> bool:
        """
        Test to see if the sample is big enough to make a normal SDSP  
        based on sample size n and proportion p
        
        Parameters
        ----------
        n: int
            mandatory - size of the sample
        p: float
            mandatory - the proportion of the sample
            
        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        boolean
        """   
        from IPython.display import display, Math
        if isinstance(n, int) and isinstance(p, float):
            p1, p2  = (n * p), (n * (1 - p))  
            msg = 'n = %s, p = %s\\'
            if p1  < 5 or p2 < 5:
                if std_out.upper() == "Y": 
                    if p1 < 5  and p2 < 5: 
                        msg = msg + '%s \\cdot %s = %s\\'
                        msg = msg + '%s \\cdot (1 - %s ) = %s\\~\\'
                        msg = msg + '\text{Sample failed proportion normalcy test.}'
                        confirm_msg = display(Math(msg%(n, p, n, p, p1, n, p, p2)))
                    elif p1 < 5:
                        msg = msg + '%s \\cdot %s = %s\\~\\'
                        msg = msg + '\text{Sample failed proportion normalcy test.}'
                        confirm_msg = display(Math(msg%(n, p, n, p, p1)))
                    else:
                        msg = msg + '%s \\cdot (1 - %s ) = %s\\~\\'
                        msg = msg + '\\text{Sample failed proportion normalcy test.}'
                        confirm_msg = display(Math(msg%(n, p, n, p, p2)))  
                    return(False, confirm_msg)
                else:
                    return (False, 'no message')
            else:
                if std_out.upper() == "Y": 
                    msg = msg + '%s \\cdot %s = %s\\'
                    msg = msg + '%s \\cdot (1 - %s ) = %s\\~\\'
                    msg = msg + '\\text{Sample passed proportion normalcy test.}'
                    confirm_msg = display(Math(msg%(n, p, n, p, p1, n, p, p2)))  
                    return(False, confirm_msg)
                else:
                    return (True, 'No Message')
        else:
            err_msg = 'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)
        
    
    def get_sample_proportions(self, samples : list | tuple, val):
        """
        Calculate the sample proportion for the provided array passed as a parameter 

        Parameters
        ----------
        samples: list
            mandatory - an array of samples 

        val: int
            mandatory - The true value of the sample
            
        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        SDSP as list 
        """   
        sdsp = []
        if isinstance(samples, list | tuple):
            for sample in samples: 
                get_proportion = (lambda x: 1 if x == val else 0)  # noqa: E731
                # some outcomes may be more than 1 observation so a list of tuple may be in play
                if isinstance(sample, list | tuple):
                    proportion = [1 for x in sample if x == val]
                    resp = len(proportion)/len(sample)
                    sdsp.append(resp)
                else:
                    proportion = get_proportion(sample)
                    sdsp.append(proportion)
            return sdsp 
        else:
            err_msg = 'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)

        
        
    def get_sample_proportion_actual_mu(self, data_set: list)-> int | float:
        """
        Calculate mu_p for the sample proportion data_set passed as a parameter 
        \\mu_{\\hat{p}} = \\sum^N_{i - 1} \\hat{p}_i \\cdot f_i
        
        Parameters
        ----------
        data_set: list
            mandatory - an array that will be used to create samples 
            
        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        the mean of of the sample proportion 
        """ 
        if isinstance(data_set, list):
            arr = []
            freq, uniq = self.get_frequencies(data_set)
            for i in range(len(freq)):
                arr.append(uniq[i] * (freq[i] / len(data_set)))
            resp = sum(arr)
            return resp
        else:
            err_msg = 'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)
        
       
    
    def get_sample_proportion_actual_std_err(self, data_set : list, p : int | float)-> int | float:
        """
        Calculate standard error for the sample proportion data_set passed as a parameter 
        \\sqrt{\\dfrac{2}{p} = \\Sigma^N_{i = 1} \\bigg(\\hat{p}_1 - p\\bigg)^2~p(\\hat{p}_{i})}
        
        Parameters
        ----------
        data_set: list
            mandatory - an array that will be used to create samples 
        p: int | float
            mandatory - an int or float that is the proportion of the population
            
        Raises
        ======
            InvalidParamEntry
        
        Returns
        -------
        the mean of of the sample proportion 
        """ 
        if isinstance(data_set, list) and isinstance(p, int | float):
            import numpy as np 
            freq, uniq = self.get_frequencies(data_set=data_set)
            # first calculate the variance 
            arr = []
            prop = sum(freq) # the denominator of the proportion , ea freq will be the numerator 
            for i in range(len(freq)):
                arr.append(((uniq[i] - p)**2) * (freq[i]/prop))
            var = sum(arr) # the variance 
            
            se = np.sqrt(var) # Standard Error 
            return se 
        else:
            err_msg = 'Invalid Argument passed'
            return InvalidParamEntry(err_msg)
        
               
               
    def get_sample_proportion_std_err(self, p_hat : int | float, n : int | float):
        """
        Calculate standard deviation for the sample proportion based on the parameter n and p_hat
        
        Parameters
        ----------
        n: int | float
            mandatory - the number of samples 
        p_hat: int | float
            mandatory - proportion of the samples 

        Raises
        ======
            InvalidParamEntry 

        Returns
        -------
        the standard deviation of of the sample proportion 
        """ 
        if isinstance(p_hat, int | float) and isinstance(n, int | float):
            import numpy as np
            resp = np.sqrt((p_hat * (1 - p_hat))/n)
            return resp 
        else: 
            err_msg = 'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)
        
        
    def get_sample_proportion_std_err_with_fpc(self, p_hat : int | float, n : int | float, N : int | float):
        """
        Calculate standard error for the sample proportion based on the parameter n, p_hat and N with finite correction factor
        
        Parameters
        ----------
        n: int | float
            mandatory - the size of n
        p_hat: int | float
            mandatory - proportion of the samples 
        N: int | float
            mandatory - the size of N
            
        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        the standard error with finite population correction
        """ 
        if all([isinstance(p_hat, int | float), isinstance(n, int | float), isinstance(N, int | float)]):
            import numpy as np
            resp = (np.sqrt(((p_hat * (1 - p_hat)) / n)) ) * (np.sqrt((N - n)/(N - 1)))
            return resp 
        else: 
            err_msg = 'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)
        
    
    def get_sample_proportion_zscore(self, p: int | float, p_hat : int | float, n : int | float):
        """
        Calculate z score  for the sample proportion based on the parameter n and p
        
        Parameters
        ----------
        n: int | float
            mandatory - the number of samples 
        p: int | float
            mandatory - proportion of the population 
        p: int | float
            mandatory - proportion of the population: int | float, mandatory - proportion of the sample

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        the standard deviation of of the sample proportion 
        """ 
        if isinstance(p, int | float) and isinstance(n, int | float):
            import numpy as np
            resp = (p_hat - p)/np.sqrt((p * (1 - p))/n)
            return resp 
        else: 
            err_msg = 'Invalid Parameter Entry'
            raise InvalidParamEntry(err_msg)      
            

    def get_matched_pair_tscore(self, d_bar: int | float, mu_d: int | float, s_d: int | float, n: int)->Tuple:
        """
       Calculate test statistic for matched pair sample with small sample size 
        
        Parameters
        ----------
        d_bar: int | float
            mandatory - mean of the matched pair differences
        mu_d: int | float
            mandatory - mean of the observed data
        s_d: int | float
            mandatory - standard deviation of the matched pair differences
        n: int | float
            mandatory - the number of samples 

        p: int | float
            mandatory - proportion of the population: int | float, mandatory - proportion of the sample
            
            
        Raises
        ======
            InvalidParamEntry, InvalidParameterValue

        Returns
        -------
        tuple - (d_bar - mu_d), s_d / sqrt(n) test statistic of matched pair sample
        """
        if all([isinstance(d_bar, int | float), isinstance(mu_d, int | float), isinstance(s_d, int | float), isinstance(n, int)]):

            nom = (d_bar - mu_d)
            denom = s_d / np.sqrt(n)
            test_stat = nom / denom 

            return (nom, denom, test_stat)
        else:
            err_msg = 'Invalid Argumenmt(s) Passed.\n(d_bar: int | float, mu_d: int | float, s_d: int | float, n: int)'
            raise InvalidParamEntry(err_msg) 


    def get_geometric_probability(self, info : Dict, std_out : str = "N"):
        """
        Geometric probability 
        
        Parameters
        ----------
        n: int | float
            mandatory - the number of samples 
        p: int | float
            mandatory - proportion of the population 
        p: int | float
            mandatory - proportion of the population: int | float, mandatory - proportion of the sample
            
            
        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        the standard deviation of of the sample proportion 
        """ 
        if isinstance(info, dict):
            for key, val in info.items():
                if key == "statement":
                    if not isinstance(val, str):
                        raise InvalidKeyError
                elif key == "n":
                    if not isinstance(val, int):
                        raise InvalidKeyError
                elif key == "success":
                    if not isinstance(val, int | float):
                        raise InvalidKeyError
            from IPython.display import display, Math 
            failures = 1 - info["success"]
            attempts = failures**((info["n"] - 1))
            ans = info["success"] * attempts
            dis_ans = round(ans * 100, 2)
            if std_out == "N":
                msg = "\\textbf{Probability: } = %s\\~\\"
                msg = msg + '\\textbf{Number of attempts: %s}\\~\\'
                msg = msg + "P(S = n) = P(1 - P)^{n - 1} = %s(1 - %s)^{%s - 1} = %s \\cdot %s^{%s} = %s \\cdot %s = %s\\~\\"
                msg = msg + "\\color{dodgerblue}\\textbf{The probability of %s after %s attempts is %s}"
                display(Math(msg%(info["success"]
                                  , info["n"]
                                  , info["success"], info["success"], info["n"], info["success"], round(failures, 4), (info["n"] - 1)
                                  , info["success"], round(attempts, 4), round(ans, 4) 
                                  , info['statement'], info["n"], dis_ans
                        )))
            else:
                return ans
            
        else:
            err_msg = 'Invalid Dictionary format passed'
            raise InvalidDictError(err_msg)
        

    def get_t_auc(self, critical_values : List = [], df : int = 0, mu : int | float = 0):
        """
        calculate t-table area under the curve (auc) of a normal distribution where critical_value
        is as standard deviation value  
        
        Parameters
        ----------
        critical_values : int | float
            mandatory - a list of standard deviations to convert to student t areas under the curve 
        df : int
            mandatory - the degrees of freedom 
        mu : int | float
            mandatory - the mean of the distributions that contains the critical values 

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        float  as percentile
        """
        if all([(isinstance(df, int)), (isinstance(mu, int | float))]):
            
            auc =  t.pdf(critical_values, df, mu)
            return auc
        else:
            err_msg = f'Argument types:\ndf: {type(df)}\nmu: {type(mu)}'
            raise InvalidParamEntry(err_msg) 
            

    def get_t_critical_value(self, tail : str, q : float = 0.0, df : int = 0, std_out : str = 'N'):
        """
        T - Distribution critical value (T - Table) calculation
        Returns a standard deviation  based on tail, degrees of freedom  
        
        Parameters
        ----------
        tail: str
            mandatory - determines lower, upper or two tail critical value 
        q: float
            mandatory - significance level (alpha) 
        df: int
            mandatory if confidence value is not provided - degrees of freedom value of the critical value calculation 

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        returns the critical value of a t - distribution 
        """ 

        if all([(isinstance(tail, str)), (isinstance(q, float)), (isinstance(df, int))]):
            if tail.lower() in ['lower', 'upper', 'two']:
                if tail.lower() == 'upper':
                    q = 1 - q
                    ans = t.ppf(q = q, df = df)
                    if std_out == 'Y':
                        from IPython.display import display, Math 
                        msg = '\\displaystyle \\text{The %s tail critical value for a probabilility of %s with %s degrees of freedom is %s}'
                        return display(Math(msg%(tail, q, df, ans)))
                    else:
                        return ans 
                elif tail.lower() == 'lower':
                    ans = t.ppf(q = q, df = df)
                    if std_out == 'Y':
                        from IPython.display import display, Math 
                        msg = '\\displaystyle \\text{The %s tail critical value for a probabilility of %s with %s degrees of freedom is %s}'
                        return display(Math(msg%(tail, q, df, ans)))
                    else:
                        return ans                 
                elif tail.lower() == 'two':
                    q = 1 - (q/2) # is this the issue 11/8/23 @ 2:21 pm `
                    ans = t.ppf(q = q, df = df)
                    if std_out == 'Y':
                        from IPython.display import display, Math 
                        msg = '\\displaystyle \\text{The %s tail critical value for a probabilility of %s with %s degrees of freedom is %s}'
                        return display(Math(msg%(tail, q, df, ans)))
                    else:
                        return ans 
            else:
                err_msg = f'tail value ({tail}) is not a valid tail argument  .\nvalid tail options are lower, upper, two.'
                raise InvalidParamEntry(err_msg)               
            
        else:
            err_msg =  'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)
    


    def get_t_confidencd_level_critical_value(self, x : float, df : int, std_out : str = 'N'):
        """
        calculate the z critical_value of confidence level based on CL and z-score 
        cv = z_critical_value((1 + cl)/2))
        
        Parameters
        ----------
        x: float
            mandatory - area under the curve 
        df: int
            mandatory - degrees of freedom 
       
       Raises
       ======
        InvalidParamEntry

        Returns
        -------
        returns the confidence level critical value of a z - distribution 
        """ 
        if isinstance(x, float) and isinstance(df, int):
            cl = (1 + x)/2
            ans = round(t.ppf(cl, df), 4)
            if std_out == 'Y':
                from IPython.display import display, Math 
                msg = '\\displaystyle \\text{The z - critical value for the confidence level of %s is %s}'
                return display(Math(msg%(x, ans)))
            else:
                return ans 
        else:
            err_msg = 'Invalid Argument passed'
            raise InvalidParamEntry(err_msg)     


    def get_pvalue(self, test_statistic : int | float = 0, tail : str = ''):
        """
        calculate p-value based on test statistic and either lower, upper, or two tail test 
        
        |         Test           |      Calculation        |
        |:----------------------:|:-----------------------:|
        | One Tail - Lower       |         p = ts          | 
        | One Tail - Upper       |       p = 1 - ts        |
        | Two Tail with neg z    |       p = ts * 2        |
        | Two Tail with pos z    |    p = - (1 - ts) * 2   |
        
        Parameters
        ----------
        test_statistic: int | float
            mandatory - the calculated test statistic  
        tail: str
            mandatory - lower, upper or two 

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        float -> p_value
        """      
        
        if isinstance(test_statistic, int | float) and isinstance(tail, str):
            if tail in ['upper', 'lower', 'two']:
                # z_score is used to check to get the upper and lower bounds of a two tail test
                z_score = self.get_z_auc(test_statistic)
                if tail == 'lower':    
                    p_value = test_statistic
                elif tail == 'upper':
                    p_value = 1 - test_statistic
                else:
                    if z_score < 0:
                        p_value = test_statistic * 2
                    else:
                        p_value = (1 - test_statistic) * 2
                return p_value
            else:
                err_msg = f'{tail} is not a valid tail option'
                raise InvalidParamEntry(err_msg)  
        else:
            err_msg = f'either {test_statistic} or {tail} are invalid datatypes'
            raise InvalidParamEntry(err_msg)  
        
        
    def get_chi_square_ctitical_value(self, alpha: int | float, df: int):
        """
        calculate the chi square critical value based on the alpha value and degrees of freedom 
        
        Parameters
        ----------
        alpha: int | float
            mandatory - alpha value of the hypothesis test
        df: int 
            mandatory - degrees of freedom 

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        critical value -> float
        """  
        if isinstance(alpha, float) and isinstance(df, int):
            return chi2.ppf(q = (1 - alpha), df = df)
        else:
            err_msg = f'alpha (type {type(alpha)}) must be float and df (type {type(df)}) must be of type int'
            raise InvalidParamEntry(err_msg)
        
    
    def get_z_score(self, mu : int | float = 0, observed_value : int | float = 0, std_dev : int | float = 0, n : int = 0, std_out = 'N'):
        """
        calculate z-score given the required arguments are provided: mu, xbar, sigma, n

        Z = \\dfrac{\\mu - \\bar{x}}{\\dfrac{\\sigma}{\\sqrt{n}}}

        Parameters
        ----------
        mu: int | float
            mandatory - population mean
        xbar: int | float
            mandatory - sample mean
        std_dev: int | float
            mandatory - either population standard deviation or sample standard deviation 
        n: int | float
            mandatory - sample size

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        z-score -> float
        """            
        if all([isinstance(mu, int | float), isinstance(observed_value, int | float), isinstance(std_dev, int | float), isinstance(n, int)]):
            import numpy as np
            nom = f'{mu - observed_value: .2f}'
            denom = f'{(std_dev / np.sqrt(n)): .2f}'
            if std_out.upper() == "Y":
                from IPython.display import display, Math
                
                # ans =  f'{(np.abs((mu - observed_value)/(std_dev/np.sqrt(n)))): .4f}'
                ans =  (mu - observed_value)/(std_dev/np.sqrt(n))
                
                msg = '\\displaystyle zscore~\\approx \\dfrac{\\mu - x_o}{\\dfrac{\\sigma}{\\sqrt{n}}} = '
                msg = msg + '\\dfrac{%s - %s}{\\dfrac{%s}{\\sqrt{%s}}} = \\dfrac{%s}{%s} = %s'
            
                return display(Math(msg%(mu, observed_value, std_dev, n, nom, denom, f'{ans: .2f}')))

            else:
                return (mu - observed_value)/(std_dev/np.sqrt(n))
        else:
            err_msg = 'invalid paramter passed to get_z_score(mu, xbar, sigma, n)'
            raise InvalidParamEntry(err_msg)
        
                  
                  
    def check_normality(self, x : list = []):
        """
        Use the emperical rule to check for the normalcy of a distribution as a list
        
        
        Parameters
        ----------
        x: list
            mandatory- a list that represents a distribution
            
        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        string in the form of IPython display
        """             
        if isinstance(x, list):
            from IPython.display import display, Math 
            import numpy as np
            
            mu = np.mean(x)
            sigma = np.std(x)
            min_val = np.min(x)
            max_val = np.max(x)
            
            std_dev1 = ((mu - sigma), (mu + sigma))
            std_dev2 = ((mu - (sigma * 2)), (mu + (sigma * 2)))
            std_dev3 = ((mu - (sigma * 3)), (mu + (sigma * 3)))

            std_dev1_cnt = 0
            std_dev2_cnt = 0
            std_dev3_cnt = 0

            #emperical = [std_dev1, std_dev2, std_dev3]

            for val in x:
                if all([(val >= std_dev1[0]), (val <= std_dev1[1])]):
                    std_dev1_cnt +=1
                if all([(val >= std_dev2[0]), (val <= std_dev2[1])]):
                    std_dev2_cnt +=1
                if all([(val >= std_dev3[0]), (val <= std_dev3[1])]):
                    std_dev3_cnt +=1

            msg = '\\displaystyle \\mu: %s\\\\sigma: %s\\\\'
            msg = msg + '\\text{minimum value: }%s\\text{maximum value: }%s\\\\~\\\\'
            msg = msg + '\\text{Emperical Rule:}\\\\~\\\\\\text{1 Standard Deviation from mean: 68 percent of distribution}\\\\~\\\\'
            msg = msg + '\\qquad \\star~ %s \\pm %s \\Rightarrow (%s, %s)\\\\~\\\\'
            msg = msg + '\\qquad \\star~ %s \\text{ pct of the data resides within 1 standard deviation}\\\\~\\\\'
            msg = msg + '\\text{2 Standard Deviation: 95 percent of distribution}\\\\~\\\\'
            msg = msg + '\\qquad \\star~ %s \\pm 2 \\cdot %s \\Rightarrow (%s, %s)\\\\~\\\\'
            msg = msg + '\\qquad \\star~ %s \\text{ pct of the data resides within 2 standard deviation}\\\\~\\\\'
            msg = msg + '\\text{3 Standard Deviation: 95 percent of distribution}\\\\~\\\\'
            msg = msg + '\\qquad \\star~ %s \\pm 3 \\cdot %s \\Rightarrow (%s, %s)\\\\~\\\\'
            msg = msg + '\\qquad \\star~ %s \\text{ pct of the data resides within 3 standard deviation}\\\\~\\\\'
            msg = msg + '\\color{gainsboro} \\text{If each standard deviation is within 5 percent of the emperical rule then }'
            msg = msg + '\\text{you can consider the distribution normal}'

            display(Math(msg%(
                f'{mu: .4f}', f'{sigma: .4f}'
                ,min_val, max_val
                ,f'{mu: .4f}', f'{sigma: .4f}', f'{std_dev1[0]: .4f}', f'{std_dev1[1]: .4f}'
                , f'{(std_dev1_cnt/len(x) * 100): .2f}'
                ,f'{mu: .4f}', f'{sigma: .4f}', f'{std_dev2[0]: .4f}', f'{std_dev2[1]: .4f}'
                , f'{(std_dev2_cnt/len(x) * 100): .2f}'
                ,f'{mu: .4f}', f'{sigma: .4f}', f'{std_dev3[0]: .4f}', f'{std_dev3[1]: .4f}'
                , f'{(std_dev3_cnt/len(x) * 100): .2f}'
            )))
        else:
            err_msg = f'invalid paramter passedto check_normality(x) as type {type(x)}'
            raise InvalidParamEntry(err_msg)
        
        
    def case_against_null(self, p_value : int | float = 0):
        """
        calculate the evidence against the null hypothesis 
        
        Parameters
        ----------
        p_value: int | float
            mandatory - p-value of hypothesis 

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        (str) evidence against null hypothesis statement based on p-value  
        """ 
        if isinstance(p_value, float):
            if p_value < .999: 
                if p_value > 0.10:
                    return f"A p-value with a value of {p_value} has weak or no evidence against the Null Hypotheis"
                elif p_value > 0.05 and p_value <= 0.10:
                    return f"A p-value with a value of {p_value} has moderate evidence against the Null Hypotheis"
                elif p_value >= 0.01 and p_value <= 0.05:
                    return f"A p-value with a value of {p_value} has stong evidence against the Null Hypotheis"
                elif p_value < 0.01:
                    return f"A p-value with a value of {p_value} has very stong evidence against the Null Hypotheis"
                else:
                    return f'There is no statistical evidence for a p-value of {p_value}'                  
            else:
                err_msg = f'Invalid p-value value {p_value}'
                raise InvalidParamValue(err_msg)
        else:
            err_msg = f'invalid paramter passed to case_aginst_null(p_value) as type {type(p_value)}'
            raise InvalidParamEntry(err_msg)
        
                        
                
    def get_rejection_regions(self, x: list = [], tail : str = '', alpha: float = 0, observed_value: int | float = 0, sigma: int | float = 0):

        """
        Create hypothesis test rejection region 
        
        Parameters
        ----------
        x: list
            mandatory - x-axis array that will contain the region of rejection 
        tail: str
            mandatory - lower, upper, or two tail test
        alpha: float
            mandatory - the significance level that will define the bound of the region of rejection
        observed_value: int | float
            mandatory - the mean of the x 
        sigma: int | float
            mandatory - the standard deviation of x


        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        (list) x-axis values that define the region of rejection 
        """ 
        if all([(isinstance(x, list)), isinstance(tail, str), (isinstance(alpha, int | float)), (isinstance(observed_value, int | float)), (isinstance(sigma, int | float))]):
            if tail.lower() in ["lower", "upper", "two"]:
                if tail == "upper":
                    # set the upper region of rejection 
                    upper_critical_value_index = (self.get_x_axis_index(x = x,  auc = (1 - alpha), mu = observed_value, sigma = sigma) + 1)
                    upper_reg_rej = x[upper_critical_value_index : ]
                    return upper_reg_rej


                elif tail == "lower":
                    # set the lower region of rejection 
                    lower_critical_value_index = (self.get_x_axis_index(x = x, auc = alpha, mu = observed_value, sigma = sigma) + 1)
                    lower_reg_rej = x[ : lower_critical_value_index]
                    return lower_reg_rej

                else:
                    # upper and lower critical value two tail test
                    lower_alpha = alpha / 2

                    lower_critical_value_index = (self.get_x_axis_index(x = x, auc = lower_alpha, mu = observed_value, sigma = sigma) + 1)
                    lower_reg_rej = x[ : lower_critical_value_index]
                    
                    # use the difference between x and the lower rejection region to get the index of the upper region 
                    upper_critical_value_index =  len(x) - len(lower_reg_rej)                     
                    upper_reg_rej = x[upper_critical_value_index : ]
                    return lower_reg_rej, upper_reg_rej
            else:
                err_msg = f'tail ({tail}, must be upper, lower, or two)'
                raise InvalidParamValue(err_msg)
        else:
            err_msg = 'invalid paramter passed to get_rejection_regions(x_list, tail, alpha, observed_value, sigma) '
            raise InvalidParamEntry(err_msg)
    
    
    def is_in_rejection_region(self, tail: str = '', test_statistic: int | float = 0, critical_value: int | float = 0, mu: int | float = 0):
        
        """
        Create hypothesis test rejection region 
        
        Parameters
        ----------
        tail: str
            mandatory - lower, upper, or two tail test
        test_statistic: int | float
            mandatory - the calculated z score
        critical_value: int | float
            mandatory - boundary of region of rejection in standard deviations 
        mu: int | float
            mandatory - the mean of the x-axis where the region of rejection resides


        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        (bool) True if test statistic is within the region of rejection                                  
        """ 
            
        if all([(isinstance(tail, str)), isinstance(test_statistic, int | float), (isinstance(critical_value, int | float)), (isinstance(mu, int | float))]):
            if tail.lower() in ["lower", "upper", "two"]:
        
                # upper critical value upper test
                # if the ts is greater than cv then in the                   
                if tail.lower() == "upper": 
                    if test_statistic > critical_value:
                        return True # in the region of rejection 
                    else:
                        return False
                        
                # lower critical value lower test
                # if the ts is less than cv then in the 
                elif tail.lower() == "lower":
                    if test_statistic < critical_value:
                        return True # in the region of rejection 
                    else:
                        return False
                else:
                    if test_statistic >  mu:
                        if test_statistic > critical_value:
                            return True # in the region of rejection 
                        else:
                            return False
                    else:
                        if test_statistic < critical_value:
                            return True # in the region of rejection 
                        else:
                            return False
            else:
                err_msg = f'tail ({tail}, must be upper, lower, or two)'
                raise InvalidParamValue(err_msg)
        else:
            err_msg = 'invalid paramter passed to is_in_rejection_region(tail, test_statistic, critical_value, mu) '
            raise InvalidParamEntry(err_msg)
                    
    
    def check_proportion_distro_for_normality(self, p1: float, p2: float, n1: int, n2: int)->bool:
        """
        determine if samples for difference of proportion are normal
        phat = ((p1 * n1) + (p2 * n2)) / (n1 + n2)
        
        Parameters
        ----------
        p1 : float
            mandatory - sample 1 proportion 
        p2 : float
            mandatory - sample 2 proportion 
        n1: int
            mandatory - sample 1 size
        n2: int
            mandatory - sample 2 size

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        (bool) True if n1 and n2 are normal distributions   
        """
        if all([isinstance(p1, float), isinstance(p2, float), isinstance(n1, int), isinstance(n2, int)]):
            return all([(n1 * p1 >= 5), (n1 * (1 - p1) >= 5), (n2 * p2 >= 5), (n2 * (1 - p2) >= 5)])
        

    def get_phat_for_proportion(self, p1: float, p2: float, n1: int, n2: int)->int | float:
        """
        Calculate phat that is used in the difference of proportion test statistic formula 
        phat = ((p1 * n1) + (p2 * n2)) / (n1 + n2)
        
        Parameters
        ----------
        p1 : float
            mandatory - sample 1 proportion 
        p2 : float
            mandatory - sample 2 proportion
        n1: int
            mandatory - sample 1 size
        n2: int
            mandatory - sample 2 size

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        (int | float) phat value for difference of proportion                                   
        """ 
        if all([isinstance(p1, float), isinstance(p2, float), isinstance(n1, int), isinstance(n2, int)]):
            
            return ((p1 * n1) + (p2 * n2)) / (n1 + n2)
        else:
            err_msg = 'invalid paramter passed to get_phat_for_proportion(p1(float), p2(float), n1(int), n2(int)) '
            raise InvalidParamEntry(err_msg)  
        
    def get_test_statistic_for_diff_of_props(self, p_diff: int | float,  phat: float, p1: float, p2: float, n1: int, n2: int)->int | float:
        
        return ((p1 - p2) - p_diff) / (np.sqrt(phat * (1 - phat) * ((1/n1) + (1/n1))))
    
    
    def get_slope(self, x: List, y: List): 
        """
        Calculate the slope (m) of a y intercept 
        
        Parameters
        ----------            
        x: list
            mandatory - a list of independent variables 
        y: list
            mandatory - a list of dependent variables 

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        m - the calculated slope of y intercept 
        """        
        
        if isinstance(x, list) and isinstance(y, list):
            if len(x) > 3 and len(y) > 3:
                n = len(x)
                xy = [x[i] * y[i] for i in range(len(x))]
                sigma_x = sum(x)
                sigma_y = sum(y)
                sigma_xy = sum(xy)
                sigma_squaredX_sum = sum([i**2 for i in x])
                sigma_squaredX = (sum(x))**2
                m = ((n * sigma_xy) - (sigma_x * sigma_y)) / ((n * sigma_squaredX_sum) - sigma_squaredX)
                return m
            else:
                err_msg = f'x length {len(x)}, y length {len(y)}. The length of both x and y must be greater than 5'
                raise InvalidParamValue(err_msg)
        else:
                err_msg = 'x and y must be of the type list'
                raise InvalidParamEntry(err_msg)  
            
    def get_beta1(self, r: int | float, x_arr: List, y_arr: List):
        """
        Calculate the slope (m) of a y intercept 
        
        Parameters
        ----------            
        x: list
            mandatory - a list of independent variables 
        y: list
            mandatory - a list of dependent variables 

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        m - the calculated slope of y intercept 
        """  
        if all([isinstance(r, int | float), isinstance(x_arr, list), isinstance(y_arr, list)]):
            s_y = self.get_sigma(y_arr)
            s_x = self.get_sigma(x_arr)   
            b_1 = r * (s_y/s_x)
            return b_1
        else: 
            err_msg = 'Invalid argument passed to get_beta1()'
            raise InvalidParamEntry(err_msg)
        
            
    def get_y_intercept(self, x: List, y: List, m: int | float): 
        """
        Calculate the y-intercept 
        
        Parameters
        ----------            
        x: list
            mandatory - a list of independent variables 
        y: list
            mandatory - a list of dependent variables 
        m: int | float
            mandatory - the slope 

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        m - the calculated the y intercept 
        """ 
        if all([isinstance(x, list), isinstance(y, list), isinstance(m, int | float)]):
            if len(x) > 3 and len(y) > 3:
                n = len(x)
                sigma_x = sum(x)
                sigma_y = sum(y)
                b = (sigma_y - (m * sigma_x)) / n
                return b
            else:
                err_msg = f'x length {len(x)}, y length {len(y)}. The length of both x and y must be greater than 5'
                raise InvalidParamValue(err_msg)
        else:
                err_msg = 'x and y must be of the type list'
                raise InvalidParamEntry(err_msg)  
            
    
    def get_beta0(self, b_1: int | float, x_arr: List, y_arr: List):
        """
        Calculate the beta_0 of  yhat = beta0 + beta1 * x 
        
        Parameters
        ----------            
        b_1: int | float
            mandatory - the slope of yhat = beta0 + beta * x
        x_arr: list
            mandatory - a list of independent variables 
        y_arr: list
            mandatory - a list of dependent variables 

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        beta0 (m or slope) - the calculated the y intercept 
        """ 
        mu_y = self.get_mean(y_arr)
        mu_x = self.get_mean(x_arr)
        b_0 = mu_y - (b_1 * mu_x)
        return b_0
            
            
    def get_y_intercept_predicted_value(self, x: int | float, m: int | float, b: int | float):
        """
        Calculate the predicted value of an y-intercept based on x
        
        Parameters
        ----------            
        x: int | float
            mandatory - x dependent variable 
        m: int | float
            mandatory - the slope 
        b: int | float
            mandatory - y-intercept 

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        predicted value of y-intercept  
        """ 
        pred_value = m * x + b 
        return pred_value
        
        

    def get_covariance(self, x: List, y: List):
        """
        Calculate the covariance of x and y list  
        Covariance is the mean value of the product of the deviations of x and y 
        from their respective means 

        mean of (x - mu_x) * (y - mu_y)
        
        Parameters
        ----------            
        x_arr: list
            mandatory - a list of independent variables 
        y: list
            mandatory - a list of dependent variables 

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        cov - the calculated covariance of x and y

        """
        if isinstance(x, list) and isinstance(y, list):
            mu_x = np.mean(x)
            mu_y = np.mean(y)
            cov = np.mean([(x[i] - mu_x) * (y[i] - mu_y) for i in range(len(x))])
            return cov
        else:
                err_msg = 'x and y must be of the type list'
                raise InvalidParamEntry(err_msg)  
        
            
            
    def get_corr_coeff(self, cov: int | float, s_x: int | float, s_y: int | float):
        """
        Calculate the y-correlation coefficient 
        
        Parameters
        ----------            
        x_arr: list
            mandatory - a list of independent variables 
        y: list
            mandatory - a list of dependent variables 
        data: bool
            optional - if True return x, y, x*2, y^2 and xy with sums in form of dictionary
            headers:  


        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        r - the calculated the correlation coefficient 
        info - x, y, x*2, y^2 and xy with sums in form of dictionary
        """ 
        if all([isinstance(cov, int | float), isinstance(s_x, int | float), isinstance(s_y, int | float)]): 
            r = cov / (s_y * s_x)
            return r
        else:
                err_msg = 'x and y must be of the type list'
                raise InvalidParamEntry(err_msg)   
    

    def chart_regression(self, x: List, y: List):
        x_tbl = copy.copy(x)
        y_tbl = copy.copy(y)
        
        mu_x = np.mean(x)
        mu_y = np.mean(y)
        s_x = np.std(x)
        s_y = np.std(y)
        xy = [x[i] * y[i] for i in range(len(x))]
        var_x = [x[i] - mu_x for i in range(len(x))]
        var_y = [y[i] - mu_y for i in range(len(y))]
        mu_x_sqr = [(i - mu_x)**2 for i in x]
        mu_y_sqr = [(i - mu_y)**2 for i in y]
        mu_x_mu_y = [var_x[i] * var_y[i] for i in range(len(x))]

        # get sums 
        x_sum = sum(x)
        y_sum = sum(y)
        xy_sum = sum(xy)
        mu_x_sqr_sum = sum(mu_x_sqr)
        mu_y_sqr_sum = sum(mu_y_sqr)
        cov = sum(mu_x_mu_y) # covariance is the sum of (x - mu_x) * (y - mu_y)
        mu_cov = np.mean(mu_x_mu_y)
        col1 = list(range(1, (len(x) + 1)))

        # add sum the columns 
        x_tbl.append(x_sum)
        y_tbl.append(y_sum)
        xy.append(xy_sum)
        mu_x_sqr.append(mu_x_sqr_sum)
        mu_y_sqr.append(mu_y_sqr_sum)
        mu_x_mu_y.append(cov)
        col1.append('$\\Sigma$')

        # add mean to the columns 
        x_tbl.append(mu_x)
        y_tbl.append(mu_y)
        xy.append(np.mean(xy[:len(x)]))
        mu_x_sqr.append(np.mean(mu_x_sqr[:len(x)]))
        mu_y_sqr.append(np.mean(mu_y_sqr[:len(x)]))
        mu_x_mu_y.append(np.mean(mu_x_mu_y[:len(x)]))
        col1.append('$\\mu$')
        
        return xy_sum, mu_x_sqr_sum, mu_y_sqr_sum, cov, mu_cov  

    def get_ols(self, x1: pd.DataFrame | pd.Series, y1: pd.Series, display_ols:bool = False):
        """
        Create an Ordinary Lease Squares summary (OLS) and display the statsmodels OLS Summary 
        
        Parameters
        ----------            
        x1: DataFrame
            mandatory - one or more independent variables
        y1: Series
            mandatory - dependent variables
        display_ols: bool
            optional - Display the OLS Summary 

        Raises
        ======
            InvalidParamEntry

        Returns
        -------
        ols dataclass: 
            results : Iterable 
            r_squared: float
            adj_r_squared: float
            intercept: float
            dependent_var: str
            intercept_pvalue: float
            coefs: List
            stderrs: List
            tstatistics: List 
            pvalues: List
            fstatistic: float
            prob_fstatistic: float 
            log_likelihood: float
            omnibus: float
            prob_omnibus: float
            skew: float
            kurtosis: float 
            durbin_watson: float
            condition_no: float 
            model: str 
            dataframe: pd.DataFrame 
        """ 
        # if x1 is a dataframe use the columns property if series use name property 
        tmp_labels = list(x1.columns) if isinstance(x1, pd.DataFrame) else [x1.name]
        labels = ['intercept'] + tmp_labels
        pvalue_labels = [l + '_pvalue' for l in tmp_labels]
        stderr_labels = [l + '_stderr' for l in tmp_labels]
        tstatistic_labels = [l + '_tstatistic' for l in tmp_labels]

        # create the ols 
        x = api.add_constant(x1)
        # get the ordinary least squared regression  (ols)
        res = api.OLS(y1, x).fit()
        # print('\r\r')
        # print(res.summary())
        summ = res.summary()

        # get the OLS tables 
        summary_tab = res.summary2().tables[0]
        coef_tab = res.summary2().tables[1]
        test_tab = res.summary2().tables[2]
               
        values = {}
        coef_list = []
        pvalue_list = []
        stderr_list = []
        tstatistic_list = []

        values['r_squared'] = summary_tab[1][6]
        values['adj_r_squared'] = summary_tab[3][0] 

        for i in range(len(coef_tab)):
            # get coef for const, independent variables
            values[labels[i]] = coef_tab.iloc[i, 0]
            # get standard errors for const, independent variables
            values[labels[i] + '_stderr'] = coef_tab.iloc[i, 1]
            # # get p-values for const, independent variables
            values[labels[i] + '_tstatistic'] = coef_tab.iloc[i, 2]            
            # # get p-values for const, independent variables
            values[labels[i] + '_pvalue'] = coef_tab.iloc[i, 3]
            
            
        for key in values.keys():
            if key in tmp_labels:
                coef_list.append((key, values.get(key)))
            if key in pvalue_labels:
                pvalue_list.append((key,values.get(key)))    
            if key in stderr_labels:
                stderr_list.append((key,values.get(key)))
            if key in tstatistic_labels:
                tstatistic_list.append((key,values.get(key)))               
                
        ols = OLS(
            results = res 
            ,r_squared = values.get('r_squared')
            ,adj_r_squared = values.get('adj_r_squared')
            #,intercept = coef_tab["Coef."][0]
            ,intercept = coef_tab.iloc[0,0]
            ,dependent_var = summary_tab.iloc[1][1]
            #,intercept_pvalue = coef_tab["P>|t|"][0]
            ,intercept_pvalue = coef_tab.iloc[0,3]
            ,coefs = coef_list
            ,stderrs = stderr_list
            ,tstatistics = tstatistic_list
            ,pvalues = pvalue_list
            ,fstatistic = summary_tab.iloc[4][3]
            ,prob_fstatistic = summary_tab.iloc[5][3]
            ,log_likelihood = summary_tab.iloc[3][3]
            ,omnibus = test_tab.iloc[0][1]
            ,prob_omnibus = test_tab.iloc[1][1]
            ,skew = test_tab.iloc[2][1]
            ,kurtosis = test_tab.iloc[3][1]
            ,durbin_watson = test_tab[3][0]
            ,condition_no = test_tab.iloc[3][3]
            ,dataframe=x
            )
        
        msg = f'$\\displaystyle {ols.dependent_var} = {ols.intercept: .4f}~+ '
        for i in range(0, len(ols.coefs)):
            if i < (len(ols.coefs) - 1):
                msg = msg + f'{ols.coefs[i][1]: .4f} \\cdot  {ols.coefs[i][0]}~+ '
            else:
                msg = msg + f'{ols.coefs[i][1]: .4f} \\cdot  {ols.coefs[i][0]}$'
                
        ols.model = msg 

        if display_ols: 
            # make an html version of the summary table for display 
            summ_html = summ.tables[0].as_html()
            summ_header = '<h2 align="left">Regression OLS Summary</h2>'
            summ_body1 = '<table align="left"><tr><td>'
            summ_body2 = '</td></tr></table><br>'
            summ_disp = summ_header + summ_body1 + summ_html + summ_body2
            display(HTML(summ_disp))
            
            # make an html version of the coef table for display 
            coef_html = summ.tables[1].as_html()
            coef_header = '<h2 align="left">Regression OLS Coefficient</h2>'
            coef_body1 = '<table align="left"><tr><td>'
            coef_body2 = '</td></tr></table><br>'
            coef_disp = coef_header + coef_body1 + coef_html + coef_body2
            display(HTML(coef_disp))
            
            # make an html version of the coef table for display 
            test_html = summ.tables[2].as_html()
            test_header = '<h2 align="left">Regression OLS Test</h2>'
            test_body1 = '<table align="left"><tr><td>'
            test_body2 = '</td></tr></table><br><br>'
            test_disp = test_header + test_body1 + test_html + test_body2
            display(HTML(test_disp))
            
            display(Markdown(msg))
        return ols 
    
    
    def get_regressor(self, x: np.ndarray, y : list | np.ndarray, test_size : float, seed: float = 1016, intercept: bool = True):
        
        if all([isinstance(x, list | np.ndarray), isinstance(y, list | np.ndarray), isinstance(test_size, float), isinstance(seed, int), isinstance(intercept, bool)]):        
            # Reshape x from a one dimensional array to a two dimensional array which is a matrix
            # X_matrix = x.values.reshape(-1, 1)
            
            # create the test and train datasets 
            X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = test_size, random_state = seed)
            
            # train the model 
            regressor = LinearRegression(fit_intercept=intercept)
            regressor.fit(X_train, y_train)
            
            # create the regressor class with data
            res = Regressor(
                r_squared = regressor.score(X_test, y_test)
                , coefs = regressor.coef_
                , intercept = regressor.intercept_
                , regressor = regressor
            )
            return res
        else:
                err_msg = 'Invalid Parameter Entry!'
                raise InvalidParamEntry(err_msg)   
            


@dataclass
class DataSet():
    data: pd.DataFrame = None 


@dataclass
class OLS():
    results : Iterable 
    r_squared: float
    adj_r_squared: float
    intercept: float
    dependent_var: str
    intercept_pvalue: float
    coefs: List
    stderrs: List
    tstatistics: List 
    pvalues: List
    fstatistic: float
    prob_fstatistic: float 
    log_likelihood: float
    omnibus: float
    prob_omnibus: float
    skew: float
    kurtosis: float 
    durbin_watson: float
    condition_no: float 
    model: str = ''
    dataframe: pd.DataFrame = None 
    
@dataclass
class Regressor():
    r_squared: float
    coefs: List
    intercept: float 
    regressor:None
    
    
    



            
        
           
    


    
    
        
        
    
    
        
    
