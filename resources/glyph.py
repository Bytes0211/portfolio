
''' 
glyph.py
Cover methods for bokeh functionality
'''


from bokeh.plotting import figure, output_notebook, curdoc, ColumnDataSource, show
from bokeh.models import Label, LabelSet, Slope, Range1d
from bokeh.transform import factor_cmap
from typing import Iterable, List, Dict, Tuple

class InvalidParamEntry(Exception):
    """Raised when invalid parameter is passed"""
    
class InvalidTypeError(Exception):
    """Raised when invalid type passed as a parameter"""
    
class InvalidBokehConfiguration(Exception):
    """Raised when Bokeh objects are not configured correctly"""
    
class InvalidShapeError(Exception):
    """Raised when invalid shaped passed to make_points"""
    

class Glyph: 

    
    def __init__(self, title : str = "New Title", width : int = 650, height : int = 450, x_axis_label :str = '' , 
                 show_ticks : bool = True , y_axis_label : str = '', theme : str = 'dark_minimal', x_range: Tuple = (0, 0),
                 y_range: Tuple = (0, 0), bck_gnd_color = '#20262B', bck_gnd_alpha = 1.0, legend_location : str = 'top_right'):
        
        self.title = title
        self.width = width
        self.height = height 
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        self.theme = theme 
        self.show_ticks = show_ticks
        self.color = 0
        self.legend_location = legend_location
        self.x_range = x_range
        self.y_range = y_range
        self.bck_gnd_color = bck_gnd_color
        self.bck_gnd_alpha = bck_gnd_alpha 
        self.plot = self.make_plot() 
        self.plots = 0
        self.dataSource = None
        self.data = False

        
             
        
    # def get_color(self):
    #     color = -1
    #     def inner_func():
    #         nonlocal color
    #         num += 1
    #         return self.palettes[num]
    #     return inner_func
    
    # color = get_color()
        
        
    def make_plot(self): 
        """
        create a bokeh figure based on title, width, height, theme 
        passed as arguments or default values at object creation 
        
        Parameters 
        ----------
        None

        Returns
        -------
        None
        """
        

        output_notebook(hide_banner=True)
        
        curdoc().theme = self.theme 
        
        p = figure(
            title = self.title
            , width = self.width
            , x_axis_label = self.x_axis_label
            , y_axis_label = self.y_axis_label
            ,height = self.height
            ,background_fill_color = self.bck_gnd_color
            ,background_fill_alpha = self.bck_gnd_alpha
        )

        if self.x_range[1] > 0:
            p.x_range = Range1d(self.x_range[0], self.x_range[1])
         

        if self.y_range[1] > 0:
            p.y_range = Range1d(self.y_range[0], self.y_range[1])
         
        if not self.show_ticks:
            p.xaxis.major_tick_line_color = None
            p.yaxis.major_tick_line_color = None
            p.xaxis.major_label_text_font_size = '0pt'
            p.yaxis.major_label_text_font_size = '0pt'
        return p
    
        
    
    def make_dataSource(self, src:Dict):
        """
        create a bokeh ColumnDataSource 
                
        Parameters 
        ----------
        src : dictionary 
            mandatory - a dictionary that contains x, y, labels keys and associated arrays as values 

        Returns
        -------
        None
        """
        try: 
            if self.dataSource is None:
                self.dataSource = ColumnDataSource(src)
                self.data = True
        except:
            err_msg = 'Error occured creating ColumnDataSource in make_dataSource()'
            raise InvalidBokehConfiguration(err_msg)
    
    
    
    def get_blue_palette(self):
        """
        get bokeh blue8 as a tuple with darkest color at index 0 and almost white - light blue at index 7
                
        Parameters 
        ----------
        None

        Returns
        -------
        list of blue colors from bokeh 
        """
        print('GET BLUE PALLETTE')
        from bokeh.palettes import Blues8
        blues = Blues8  
        return blues[20] 
        
        
    def make_line(self, x : [], y : [],  width : int = 1, label : str = "",  color : str = "dodgerblue", alpha : float = .90):
        """
        create a bokeh figure.line based on x and y values
        the line width (default = 1) and line color (default None) can be set with parameters
        
        Parameters 
        ----------
        x : list
            mandatory - a list that consisted of the x-axis values
        y : list
            mandatory - a list that consisted of the y-axis values
        width : int 
            a value that represent line width
        label : str 
            'the string value that denotes the line
        Returns
        -------
        None
        """
        
        source = ColumnDataSource(
            dict(x = x, y = y)
        )        
        if len(label) > 0:   
            self.plot.line(
                x = 'x'
                ,y = 'y'
                ,line_width = width 
                ,color = color
                ,alpha = alpha
                ,legend_label = label 
                ,source = source 
            )
            self.plot.legend.location = self.legend_location  
        else: 
            self.plot.line(
                x = 'x'
                ,y = 'y'
                ,line_width = width 
                ,color = color
                ,alpha = alpha 
                ,source = source 
            )
        self.plots += 1 
                   
                   
    def make_vert_line(self
                       , data_point : int | float
                       , y_min : int | float = 0
                       , y_max : int | float = None
                       , width : int = 1
                       , label : str = ""
                       , color : str = 'firebrick'
                       , alpha : float = 0.75
                       , x : list = None
                       , mu : int | float = None
                       , sigma : int | float = None
                    ):
        """
        create a bokeh figure.line which will be vertical based on x, mu, sigma 
         
        Parameters 
        ----------
        data_point : int | float
            mandatory - a data point along the x axis of the distribution which determines the location of the vertical line
        y_min  : int | float
            mandatory - the minimum point of the the vertical line 
        y_max : int | float 
            optional - the maximum point of the the vertical line. If not provided, will be calculated from mu and sigma
        width : int 
            mandatory - a value that represent line width
        label : str 
            mandatory - 'the string value that denotes the line
        x : list
            optional - x-axis data array (used with mu and sigma to calculate y_max)
        mu : int | float
            optional - mean of distribution (used with sigma to calculate y_max)
        sigma : int | float
            optional - standard deviation (used with mu to calculate y_max)

        Returns
        -------
        None
        """  
        if self.plots > 0:
            import sys
            sys.path.insert(0, '..')
            import resources.datum as data
            new_data = data.Data()
            if y_max is not None:
                y_point = y_max
            elif mu is not None and sigma is not None:
                # Calculate y_max from normal distribution at data_point
                y_point = new_data.get_normal_dist(x_arr=data_point, mu=mu, sigma=sigma)
            else:
                raise InvalidParamEntry('Either y_max or (mu and sigma) must be provided')
            x_line = [data_point, data_point]
            y = [y_min, y_point]
            if len(label) > 0:          
                self.plot.line(
                    x = x_line
                    ,y = y
                    ,line_width = width 
                    ,color = color
                    ,alpha = alpha 
                    ,legend_label = label 
                )
                self.plot.legend.location = self.legend_location  
            else: 
                self.plot.line(
                    x = x_line
                    ,y = y
                    ,line_width = width 
                    ,color = color
                    , alpha = alpha
                )
            self.plots += 1
            
        else:
            raise InvalidBokehConfiguration
            
            
    def make_varea(self 
                   , x 
                   , y
                   , floor
                   , fill_color : str = 'dodgerblue' 
                   , fill_alpha : float = 0.75
                   , legend_label : str = ''
                   ):
        """
        create a bokeh figure.area which is vertically directed based on x, y1, and y2 values 
         
        Parameters 
        ----------
        x : list | List, mandatory - The x-coordinates for the points of the area.
        floor: list | List, mandatory - The zero value y-coordinates for the bottom side of the area
        y: list | List, mandatory - The value y-coordinates for the side side of the area
        data_point : int | float, mandatory - a data point along the x axis of the distribution 
        fill_color : str, optional, - color of the area, default - dodger blue
        fill_alpha : float, optional - alpha value for the file_color, default 0.75
        legend_label : str - 'the string value that denotes the line

        Returns
        -------
        None
        """  
        source = ColumnDataSource(
            dict(x = x, floor = floor, y = y)
        )
        if len(legend_label) > 0:
            self.plot.varea(
                x = 'x'
                , y1 = 'floor' 
                , y2 = 'y'
                , fill_color = fill_color
                , fill_alpha = fill_alpha
                , legend_label = legend_label 
                ,source = source 
            )
            self.plot.legend.location = self.legend_location  
        else:
            self.plot.varea(
                x = 'x'
                , y1 = 'floor' 
                , y2 = 'y'
                , fill_color = fill_color
                , fill_alpha = fill_alpha
                , source = source 
            )
        self.plots += 1
            

    def make_square(self
                    , x:  List
                    , y: List
                    , color: str = 'goldenrod'
                    , width: int = 1
                    , alpha: float = 0.75 
                    , label: str = ''
                    ):
        """
        Create four bokeh lines that represent a least square of a regression line 
         
        Parameters 
        ----------
        x : list | List
            mandatory - The value x-coordinates for the side side of the area
        y: list | List
            mandatory - The value y-coordinates for the side side of the area
        data_point : int | float
            mandatory - a data point along the x axis of the distribution 
        fill_color : str
            optional, - color of the area, default - dodger blue
        fill_alpha : float
            optional - alpha value for the file_color, default 0.75
        label : 
            str - 'the string value that denotes the line

        Returns
        -------
        None
        """  
        self.make_line(x = x, y = [y[0], y[0]], width=width, color = color, alpha = alpha)
        self.make_line(x = x, y = [y[1], y[1]], width=width, color = color, alpha = alpha)
        self.make_vert_line(data_point=x[0], y_min = y[0], y_max= y[1], color = color, width = width)
        self.make_vert_line(data_point=x[1], y_min = y[0], y_max= y[1], color = color, width = width)
    
    
    def add_label(self
            ,text : str 
            ,text_color = 'gainsboro'
            ,x_loc : int= 250 
            ,y_loc : int = 75    
            ,line_color : str = None
            ,line_alpha : float = 0.90
            ,fill_color : str = None
            ,fill_alpha : float = 0.50
        ):
        """
        Create a Annotation Label 
         
        Parameters 
        ----------
        text : str 
            mandatory - The displayed text
        , text color: str:
            optional - default = gainsboro
        , x_loc: int
            optional - default 250
        , y_loc: int
            optional - default 75
        , line_color: str
            optional - default = gainsboro
        , line_alpha: float
            optional - default = 0.90
        , fill_color: str
            optional - default = None
        , fill_alpha: float
            optional - default = 0.50

        Returns
        -------
        None
        """  
        label = Label(x=x_loc, y=y_loc, x_units='screen', y_units='screen', text= text,
                        text_color= text_color, border_line_color = line_color, border_line_alpha=line_alpha,
                        background_fill_color=fill_color, background_fill_alpha=fill_alpha)
        self.plot.add_layout(label)


    
    def add_label_set(self, x : List, y: List,  labels: List, x_offset: int = 5, y_offset: int = 5):
        """
        Create a Annotation LabelSet
         
        Parameters 
        ----------
        x : List 
            mandatory - list of x values for labelset
        y : List 
            mandatory - list of  values for labelset 
        labels : List 
            mandatory - list of string labels for x, y datapoints 
        x_offset : int
            mandatory - x coordinate offset from the x, y data point
        y_offset : int
            mandatory - y coordinate offset from the x, y data point
        Returns
        -------
        None
        """  

        if self.plots > 0:
                data = dict(x = x, y = y, labels = labels)
                source = ColumnDataSource(data)
                new_labels = LabelSet(x = "x", y = "y", text = "labels", x_offset= x_offset, y_offset=y_offset, source = source)
                self.plot.add_layout(new_labels)
        else:
            err_msg = "add_label_set() requires at least one plot"
            raise InvalidBokehConfiguration(err_msg)


        
    
    def make_points(self
                    , shape : str
                    , dataset : Dict
                    , size : int = 5
                    , fill_color : str = 'firebrick'
                    , line_color : str = 'firebrick'
                    , alpha : float = 0.90
                    , label : str = ''
                    , col : str = None
                    , cmap : List = None 
          ):
        """
        create a bokeh figure.shape array (circle, square, diamond, triangle, star)
         
        Parameters 
        ----------
        shape : str mandatory - circle, square, diamond, triangle, or star
        dataset : dict,  mandatory - dictionary containing the x, y, z values 
        size  : int - optional the size of the shape, default 5
        fill_color : str, optional, - fill color of the shape
        line_cole : str, optional, - line color of the shape
        fill_alpha : float, optional - alpha value for the file_color, default 0.90
        legend_label : str - 'the string value that denotes the shape, de

        Returns
        -------
        None
        """  

        if isinstance(shape, str):
            if len(shape) < 1:
                raise InvalidParamEntry(Exception)
            if all([isinstance(size, int), isinstance(fill_color, str), isinstance(alpha, float), isinstance(line_color, str)]):
                self.plots += 1
                if all([isinstance(col, str), isinstance(cmap, List), (dataset.get('c') is not None)]):
                    inner_color = factor_cmap(col, palette = cmap, factors=sorted(dataset.get('c')))
                    outer_color = factor_cmap(col, palette = cmap, factors=sorted(dataset.get('c')))
                    src = ColumnDataSource(dict(x = list(dataset.get('x')), y = list(dataset.get('y')), c = list(dataset.get('c'))))
                else:
                    inner_color = fill_color
                    outer_color = line_color
                    src = ColumnDataSource(dict(x = list(dataset.get('x')), y = list(dataset.get('y'))))
                match shape:
                    case 'circle':
                        self.plot.circle(x = 'x', y = 'y', size = size, fill_color = inner_color, fill_alpha = alpha, legend_label = label, line_color = outer_color, source = src)
                        self.plot.legend.location = self.legend_location
                    case 'square':
                        self.plot.square(x = 'x', y = 'y', size = size, fill_color = inner_color, fill_alpha = alpha, legend_label = label, line_color = outer_color, source = src)
                        self.plot.legend.location = self.legend_location
                    case 'diamond':
                        self.plot.diamond(x = 'x', y = 'y', size = size, fill_color = inner_color, fill_alpha = alpha, legend_label = label, line_color = outer_color, source = src)
                        self.plot.legend.location = self.legend_location
                    case 'triangle':
                        self.plot.triangle(x = 'x', y = 'y', size = size, fill_color = inner_color, fill_alpha = alpha, legend_label = label, line_color = outer_color, source = src)
                        self.plot.legend.location = self.legend_location
                    case 'star':
                        self.plot.star(x = 'x', y = 'y', size = size, fill_color = inner_color, fill_alpha = alpha, legend_label = label, line_color = outer_color, source = src)
                        self.plot.legend.location = self.legend_location 
                    case _:
                        raise InvalidShapeError(shape)   
                if len(label) > 1:
                    label = shape
                    self.plot.legend.location = self.legend_location  
            else:
                raise InvalidParamEntry(Exception)
        else:
            raise InvalidParamEntry(Exception)

     
    def add_regression_line(
        self, slope: int | float
        , y_intercept: int | float
        , line_width: int = 2
        , line_color: str = "crimson"
        , line_dash: str = "solid"
        , line_alpha: float = 0.70
        ):
        """
        Create a line slope based on slope and y-intercept
         
        Parameters 
        ----------
        slope : int | float
            mandatory - list of x values for labelset
        y-intercept : int | float 
            mandatory - list of  values for labelset 
        line_width : int 
            optional - default = 2, width of line
        line_color : str
            optional - default = crimson, line color
        line_dash : str
            optional - default = solid, dashed, dotted, dotdash, dashdot
        line_dash : 
            optional - default = solid, dashed, dotted, dotdash, dashdot
        line_alpha : float
            optional - default = 0.70

        Returns
        -------
        None
        """  
        slope = Slope(
            gradient = slope
            , y_intercept = y_intercept
            , line_width = line_width
            , line_color = line_color
            , line_dash = line_dash
            , line_alpha = line_alpha
            )
        self.plot.add_layout(slope)
         
        
        
    def make_histogram(self 
                   , x 
                   , start : int = 0
                   , stop : int = 0
                   , bins : int = 0
                   , mu : int | float = 0
                   , sigma : int | float = 0
                   , fill_alpha : float = 0.90 
                   , fill_color : str = 'dodgerblue'
                   , line_color : str = 'white'
                   , pdf : bool = False
                   , legend_label = ''
                   ):
        
        """
        create a bokeh histogram based on a list, bin parameters (start, stop, bin size)
         
        Parameters 
        ----------
        x : list | ndarray, mandatory - The population of the histogram
        start: int , mandatory - The minimal value of population
        stop: int , mandatory - The minimal value of population
        bins: int, mandatory - Number of bins - 1 (if 10, then 9 bins will be created)
        fill_alpha : float, optional - alpha value for the file_color, default 0.90
        fill_color : str, optional, - color of the area, default - dodger blue
        pdf : bool - if true draw a probability density function line based on histogram value
        Returns
        -------
        Histogram
        """  
        if all([isinstance(start, int | float), isinstance(stop, int | float), isinstance(bins, int), 
                isinstance(mu, int | float), isinstance(sigma, int | float),  isinstance(pdf, bool)]):
            self.plots += 1
            if all([start > -0.99, stop >  0, bins > 0]):
                if len(legend_label) < 2:
                    legend_label = 'histogram' 
                import numpy as np
                import sys
                sys.path.insert(0, '..')
                import resources.datum as datum 
                data = datum.Data()
                
                bin_cnt = np.linspace(start, stop, bins)
                hist, edges = np.histogram(x, density=True, bins = bin_cnt)
                self.plot.quad(top = hist
                    ,bottom=0 
                    ,left = edges[:-1] 
                    ,right= edges[1:]
                    ,fill_color = fill_color  
                    ,alpha = fill_alpha
                    ,line_color = line_color
                    ,legend_label = legend_label
                )
                if pdf:
                    if len(x) < 200:
                        n = len(x) * 2
                    else:
                        n = len(x)  # noqa: F841
                    
                    xx = np.linspace(np.min(x), np.max(x), len(x))
                    y = data.get_normal_dist(x = xx, mu = mu, sigma = sigma)
                    self.make_line(x = xx, y = y)
            else:
                err_msg = f'start ({start}), stop ({stop}), bins ({bins}) must have values greater than 0'
                raise InvalidParamEntry(err_msg)        
        else:        
            err_msg = 'either start, stop, or bins is an invalid type'
            raise InvalidTypeError(err_msg)                            
              
              
    def show(self):
        show(self.plot)
        
        
    def show_column():
        from bokeh.layouts import column
        


