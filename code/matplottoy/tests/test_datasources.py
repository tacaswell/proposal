import pytest 
import numpy as np 

import matplotlib.pyplot as plt
from matplotlib.testing.decorators import check_figures_equal

import matplottoy.artists.artists as ap
import matplottoy.datasources.array as da

def axes_property_check(ax_test, ax_ref):

    assert ax_test.get_xlim() == ax_ref.get_xlim()
    assert ax_test.get_ylim() == ax_ref.get_ylim()
    assert ax_test.get_aspect() == ax_ref.get_aspect()

    assert (ax_test.get_position().bounds == 
            ax_ref.get_position().bounds)
    assert (ax_test.get_window_extent().bounds ==
            ax_ref.get_window_extent().bounds)

class TestArray: 
    @pytest.fixture(autouse=True)
    def data(self):
        array =  np.tile(np.arange(13),10).reshape(10,13)
        self.datasource = da.DataSourceArray(array)
        self.rows, self.cols = self.datasource.data.shape

    @check_figures_equal(extensions=['png'])
    def test_image(self, fig_test, fig_ref):
        ax_test = fig_test.subplots()
        ar_test = ap.Image(ax_test, self.datasource, origin="lower")
        ax_test.add_artist(ar_test)
        ax_test.set_aspect(1.0)
        fig_test.colorbar(ar_test, ax=ax_test)
        fig_test.canvas.draw()

        ax_ref = fig_ref.subplots()
        ar_ref = ax_ref.imshow(self.datasource.data, origin="lower")
        fig_ref.colorbar(ar_ref, ax=ax_ref)
        fig_ref.canvas.draw()

        axes_property_check(ax_test, ax_ref)
        assert ar_test.zorder == ar_ref.zorder
        assert (ar_test.get_window_extent().bounds ==
                ar_ref.get_window_extent().bounds)



    @check_figures_equal(extensions=['png'])
    def test_line(self, fig_test, fig_ref):

        ax_test= fig_test.subplots()
        artist_test = ap.Line(self.datasource)
        ax_test.add_artist(artist_test)
        ax_test.set(xlim=(0, self.rows-1), 
                    ylim=(0, self.cols-1))
        fig_ref.canvas.draw()

        ax_ref = fig_ref.subplots()
        _ = ax_ref.plot(self.datasource.data, color='C0')
        ax_ref.set(xlim=(0, self.rows-1), 
                   ylim=(0, self.cols-1))
        fig_test.canvas.draw()
        axes_property_check(ax_test, ax_ref)
    
    @check_figures_equal(extensions=['png'])
    def test_bar_grouped(self, fig_test, fig_ref):
        ax_test = fig_test.subplots()
        artist_test = ap.Bar(self.datasource)
        ax_test.add_artist(artist_test)
        ax_test.set(xlim=(0, self.rows-1), 
                    ylim=(0, self.cols-1))

        ax_ref = fig_ref.subplots()
        for i, row in enumerate(self.datasource.data.T):
            x = np.arange(row.shape[0]) + (i/self.rows)
            width = 1/self.rows
            _ = ax_ref.bar(x, row, width)
        ax_ref.set(xlim=(0, self.rows-1), 
                   ylim=(0, self.cols-1))

        axes_property_check(ax_test, ax_ref)
    
        
    
    
    @pytest.mark.skip()
    @check_figures_equal(extensions='png')
    def test_bar_stacked(self, fig_test, fig_ref):
        pass
    
    