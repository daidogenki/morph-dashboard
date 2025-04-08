{{
    config(
        connection="MORPH_APPLICATION_PROD"
    )
}}

select "created_at", "updated_at", "status", "database_id","id" from "user_function_deployment"