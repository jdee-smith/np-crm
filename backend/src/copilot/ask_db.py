from sqlalchemy import sql
from sqlalchemy.orm import Session


def get_table_names(session: Session):
    query = sql.text(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE';
        """
    )
    result = session.execute(query).fetchall()
    table_names = []
    for i in result:
        table_names.append(i[0])
    return table_names

def get_view_names(session: Session):
    query = sql.text(
        """
        SELECT table_name
        FROM INFORMATION_SCHEMA.views
        WHERE table_schema = ANY (CURRENT_SCHEMAS(false));
        """
    )
    result = session.execute(query).fetchall()
    view_names = []
    for i in result:
        view_names.append(i[0])
    return view_names

def get_column_names(session: Session, table: str):
    query = sql.text(
        f"""
        SELECT column_name
        FROM INFORMATION_SCHEMA.columns
        WHERE table_name = '{table}';
        """
    )
    result = session.execute(query).fetchall()
    column_names = []
    for i in result:
        column_names.append(i[0])
    return column_names

def get_db_info(session: Session):
    mapping = []
    tables_and_views = get_table_names(session)
    tables_and_views.extend(get_view_names(session))
    for i in tables_and_views:
        columns = get_column_names(session, i)
        mapping.append({"table": i, "columns": columns})
    return mapping

def generate_db_info_string(session: Session):
    mapping = get_db_info(session)
    return "\n".join([f"Table: {i['table']}\nColumns: {', '.join(i['columns'])}" for i in mapping])

def ask_db(session: Session, query: str):
    raise NotImplementedError