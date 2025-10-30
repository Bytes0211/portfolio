"""
plot.py
generates hypothesis test plots based on information passed from test.py 
"""

class InvalidParamEntry(Exception):
    """Raised when invalid parameter is passed"""
    pass

class InvalidTypeError(Exception):
    """Raised when invalid type passed as a parameter"""
    pass

class InvalidBokehConfiguration(Exception):
    """Raised when Bokeh objects are not configured correctly"""
    pass


class Plot: 
    def __init__(self, data : dict = {}) -> None:
        self.data = data 
        
        
    def create_plot(self):
        import numpy as np 
        import sys 
        sys.path.insert(0, '..')
        from  resources import glyph , datum
        datum = datum.Data()
        
        if self.data['type'] == 'mean':
            plot = glyph.Glyph(f'{self.data["tail"].capitalize()} Tail Test\nNull Hypothesis {self.data["null_hypo"]}\n')
            
            if self.data["mu"] > 0:
                mean = self.data["mu"]
            else:        
                mean = self.data['xbar1']
            
            if self.data["sigma1"] > 0:
                std_dev = self.data["sigma1"]
            else:
                std_dev = self.data['s1']
            
            # population distribution 
            plot.make_line(x = self.data['x_data'], y = self.data['y_data'], width = 2, color = 'gainsboro')

            # mean
            plot.make_vert_line(
                x = self.data['x_data']
                , data_point = mean
                , y_min = np.min(self.data["y_data"])
                , mu = mean
                , sigma = std_dev 
                , label = f'mean: {mean}'
                )
                              

            if self.data["tail"] == 'two':
                # lower region of rejection data
                x_lwr_reg_rej = self.data["lower_reg_rej"]
                y_lwr_reg_rej = datum.get_normal_dist(x_arr = x_lwr_reg_rej, mu = mean, sigma = std_dev)
                floor_lwr_reg_rej = np.full(len(y_lwr_reg_rej), np.min(y_lwr_reg_rej))
                
                # upper region of rejection data
                x_upr_reg_rej = self.data["upper_reg_rej"]
                y_upr_reg_rej = datum.get_normal_dist(x_arr = x_upr_reg_rej, mu = mean, sigma = std_dev)
                floor_upr_reg_rej = np.full(len(y_upr_reg_rej), np.min(y_upr_reg_rej))
                
                # test statistic vertical line
                plot.make_vert_line(
                    x = self.data['x_data']
                    , data_point = self.data['x_data'][self.data['ts_index']]
                    , y_min = np.min(self.data["y_data"])
                    , mu = mean
                    , sigma = std_dev
                    , label = f'test statistic {self.data["x_data"][self.data["ts_index"]]: .4f}'
                    , color = 'darkorange'
                    , width = 3
                    )
                
              
                # lower region of rejection  
                plot.make_varea(
                    x = x_lwr_reg_rej
                    , floor = floor_lwr_reg_rej
                    , y = y_lwr_reg_rej
                    , legend_label = "lower region of rejection"
                )
                
                # upper region of rejection  
                plot.make_varea(
                    x = x_upr_reg_rej
                    , floor = floor_upr_reg_rej
                    , y = y_upr_reg_rej
                    , legend_label = "upper region of rejection"
                )
            elif self.data["tail"] == 'lower':
                # lower region of rejection data
                x_lwr_reg_rej = self.data["lower_reg_rej"]
                y_lwr_reg_rej = datum.get_normal_dist(x_arr = x_lwr_reg_rej, mu = mean, sigma = std_dev)
                floor_lwr_reg_rej = np.full(len(y_lwr_reg_rej), np.min(y_lwr_reg_rej))
                
                # test statistic vertical line
                plot.make_vert_line(
                    x = self.data['x_data']
                    , data_point = self.data['x_data'][self.data['ts_index']]
                    , y_min = np.min(self.data["y_data"])
                    , mu = mean
                    , sigma = std_dev
                    , label = f'test statistic {self.data["x_data"][self.data["ts_index"]]: .4f}'
                    , color = 'darkorange'
                    , width = 4
                    )
                
                # lower region of rejection  
                plot.make_varea(
                    x = x_lwr_reg_rej
                    , floor = floor_lwr_reg_rej
                    , y = y_lwr_reg_rej
                    , legend_label = "lower region of rejection"
                )
            else:               
                # upper region of rejection data
                x_upr_reg_rej = self.data["upper_reg_rej"]
                y_upr_reg_rej = datum.get_normal_dist(x_arr = x_upr_reg_rej, mu = mean, sigma = std_dev)
                floor_upr_reg_rej = np.full(len(y_upr_reg_rej), np.min(y_upr_reg_rej)) # the floor for y is not always 0
                
                # test statistic vertical line
                plot.make_vert_line(
                    x = self.data['x_data']
                    , data_point = self.data['x_data'][self.data['ts_index']]
                    , y_min = np.min(self.data["y_data"])
                    , mu = mean
                    , sigma = std_dev
                    , label = f'test statistic {self.data["x_data"][self.data["ts_index"]]: .4f}'
                    , color = 'darkorange'
                    , width = 3
                    )
                
                # upper region of rejection  
                plot.make_varea(
                    x = x_upr_reg_rej
                    , floor = floor_upr_reg_rej
                    , y = y_upr_reg_rej
                    , legend_label = "upper region of rejection"
                ) 

            plot.show()
                
        if self.data['type'] == 'prop':
            plot = glyph.Glyph(f'{self.data["tail"].capitalize()} Tail Test\nNull Hypothesis {self.data["null_hypo"]}\n')
            
            mean =  self.data["mu"]
            std_dev = self.data['s1']
            
            # population distribution 
            plot.make_line(x = self.data['x_data'], y = self.data['y_data'], width = 2, color = 'gainsboro')

            # mean
            plot.make_vert_line(
                x = self.data['x_data']
                , data_point = mean
                , y_min = np.min(self.data["y_data"])
                , mu = mean
                , sigma = std_dev 
                , label = f'mean: {mean}'
                )
                              

            if self.data["tail"] == 'two':
                # lower region of rejection data
                x_lwr_reg_rej = self.data["lower_reg_rej"]
                y_lwr_reg_rej = datum.get_normal_dist(x_arr = x_lwr_reg_rej, mu = mean, sigma = std_dev)
                floor_lwr_reg_rej = np.full(len(y_lwr_reg_rej), np.min(y_lwr_reg_rej))
                
                # upper region of rejection data
                x_upr_reg_rej = self.data["upper_reg_rej"]
                y_upr_reg_rej = datum.get_normal_dist(x_arr = x_upr_reg_rej, mu = mean, sigma = std_dev)
                floor_upr_reg_rej = np.full(len(y_upr_reg_rej), np.min(y_upr_reg_rej))
                
                # test statistic vertical line
                plot.make_vert_line(
                    x = self.data['x_data']
                    , data_point = self.data['x_data'][self.data['ts_index']]
                    , y_min = np.min(self.data["y_data"])
                    , mu = mean
                    , sigma = std_dev
                    , label = f'test statistic {self.data["x_data"][self.data["ts_index"]]: .4f}'
                    , color = 'darkorange'
                    , width = 3
                    )
                
                # lower region of rejection  
                plot.make_varea(
                    x = x_lwr_reg_rej
                    , floor = floor_lwr_reg_rej
                    , y = y_lwr_reg_rej
                    , legend_label = "lower region of rejection"
                )
                
                # upper region of rejection  
                plot.make_varea(
                    x = x_upr_reg_rej
                    , floor = floor_upr_reg_rej
                    , y = y_upr_reg_rej
                    , legend_label = "upper region of rejection"
                )
            elif self.data["tail"] == 'lower':
                # lower region of rejection data
                x_lwr_reg_rej = self.data["lower_reg_rej"]
                y_lwr_reg_rej = datum.get_normal_dist(x_arr = x_lwr_reg_rej, mu = mean, sigma = std_dev)
                floor_lwr_reg_rej = np.full(len(y_lwr_reg_rej), np.min(y_lwr_reg_rej))
                
                # test statistic vertical line
                plot.make_vert_line(
                    x = self.data['x_data']
                    , data_point = self.data['x_data'][self.data['ts_index']]
                    , y_min = np.min(self.data["y_data"])
                    , mu = mean
                    , sigma = std_dev
                    , label = f'test statistic {self.data["x_data"][self.data["ts_index"]]: .4f}'
                    , color = 'darkorange'
                    , width = 3
                    )
                
                # lower region of rejection  
                plot.make_varea(
                    x = x_lwr_reg_rej
                    , floor = floor_lwr_reg_rej
                    , y = y_lwr_reg_rej
                    , legend_label = "lower region of rejection"
                )
            else:               
                # upper region of rejection data
                x_upr_reg_rej = self.data["upper_reg_rej"]
                y_upr_reg_rej = datum.get_normal_dist(x_arr = x_upr_reg_rej, mu = mean, sigma = std_dev)
                floor_upr_reg_rej = np.full(len(y_upr_reg_rej), np.min(y_upr_reg_rej)) # the floor for y is not always 0
                
                # test statistic vertical line
                plot.make_vert_line(
                    x = self.data['x_data']
                    , data_point = self.data['x_data'][self.data['ts_index']]
                    , y_min = np.min(self.data["y_data"])
                    , mu = mean
                    , sigma = std_dev
                    , label = f'test statistic {self.data["x_data"][self.data["ts_index"]]: .4f}'
                    , color = 'darkorange'
                    , width = 5
                    )
                
                
                # upper region of rejection  
                plot.make_varea(
                    x = x_upr_reg_rej
                    , floor = floor_upr_reg_rej
                    , y = y_upr_reg_rej
                    , legend_label = "upper region of rejection"
                ) 

            plot.show()