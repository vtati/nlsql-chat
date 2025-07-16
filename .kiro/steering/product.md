# Product Overview

## Natural Language to SQL Chat Interface

A chat-based application that converts natural language queries into SQL statements and executes them against relational databases. The product enables non-technical users to query databases using plain English, eliminating the need for SQL knowledge.

## Target Users
- Business analysts
- Data analysts  
- Product managers
- Non-technical stakeholders needing database insights

## Core Value Proposition
Transform natural language questions like "Show me all customers from Germany" into executable SQL queries with results displayed in an intuitive chat interface.

## Key Features
- Natural language to SQL conversion using OpenAI GPT models
- Real-time chat interface with conversation history
- Tabular result display with export capabilities
- Automatic database schema detection
- Read-only query execution for security
- Support for complex queries including JOINs and aggregations

## Sample Database
Includes a pre-configured SQLite database with customers, products, and orders tables for immediate testing and demonstration.

## Security Focus
- Only SELECT queries allowed
- SQL injection prevention
- Input sanitization and validation
- Read-only database access