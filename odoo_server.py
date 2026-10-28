# odoo_server.py
import os
import xmlrpc.client
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

URL = os.environ["ODOO_URL"]        # e.g. http://localhost:8069
DB = os.environ["ODOO_DB"]
USER = os.environ["ODOO_USER"]
KEY = os.environ["ODOO_API_KEY"]    # Odoo API key (Preferences > Account Security)

common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
uid = common.authenticate(DB, USER, KEY, {})
models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")

mcp = FastMCP("odoo")


@mcp.tool()
def search_records(model: str, domain: list, fields: list, limit: int = 20) -> list:
    """Read records from any Odoo model.
    Example: model='res.partner', domain=[['customer_rank','>',0]], fields=['name','credit']
    """
    return models.execute_kw(
        DB, uid, KEY, model, "search_read",
        [domain], {"fields": fields, "limit": min(limit, 100)},
    )


@mcp.tool()
def customer_balances(limit: int = 20) -> list:
    """Customers with the highest receivable balance."""
    return models.execute_kw(
        DB, uid, KEY, "res.partner", "search_read",
        [[["customer_rank", ">", 0], ["credit", ">", 0]]],
        {"fields": ["name", "credit"], "order": "credit desc", "limit": limit},
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
    