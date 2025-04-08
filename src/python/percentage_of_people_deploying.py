import pandas as pd
from morph_lib.types import HtmlResponse
import morph
from morph import MorphGlobalContext

@morph.func
@morph.load_data("get_user_data")
@morph.load_data("get_database_users")
@morph.load_data("get_deploy_data")
def percentage_of_people_deploying(context: MorphGlobalContext):
    # データ取得
    users_df = context.data['get_user_data']
    db_users_df = context.data['get_database_users']
    deploy_df = context.data['get_deploy_data']

    # Step 1: deploy_data.database_id ⇔ db_users.database_id
    db_users_trimmed = db_users_df[['user_id', 'database_id']]
    deploy_trimmed = deploy_df[['database_id']]
    merged_df = pd.merge(deploy_trimmed, db_users_trimmed, on='database_id', how='inner')

    # Step 2: user_id ⇔ users.id
    final_df = pd.merge(merged_df, users_df, left_on='user_id', right_on='id', how='inner')

    # ✅ デプロイ済ユーザー数（重複除く）
    deployed_user_count = final_df['id'].nunique()

    # ✅ 全サインアップユーザー数
    total_users = users_df['id'].nunique()

    # ✅ 割合を計算
    percentage = (deployed_user_count / total_users * 100) if total_users > 0 else 0

    # ✅ 結果をHTMLで返す
    html = f"""
    <h3>デプロイの割合</h3>
    <ul>
        <li><strong>サインアップした人数:</strong> {total_users}</li>
        <li><strong>デプロイをしている人数:</strong> {deployed_user_count}</li>
        <li><strong>サインアップした人の中でデプロイをしている人の割合:</strong> {percentage:.2f}%</li>
    </ul>
    """
    return HtmlResponse(html)
