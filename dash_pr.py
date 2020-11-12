import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from csv_read import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# 연도별 매출액 합계 그래프
year_sum_bar_chart = px.bar(
    data_frame=year_data, x='연도', y='매출액', text='매출액',
    opacity=0.8,
    orientation='v',
    barmode='relative',
    template='plotly_white'
)
year_sum_bar_chart.update_layout(
    xaxis=dict({
        'tick0': '2015',
        'dtick': 'M12'
    }),
    title=dict({
        'text': '<b>연도별 매출액</b>',
        'font_size': 20,
        'x': 0.5, 'y': 0.95
    })
)

# 연도별 결제건수 합계 그래프
year_cnt_bar_chart = px.bar(
    data_frame=year_data, x='연도', y='결제건수', text='결제건수',
    opacity=0.8,
    orientation='v',
    barmode='relative',
    template='plotly_white'
)
year_cnt_bar_chart.update_layout(
    xaxis=dict({
        'tick0': '2015',
        'dtick': 'M12'
    }),
    title=dict({
        'text': '<b>연도별 결제건수</b>',
        'font_size': 20,
        'x': 0.5, 'y': 0.95
    })
)

# 월별 매출액 합계 그래프
month_sum_data_chart = px.line(
    data_frame=month_sum_data, x='주문날짜', y='결제금액',
    line_shape='spline', orientation='v', width=1500, template='plotly_white'

)
month_sum_data_chart.update_layout(
    xaxis=dict({
        'tick0': '2015-01-01',
        'dtick': 'M12'
    }),
    title=dict({
        'text': '<b>월별 결제금액</b>',
        'font_size': 20,
        'x': 0.5, 'y': 0.95
    })
)

# 분류/성별/결제방법/주소별 판매액 추이
category_names = year_sum_cate_data['분류'].unique()
sexs = year_sum_data['성별'].unique()
payments = year_sum_data['결제방법'].unique()
geos = year_sum_data['주소'].unique()

# 요일/시간대별 히트맵
fig_heatmap = go.Figure(
    data = go.Heatmap(
        x=order_df_weekday_hour['요일'],
        y=order_df_weekday_hour['주문시간'],
        z=order_df_weekday_hour['결제건수'],
        colorscale='Reds', zauto=False, zmax=1200, zmid=1000, zsmooth='best'
    )
)
fig_heatmap.update_layout(
    title=dict({
            'text': '<b>요일/시간대별 판매(건수) 빈도</b>',
            'font_size': 20,
            'x': 0.5, 'y': 0.9
    }), height=600, template='plotly_white'
)

top10_sum_bar_chart = px.bar(
    data_frame=order_df_top10_sum, x='상품명', y='결제금액', text='결제금액',
    opacity=0.8,
    orientation='v',
    template='plotly_white'
)
top10_sum_bar_chart.update_layout(
    title=dict({
        'text': '<b>결제금액 많은 제품 TOP10</b>',
        'font_size': 20,
        'x': 0.5, 'y': 0.95
    }), height=500
)

top10_cnt_bar_chart = px.bar(
    data_frame=order_df_top10_cnt, x='주소', y='결제건수', text='결제건수',
    opacity=0.8,
    orientation='v',
    template='plotly_white'
)
top10_cnt_bar_chart.update_layout(
    title=dict({
        'text': '<b>결제건 많은 지역 TOP10</b>',
        'font_size': 20,
        'x': 0.5, 'y': 0.95
    }), height=500
)

mem_bar_chart = px.line(
    data_frame=mem_df, x='가입일', y='가입회원수',
    line_shape='spline', orientation='v', width=1500, template='plotly_white'
)
mem_bar_chart.update_layout(
    title=dict({
        'text': '<b>회원가입 추이</b>',
        'font_size': 20,
        'x': 0.5, 'y': 0.95
    }), height=500
)

