import logging
from datetime import datetime, timedelta
from flask import request, render_template, jsonify, redirect, url_for, flash
from db_utils import execute_query, load_sql_query
from data_loader import DataLoader
import traceback

logger = logging.getLogger(__name__)

def register_routes(app):
    
    @app.route("/")
    def index():
        """Main dashboard page"""
        return render_template("index.html")
    
    @app.route("/health")
    def health():
        """Health check endpoint"""
        return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
    
    @app.route("/load-data", methods=["POST"])
    def load_data():
        """Load data from CSV files"""
        try:
            loader = DataLoader()
            loader.load_all_data()
            flash("Data loaded successfully!", "success")
        except Exception as e:
            logger.error(f"Data loading failed: {str(e)}")
            flash(f"Data loading failed: {str(e)}", "error")
        
        return redirect(url_for("index"))
    
    @app.route("/analytics/kpi")
    def kpi():
        """Daily KPI snapshot"""
        try:
            date_param = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
            
            query = load_sql_query("kpi.sql")
            result = execute_query(query, {"target_date": date_param})
            
            if result:
                return jsonify(result[0])
            else:
                return jsonify({"error": "No data found for the specified date"}), 404
                
        except Exception as e:
            logger.error(f"KPI query failed: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route("/analytics/revenue-by-month-category")
    def revenue_by_month_category():
        """Revenue by month and category"""
        try:
            start_date = request.args.get("start", "2024-01")
            end_date = request.args.get("end", "2024-12")
            
            # Convert to full dates
            start_date_full = f"{start_date}-01"
            end_date_full = f"{end_date}-31"
            
            query = load_sql_query("revenue_by_month_category.sql")
            result = execute_query(query, {
                "start_date": start_date_full,
                "end_date": end_date_full
            })
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Revenue by month-category query failed: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route("/analytics/repeat-rate")
    def repeat_rate():
        """Repeat purchase rate analysis"""
        try:
            start_date = request.args.get("start", "2024-01")
            end_date = request.args.get("end", "2024-12")
            
            start_date_full = f"{start_date}-01"
            end_date_full = f"{end_date}-31"
            
            query = load_sql_query("repeat_rate.sql")
            result = execute_query(query, {
                "start_date": start_date_full,
                "end_date": end_date_full
            })
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Repeat rate query failed: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route("/analytics/cohort-retention")
    def cohort_retention():
        """Cohort retention analysis"""
        try:
            start_date = request.args.get("start", "2024-01")
            end_date = request.args.get("end", "2024-12")
            horizon = int(request.args.get("horizon", 12))
            
            start_date_full = f"{start_date}-01"
            end_date_full = f"{end_date}-31"
            
            query = load_sql_query("cohort_retention.sql")
            result = execute_query(query, {
                "start_date": start_date_full,
                "end_date": end_date_full,
                "horizon": horizon
            })
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Cohort retention query failed: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route("/analytics/rfm")
    def rfm():
        """RFM customer scoring"""
        try:
            as_of_date = request.args.get("as_of", datetime.now().strftime("%Y-%m-%d"))
            
            query = load_sql_query("rfm.sql")
            result = execute_query(query, {"as_of_date": as_of_date})
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"RFM query failed: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route("/analytics/top-products")
    def top_products():
        """Top products by margin"""
        try:
            metric = request.args.get("metric", "margin")
            n = min(int(request.args.get("n", 10)), 100)  # Clamp to 100
            start_date = request.args.get("start", "2024-01-01")
            end_date = request.args.get("end", "2024-12-31")
            
            query = load_sql_query("top_products.sql")
            result = execute_query(query, {
                "start_date": start_date,
                "end_date": end_date,
                "limit_n": n
            })
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Top products query failed: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route("/analytics/low-stock")
    def low_stock():
        """Low stock alerts"""
        try:
            n = min(int(request.args.get("n", 20)), 100)  # Clamp to 100
            
            query = load_sql_query("low_stock.sql")
            result = execute_query(query, {"limit_n": n})
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Low stock query failed: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route("/analytics/order-funnel")
    def order_funnel():
        """Order funnel status analysis"""
        try:
            start_date = request.args.get("start", "2024-01-01")
            end_date = request.args.get("end", "2024-12-31")
            
            query = load_sql_query("order_funnel.sql")
            result = execute_query(query, {
                "start_date": start_date,
                "end_date": end_date
            })
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Order funnel query failed: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500
