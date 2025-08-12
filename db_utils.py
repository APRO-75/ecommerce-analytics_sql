import os
import sqlite3
import psycopg2
from app import db
import logging

logger = logging.getLogger(__name__)

def get_db_dialect():
    """Determine if we're using SQLite or PostgreSQL"""
    database_url = os.environ.get("DATABASE_URL", "sqlite:///analytics.db")
    return "postgresql" if database_url.startswith("postgresql") else "sqlite"

def get_date_trunc_function(period, column):
    """Return the appropriate date truncation function based on database dialect"""
    dialect = get_db_dialect()
    
    if dialect == "postgresql":
        return f"date_trunc('{period}', {column})"
    else:  # SQLite
        if period == "month":
            return f"strftime('%Y-%m-01', {column})"
        elif period == "day":
            return f"strftime('%Y-%m-%d', {column})"
        else:
            return column

def get_extract_function(part, column):
    """Return the appropriate date extraction function"""
    dialect = get_db_dialect()
    
    if dialect == "postgresql":
        return f"EXTRACT({part} FROM {column})"
    else:  # SQLite
        if part.lower() == "month":
            return f"strftime('%m', {column})"
        elif part.lower() == "year":
            return f"strftime('%Y', {column})"
        elif part.lower() == "day":
            return f"strftime('%d', {column})"
        else:
            return column

def execute_query(query, params=None):
    """Execute a query and return results"""
    try:
        if params is None:
            params = {}
        
        result = db.session.execute(db.text(query), params)
        
        # Get column names
        columns = result.keys()
        
        # Fetch all rows and convert to list of dictionaries
        rows = result.fetchall()
        data = []
        for row in rows:
            row_dict = {}
            for i, col in enumerate(columns):
                row_dict[col] = row[i]
            data.append(row_dict)
        
        logger.info(f"Query executed successfully, returned {len(data)} rows")
        return data
        
    except Exception as e:
        logger.error(f"Query execution failed: {str(e)}")
        raise

def load_sql_query(filename):
    """Load SQL query from file and replace dialect-specific functions"""
    query_path = os.path.join("queries", filename)
    
    try:
        with open(query_path, 'r') as f:
            query = f.read()
        
        # Replace date functions based on dialect
        dialect = get_db_dialect()
        
        if dialect == "sqlite":
            # Replace PostgreSQL date functions with SQLite equivalents
            query = query.replace("date_trunc('month',", "strftime('%Y-%m-01',")
            query = query.replace("date_trunc('day',", "strftime('%Y-%m-%d',")
            query = query.replace("EXTRACT(epoch FROM", "strftime('%s',")
            query = query.replace("INTERVAL '1 month'", "'+1 month'")
            
        return query
        
    except FileNotFoundError:
        logger.error(f"SQL file not found: {query_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading SQL file {query_path}: {str(e)}")
        raise
