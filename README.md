# E-commerce Sales Analytics

## Overview

This is a SQL-first e-commerce analytics application built for Replit deployment. The system provides business stakeholders with curated analytics endpoints to explore sales performance, customer behavior, and inventory management through prebuilt SQL queries. The application features a lightweight Flask backend with SQLAlchemy ORM, supports both SQLite and PostgreSQL databases, and includes a simple web UI for executing analytics queries and visualizing results.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask web application with SQLAlchemy ORM
- **Database Layer**: Database-agnostic design supporting both SQLite (development) and PostgreSQL (production)
- **ORM Strategy**: Uses SQLAlchemy with DeclarativeBase for model definitions and relationship management
- **Configuration**: Environment-based configuration for database URLs and session secrets
- **Proxy Support**: ProxyFix middleware for deployment behind reverse proxies

### Database Design
- **Core Entities**: Customers, Categories, Products, Orders, OrderItems, and Inventory
- **Relationships**: Proper foreign key constraints with one-to-many and many-to-one relationships
- **Data Types**: Decimal precision for financial data, proper date/datetime handling
- **Constraints**: Check constraints and business rule enforcement at the database level

### Data Management
- **CSV Data Loading**: Bulk data loader supporting dependency-ordered imports
- **Cross-Database Compatibility**: Database utility layer that abstracts SQL dialect differences
- **Query Execution**: Centralized query execution with parameter binding and error handling
- **Indexing Strategy**: Post-load index creation for optimal query performance

### API Architecture
- **RESTful Endpoints**: JSON API endpoints for analytics queries
- **Parameter Handling**: Date-based filtering and query parameterization
- **Error Handling**: Comprehensive logging and error response management
- **Health Monitoring**: Built-in health check endpoint for monitoring

### Frontend Architecture
- **Template Engine**: Jinja2 templating with Bootstrap 5 dark theme
- **JavaScript**: Vanilla JavaScript for dynamic content loading and chart rendering
- **Styling**: Custom CSS with CSS variables for theming consistency
- **Visualization**: Chart.js integration for data visualization
- **User Experience**: Tab-based navigation with loading states and error handling

### Analytics Capabilities
- **KPI Tracking**: Daily key performance indicator snapshots
- **Revenue Analysis**: Time-based revenue breakdown and trending
- **Customer Analytics**: RFM segmentation and cohort retention analysis
- **Product Performance**: Top products, margins, and inventory alerts
- **Order Funnel**: Status-based order flow analysis

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web application framework
- **SQLAlchemy**: ORM and database abstraction layer
- **Flask-SQLAlchemy**: Flask integration for SQLAlchemy

### Database Support
- **SQLite**: Default development database (file-based)
- **PostgreSQL**: Production database support via psycopg2
- **Database Drivers**: sqlite3 (built-in), psycopg2 for PostgreSQL

### Frontend Libraries
- **Bootstrap 5**: UI framework with dark theme support
- **Font Awesome**: Icon library for enhanced UI
- **Chart.js**: JavaScript charting library for data visualization

### Development and Deployment
- **Werkzeug**: WSGI utilities including ProxyFix middleware
- **Python Standard Library**: CSV processing, logging, datetime handling, and OS environment management

### Data Processing
- **CSV Module**: Built-in Python CSV processing for data imports
- **Decimal**: Precise financial calculations
- **DateTime**: Date and time manipulation for analytics queries