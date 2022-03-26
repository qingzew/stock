#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 wang <wang@wang-pc>
#
# Distributed under terms of the MIT license.

"""

"""
import os
import pandas as pd
from pyecharts.charts import Kline, Line, Bar, Grid, EffectScatter
from pyecharts import options as opts
from pyecharts.globals import SymbolType
import numpy as np


def split_data(data):
    category_data = []
    values = []
    volumes = []

    for i, tick in enumerate(data):
        category_data.append(tick[0])
        values.append(tick)
        volumes.append([i, tick[4], 1 if tick[1] > tick[2] else -1])
    return {"categoryData": category_data, "values": values, "volumes": volumes}


def calculate_ma(day_count: int, data):
    result: List[Union[float, str]] = []
    #for i in range(len(data["values"])):
    for i in range(len(data)):
        if i < day_count:
            result.append("-")
            continue
        sum_total = 0.0
        for j in range(day_count):
            sum_total += float(data[i - j][1])
        result.append(abs(float("%.3f" % (sum_total / day_count))))
    return result

#def draw_charts(xaxis, stock_price, volume, output_html, indicator=None, special_line=None):
def draw_charts(xaxis, stock_price, volume, output_html, indicator=None, slines=None):
    # Kline
    kline = Kline()
    kline.add_xaxis(xaxis_data=xaxis)
    kline.add_yaxis(
            series_name="",
            y_axis=stock_price,
            itemstyle_opts=opts.ItemStyleOpts(color="#ec0000", color0="#00da3c"),)
    
    kline.set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False, pos_bottom=10, pos_left="center"),
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False,
                    type_="inside",
                    xaxis_index=[0, 1],
                    range_start=50,
                    range_end=100),
                opts.DataZoomOpts(
                    is_show=True,
                    xaxis_index=[0, 1],
                    type_="slider",
                    pos_top="85%",
                    range_start=50,
                    range_end=100)],
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)),),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="cross",
                background_color="rgba(245, 245, 245, 0.8)",
                border_width=1,
                border_color="#ccc",
                textstyle_opts=opts.TextStyleOpts(color="#000")),
            visualmap_opts=opts.VisualMapOpts(
                is_show=False,
                dimension=2,
                series_index=6,
                is_piecewise=True,
                pieces=[
                    {"value": 1, "color": "#00da3c"},
                    {"value": -1, "color": "#ec0000"}]),
            axispointer_opts=opts.AxisPointerOpts(
                is_show=True,
                link=[{"xAxisIndex": "all"}],
                label=opts.LabelOpts(background_color="#777")),
            brush_opts=opts.BrushOpts(
                x_axis_index="all",
                brush_link="all",
                out_of_brush={"colorAlpha": 0.1},
                brush_type="lineX"))

    # Line
    line = Line()
    line.add_xaxis(xaxis_data=xaxis)
    line.add_yaxis(
            series_name="MA5",
            y_axis=calculate_ma(day_count=5, data=stock_price),
            is_smooth=True,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False))
    line.add_yaxis(
            series_name="MA10",
            y_axis=calculate_ma(day_count=10, data=stock_price),
            is_smooth=True,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False))
    line.add_yaxis(
            series_name="MA20",
            y_axis=calculate_ma(day_count=20, data=stock_price),
            is_smooth=True,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False))
    line.add_yaxis(
            series_name="MA30",
            y_axis=calculate_ma(day_count=30, data=stock_price),
            is_smooth=True,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False))
    line.add_yaxis(
            series_name="MA60",
            y_axis=calculate_ma(day_count=60, data=stock_price),
            is_smooth=True,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False))

    line.set_global_opts(xaxis_opts=opts.AxisOpts(type_="category"))

    kline = kline.overlap(line)

    #if special_line is not None:

    for sline in slines:
        x = list(sline.keys())
        y = list(sline.values())
        sline = Line()
        sline.add_xaxis(xaxis_data=x)

        sline.add_yaxis(
                series_name="special_line",
                y_axis=y,
                is_smooth=True,
                is_hover_animation=False,
                linestyle_opts=opts.LineStyleOpts(width=5, opacity=2, color='black'),
                label_opts=opts.LabelOpts(is_show=False))
        kline = kline.overlap(sline)
        
    # EffectScatter
    if indicator is not None:
        es_buy = EffectScatter()
        es_buy.add_xaxis(indicator['buy'][0])
        #es_buy.add_yaxis("", indicator['buy'][1], symbol='image://b.jpg',
        #        effect_opts=opts.EffectOpts(symbol='arrow', scale=5, period=-1, brush_type='fill', color='black'))
        #es_buy.add_yaxis("", inds['buy'][1], symbol='triangle')

        es_buy.add_yaxis("", indicator['buy'][1], symbol='arrow',
                effect_opts=opts.EffectOpts(scale=5, period=5, brush_type='fill', color='blue'))

        es_sell = EffectScatter()
        es_sell.add_xaxis(indicator['sell'][0])
        es_sell.add_yaxis("", indicator['sell'][2], symbol='pin',
                effect_opts=opts.EffectOpts(scale=5, period=5,  brush_type='fill', color='blue'))


        #es.set_global_opts(title_opts=opts.TitleOpts(title="EffectScatter-不同Symbol"))
    
        kline = kline.overlap(es_buy).overlap(es_sell)

    # bar
    bar = Bar()
    bar.add_xaxis(xaxis_data=xaxis)
    bar.add_yaxis(
            series_name="Volume",
            y_axis=volume,
            xaxis_index=1,
            yaxis_index=1,
            label_opts=opts.LabelOpts(is_show=False))
    bar.set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="category",
                is_scale=True,
                grid_index=1,
                boundary_gap=False,
                axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
                axislabel_opts=opts.LabelOpts(is_show=False),
                split_number=20,
                min_="dataMin",
                max_="dataMax"),
            yaxis_opts=opts.AxisOpts(
                grid_index=1,
                is_scale=True,
                split_number=2,
                axislabel_opts=opts.LabelOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(is_show=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
            ),
            legend_opts=opts.LegendOpts(is_show=False))
   
    # Grid Overlap + Bar
    grid_chart = Grid(
        init_opts=opts.InitOpts(
            width="1000px",
            height="800px",
            animation_opts=opts.AnimationOpts(animation=False),
        )
    )
    
    
    grid_chart.add(
        kline,
        grid_opts=opts.GridOpts(pos_left="10%", pos_right="8%", height="50%"),
    )
   
    grid_chart.add(
        bar,
        grid_opts=opts.GridOpts(
            pos_left="10%", pos_right="8%", pos_top="63%", height="16%"
        ),
    )
    #grid_chart.render_notebook()
    grid_chart.render(output_html)



if __name__ == '__main__':
    df = pd.read_csv('tsla.csv')
    print(df)

    #date = df['date'].tolist()
    #open = df['open'].tolist()
    #close = df['close'].tolist()
    #low = df['low'].tolist()
    #high = df['high'].tolist()
    #volume = df['volume'].tolist()

    #new_data = []
    #for d, o, c, l, h, v in zip(date, open, close, low, high, volume):
    #    new_data.append([d, o, c, l, h, v])

    #data = split_data(new_data)
    #print(data['values'])

    df_np = df.to_numpy()[-100:]
    xaxis = []
    stock_price = []
    volume = []
    for row in df_np:
        d, o, h, l, c, v = row[0], row[1], row[2], row[3], row[4], row[5]
        xaxis.append(d)
        stock_price.append([o, c, l, h])
        volume.append(v)
        

    print(volume)
    special_line = list(range(900, 1000))
    indicator = {}
    indicator['buy'] = [['2021-10-25'], [944], [1045]]
    indicator['sell'] = [['2021-11-05'], [1217], [1243]]
    draw_charts(xaxis, stock_price, volume, 'vis.html', special_line=special_line, indicator=indicator)
