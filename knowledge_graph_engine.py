"""
This module provides the core functionality of the Knowledge Graph Engine, managing nodes and relationships in a graph database.
"""

from typing import Optional, Dict, Any
import logging
from neo4j.exceptions import Neo4jError

class KnowledgeGraphEngine:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)

    def create_node(self, label: str, properties: Dict[str, Any]) -> Optional[int]:
        """
        Creates a new node with specified label and properties.
        
        Args:
            label: The label of the node.
            properties: Dictionary of properties for the node.
            
        Returns:
            The ID of the created node or None if creation failed.
        """
        try:
            with self.driver.session() as session:
                result = session.write_transaction(
                    lambda tx: tx.create_node(label, properties)
                )
                self.logger.info(f"Created {label} node with id: {result}")
                return result
        except Neo4jError as e:
            self.logger.error(f"Failed to create node: {str(e)}")
            return None

    def create_relationship(self, start_id: int, end_id: int, type: str) -> Optional[int]:
        """
        Creates a relationship between two nodes.
        
        Args:
            start_id: ID of the starting node.
            end_id: ID of the ending node.
            type: Type of the relationship.
            
        Returns:
            The ID of the created relationship or None if creation failed.
        """
        try:
            with self.driver.session() as session:
                result = session.write_transaction(
                    lambda tx: tx.create_relationship(type, start_id, end_id)
                )
                self.logger.info(f"Created {type} relationship between nodes {start_id} and {end_id}")
                return result
        except Neo4jError as e:
            self.logger.error(f"Failed to create relationship: {str(e)}")
            return None

    def query(self, cypher: str, parameters: Optional[Dict[str, Any]] = None) -> Dict:
        """
        Executes a Cypher query on the graph database.
        
        Args:
            cypher: The Cypher query string.
            parameters: Dictionary of parameters for the query.
            
        Returns:
            A dictionary containing the result of the query.
        """
        try:
            with self.driver.session() as session:
                result = session.read_transaction(
                    lambda tx: tx.run(cypher, parameters)
                )
                return dict(result)
        except Neo4jError as e:
            self.logger.error(f"Query failed: {str(e)}")
            raise