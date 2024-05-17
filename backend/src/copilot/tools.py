db_info_string = "hello"

tools = [
    {
        "type": "function",
        "function": {
            "name": "ask_db",
            "description": "Use this function to provide factual answers to user questions. Input should be a fully formed PostgreSQL query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": f"""
                            PostgreSQL query extracting info to answer the user's question.
                            PostgreSQL should be written using this database schema:
                            {db_info_string}
                            The query should be return in plain text, not in JSON.
                            """
                    }
                }
            },
            "required": ["query"]
        }
    }
]