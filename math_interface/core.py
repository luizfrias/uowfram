#!/usr/bin/python
# -*- coding: utf-8 -*-

import platform
# MacOS work around. See: http://stackoverflow.com/questions/21784641/installation-issue-with-matplotlib-python
if platform.system() == 'Darwin':
    import matplotlib
    matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import cStringIO


class MathPlotMissingParameter(Exception):
    pass


class UndefinedFunctionType(Exception):
    pass


class MathPlot(object):

    def __init__(self, plot_params, fn_params):
        self.parse_plot_params(plot_params)
        self.parse_fn_params(fn_params)

    def parse_plot_params(self, params):
        '''
        Receives a dict and set object state
        '''
        # First we should parse required parameters

        try:
            _x = params['xrange']
            self.xrange_min, self.xrange_max, self.range_npoints = _x
        except KeyError:
            raise MathPlotMissingParameter('a required parameter is missing')

        # Set default parameters
        self.xmin, self.xmax, self.ymin, self.ymax = None, None, None, None
        self.show_grid = False
        self.xlabel, self.ylabel, self.title = '', '', ''

        if 'xlimits' in params:
            self.xmin, self.xmax = params['xlimits']
        if 'ylimits' in params:
            self.ymin, self.ymax = params['ylimits']

        self.xlabel = params.get('xlabel', self.xlabel)
        self.ylabel = params.get('ylabel', self.ylabel)
        self.title = params.get('title', self.title)
        self.show_grid = params.get('show_grid', self.show_grid)

    def parse_fn_params(self, params):
        self.functions = []
        for function in params:
            ftype = function['type']
            if ftype == 'cos':
                self.functions.append(CosPlot(function))
            elif ftype == 'sin':
                self.functions.append(SinPlot(function))
            elif ftype == 'poly':
                self.functions.append(PolyPlot(function))
            else:
                raise UndefinedFunctionType(
                    "It's not possible to plot type '%s'" % ftype)

    def get_time_range(self):
        return np.linspace(self.xrange_min,
                           self.xrange_max,
                           self.range_npoints)

    def as_base64(self):
        image_file = cStringIO.StringIO()
        plt.savefig(image_file)
        plt.clf()
        encoded_string = image_file.getvalue().encode("base64")
        return encoded_string

    def plot_functions(self, time_range):
        for fnobj in self.functions:
            plt.plot(time_range,
                     fnobj.get_fn(time_range),
                     label=fnobj.label)

    def set_parameters(self):
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.title(self.title)
        plt.grid(self.show_grid)
        if self.ymin or self.ymax:
            plt.ylim([self.ymin, self.ymax])
        if self.xmin or self.xmax:
            plt.xlim([self.xmin, self.xmax])
        plt.legend()

    def render(self):
        time_range = self.get_time_range()
        self.plot_functions(time_range)
        self.set_parameters()
        return self.as_base64()


class BasePlot(object):

    def __init__(self, params):
        self.label = params.get('label', params['type'])


class HarmonycPlot(BasePlot):

    def __init__(self, params):
        super(HarmonycPlot, self).__init__(params)
        self.amplitude = params.get('amplitude', 1)


class CosPlot(HarmonycPlot):

    def get_fn(self, time_range):
        return self.amplitude*np.cos(time_range)


class SinPlot(HarmonycPlot):

    def get_fn(self, time_range):
        return self.amplitude*np.sin(time_range)


class PolyPlot(BasePlot):

    def __init__(self, params):
        super(PolyPlot, self).__init__(params)
        try:
            self.coefs = params['coef']
        except KeyError:
            raise MathPlotMissingParameter(
                'Missing polynomial coefficients')

    def get_fn(self, time_range):
        fn = 0
        for index, coef in enumerate(self.coefs):
            fn += coef*(time_range**index)
        return fn

if __name__ == '__main__':
        post = {
            'plot': {
                'xrange': [0, 10, 100],
                # 'xlimits': [0, 0],
                # 'ylimits': [0, 0],
                # 'xlabel': '',
                # 'ylabel': '',
                # 'title': '',
                # 'show_grid': True,
            },
            'fn': [
                {
                    'type': 'cos',
                    'amplitude': 2,
                    'label': 'cos',
                },
                {
                    'type': 'sin',
                    'amplitude': 5,
                    'label': 'sin',
                },
                {
                    'type': 'poly',
                    'coef': [1, 1],
                    'label': 'poly',
                }
            ]
        }
        plot_params = post['plot']
        fn_params = post['fn']
        m = MathPlot(plot_params, fn_params)
        m.render()
        plt.show()
