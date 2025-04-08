import pandas as pd
from morph_lib.types import HtmlResponse
import morph
from morph import MorphGlobalContext

@morph.func
@morph.load_data("get_user_data")
@morph.load_data("get_database_users")
@morph.load_data("get_deploy_data")
def test(context: MorphGlobalContext):
    # データ取得
    users_df = context.data['get_user_data']
    db_users_df = context.data['get_database_users']
    deploy_df = context.data['get_deploy_data']

    # Step 1: デプロイされた database_id を database_users と JOIN
    db_users_trimmed = db_users_df[['user_id', 'database_id']]
    deploy_trimmed = deploy_df[['database_id']]
    merged_df = pd.merge(deploy_trimmed, db_users_trimmed, on='database_id', how='inner')

    # Step 2: user_id ⇔ users_df.id で JOIN
    final_df = pd.merge(merged_df, users_df, left_on='user_id', right_on='id', how='inner')

    # 結果のテーブルをHTMLにして返す
    html_table = final_df.to_html(index=False)
    return HtmlResponse(f"<h3>Deployed Users</h3>{html_table}")
