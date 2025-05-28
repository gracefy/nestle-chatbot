from typing import List, Optional, Dict
from common.neo4j_client import get_neo4j_driver


def get_products_by_brand(brand_name: str) -> List[Dict]:
    driver = get_neo4j_driver()
    query = """
        MATCH (b:Brand {name: $brand_name})-[:HAS_PRODUCT]->(p:Product)
        RETURN p.name AS name, p.description AS description, p.label AS label,
               p.product_size AS product_size, p.url AS url
    """
    with driver.session() as session:
        results = session.run(query, brand_name=brand_name)
        return [record.data() for record in results]


def get_product_by_name(name: str) -> Optional[Dict]:
    driver = get_neo4j_driver()
    query = """
        MATCH (p:Product {name: $name})
        RETURN p.name AS name, p.description AS description, p.label AS label,
               p.product_size AS product_size, p.url AS url
    """
    with driver.session() as session:
        result = session.run(query, name=name)
        record = result.single()
        return record.data() if record else None
