import pandas as pd
import plotly.express as px
from morph_lib.types import HtmlResponse

import morph
from morph import MorphGlobalContext

@morph.func
@morph.load_data("get_user_data")
def user_transition(context: MorphGlobalContext):
    df = context.data['get_user_data']

    # タイムスタンプを日付に変換
    df['created_at'] = pd.to_datetime(pd.to_numeric(df['created_at']), unit='s')

    # 年月を日本語形式で表記（例: 2024年9月）
    df['month'] = df['created_at'].dt.to_period('M')
    df['month_label'] = df['month'].dt.strftime('%Y年%-m月')

    # 集計
    user_count_by_month = df.groupby(['month', 'month_label']).size().reset_index(name='user_count')

    # 月順に並べるためカテゴリを設定
    user_count_by_month['month_label'] = pd.Categorical(
        user_count_by_month['month_label'],
        categories=[m.strftime('%Y年%-m月') for m in sorted(df['month'].unique())],
        ordered=True
    )

    # グラフ作成（日本語ラベルに変更）
    fig = px.line(
        user_count_by_month,
        x='month_label',
        y='user_count',
        title='月ごとの新規ユーザー数の推移',
        labels={'month_label': '月', 'user_count': '新規ユーザー数'}
    )

    return HtmlResponse(fig.to_html(full_html=False, include_plotlyjs='cdn'))