app.layout = html.Div([

    html.H1(children='KSH E-Commerce Dashboard', style={'text-align': 'center', 'margin': '30 auto'}),

    dcc.Tabs([
        dcc.Tab(label='추세 분석', children=[
            
            html.H2(children='매출액/건수/회원가입 추이', style={'text-align': 'center', 'margin': '30 auto', 'font-weight': 'bold'}),
            
            dcc.Graph(
                figure=year_sum_bar_chart,
                style={'display': 'inline-block', 'width': '50%'}
            ),
            dcc.Graph(
                figure=year_cnt_bar_chart,
                style={'display': 'inline-block', 'width': '50%'}
            ),
            dcc.Graph(
                figure=month_sum_data_chart,
                style={'display': 'inline-block', 'width': '80%'}
            ),
            dcc.Graph(
                figure=mem_bar_chart,
                style={'display': 'inline-block', 'width': '80%'}
            )
        ]),
        dcc.Tab(label='판매 제품별 분석', children=[

            html.H2(children='제품 카테고리별 매출액 분석', style={'text-align': 'center', 'margin': '30 auto', 'font-weight': 'bold'}),
            html.H4(children='- 하단 DropDown 메뉴를 눌러서 카테고리를 선택하세요 - ', style={'text-align': 'center', 'margin': '30 auto'}),

            dcc.Dropdown(
                id='dropdown_1',
                options=[
                    {'label': category, 'value': category} for category in category_names
                ],
                value='스마트폰',
                style={'display': 'block', 'margin-top': 50, 'margin-bottom': 30, 'margin-left': 'auto', 'margin-right': 'auto', 'width': '50%'}
            ),
            dcc.Graph(
                id='dropdown_graph_1',
                style={'display': 'inline-block', 'width': '30%'}
            ),
            dcc.Graph(
                id='dropdown_graph_2',
                style={'display': 'inline-block', 'width': '30%'}
            ),
            dcc.Graph(
                id='dropdown_graph_3',
                style={'display': 'inline-block', 'width': '30%'}
            ),
            dcc.Graph(
                id='dropdown_graph_4',
                style={'display': 'inline-block', 'width': '100%'}
            )
        ]),
        dcc.Tab(label='상세 분석', children=[
            
            html.H2(children='제품 판매데이터 상세 분석', style={'text-align': 'center', 'margin': '30 auto', 'font-weight': 'bold'}),

            dcc.Graph(
                figure=top10_sum_bar_chart,
                style={'display': 'inline-block', 'width': '60%'}
            ),
            dcc.Graph(
                figure=top10_cnt_bar_chart,
                style={'display': 'inline-block', 'width': '40%'}
            ),
            dcc.Graph(
                figure=fig_heatmap,
                style={'display': 'inline-block', 'width': '80%'}
            ),
        ])
    ])
], style={'display': 'block', 'width': '100%', 'textAlign': 'center', 'margin': 'auto auto'})


@app.callback(
    [Output(component_id='dropdown_graph_1', component_property='figure'),
     Output(component_id='dropdown_graph_2', component_property='figure'),
     Output(component_id='dropdown_graph_3', component_property='figure'),
     Output(component_id='dropdown_graph_4', component_property='figure')],
    [Input(component_id='dropdown_1', component_property='value')]
)
def update_graph(value):
    cond = year_sum_cate_data['분류'] == value
    cond_pie = year_sum_sex_data['분류'] == value
    cond_pie_pay = year_sum_payment_data['분류'] == value
    cond_geo = year_sum_geo_data['분류'] == value
    figure_bar_1 = px.bar(
                data_frame=year_sum_cate_data[cond], x='연도', y='결제금액', text='결제금액',
                opacity=0.8,
                orientation='v',
                barmode='relative',
                template='plotly_white'
            )
    figure_bar_1.update_layout(
           xaxis=dict({
               'tick0': '2015',
               'dtick': 'M12'
           }),
           title=dict({
               'text': f'<b>{value} 연도별 매출액</b>',
               'font_size': 20,
               'x': 0.5, 'y': 0.95
           })
    )
    figure_pie_1 = px.pie(
        data_frame=year_sum_sex_data[cond_pie], names='성별', values='결제금액', color='성별',
        opacity=0.8, template='plotly_white'
    )
    figure_pie_1.update_layout(
        title=dict({
            'text': f'<b>{value} 성별 매출액 </b>',
            'font_size': 20,
            'x': 0.5, 'y': 0.95
        })
    )
    figure_pie_1.update_traces(textposition='inside', textinfo='percent+label')
    figure_pie_2 = px.pie(
        data_frame=year_sum_payment_data[cond_pie_pay], names='결제방법', values='결제금액', color='결제방법',
        opacity=0.8
    )
    figure_pie_2.update_layout(
        title=dict({
            'text': f'<b>{value} 결제방법 비율</b>',
            'font_size': 20,
            'x': 0.5, 'y': 0.95
        })
    )
    figure_pie_2.update_traces(textposition='inside', textinfo='percent+label')
    figure_geo_1 = px.scatter_mapbox(
        data_frame=year_sum_geo_data[cond_geo], lat='위도', lon='경도', size='결제금액', color='결제금액',
        opacity=0.8, mapbox_style='open-street-map', size_max=15, zoom=6,
        color_continuous_scale=px.colors.cyclical.IceFire, width=700, height=700, template='plotly_white'
    )
    figure_geo_1.update_layout(
        title=dict({
            'text': f'<b>{value} 지역별 구매액 비율</b>',
            'font_size': 20,
            'x': 0.5, 'y': 0.95
        })
    )
    return figure_bar_1, figure_pie_1, figure_pie_2, figure_geo_1


if __name__ == '__main__':
    app.run_server(debug=True, host='localhost')
