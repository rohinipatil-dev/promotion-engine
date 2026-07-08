import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import azure.functions as func

PROMOTIONS_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "promotions.json")
)

def load_promotions() -> List[Dict[str, Any]]:
    try:
        with open(PROMOTIONS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            logging.error("promotions.json is not a list")
            return []
        return data
    except Exception as e:
        logging.error(f"Failed to load promotions.json: {e}")
        return []


def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str)
    except Exception:
        logging.warning(f"Invalid date format: {date_str}")
        return None


def is_promotion_active(promo: Dict[str, Any]) -> bool:
    if not promo.get("active", False):
        return False

    valid_until = parse_date(promo.get("valid_until"))
    if valid_until and valid_until < datetime.utcnow():
        return False

    return True


def matches_category(promo: Dict[str, Any], category: str) -> bool:
    return promo.get("category") == category


def matches_segment(promo: Dict[str, Any], segment: str) -> bool:
    return promo.get("customer_segment") == segment


def matches_season(promo: Dict[str, Any], season: str) -> bool:
    promo_season = promo.get("season")
    if not promo_season:
        # Generic promotion, allowed
        return True
    return promo_season == season


def matches_cart_value(promo: Dict[str, Any], cart_value: float) -> bool:
    min_cart = promo.get("min_cart_value")
    if min_cart is None:
        return True
    try:
        return float(cart_value) >= float(min_cart)
    except Exception:
        return False


def matches_location(promo: Dict[str, Any], location: Optional[str]) -> bool:
    promo_location = promo.get("location")
    if not promo_location:
        return True
    if not location:
        return False
    return promo_location.lower() == location.lower()


def filter_promotions(
    promotions: List[Dict[str, Any]],
    category: str,
    segment: str,
    season: str,
    cart_value: float,
    location: Optional[str],
) -> List[Dict[str, Any]]:
    filtered = []
    for promo in promotions:
        if not is_promotion_active(promo):
            continue
        if not matches_category(promo, category):
            continue
        if not matches_segment(promo, segment):
            continue
        if not matches_season(promo, season):
            continue
        if not matches_cart_value(promo, cart_value):
            continue
        if not matches_location(promo, location):
            continue
        filtered.append(promo)
    return filtered


def score_promotion(
    promo: Dict[str, Any],
    season: str,
) -> int:
    """
    Higher score = better promotion.
    Priority:
    1. Seasonal promotions
    2. Segment-specific
    3. Cart-based
    4. Generic category
    """
    score = 0

    # Seasonal priority
    promo_season = promo.get("season")
    if promo_season and promo_season == season:
        score += 30
    elif promo_season:
        # Different season, but still seasonal
        score += 10

    # Segment-specific
    if promo.get("customer_segment"):
        score += 20

    # Cart-based
    if promo.get("min_cart_value") is not None:
        score += 10

    # Generic category promotions get base score
    if not promo_season:
        score += 5

    # Discount value contributes
    try:
        discount_value = float(promo.get("discount_value", 0))
        score += int(discount_value)
    except Exception:
        pass

    return score


def select_best_promotion(
    promotions: List[Dict[str, Any]],
    season: str,
) -> Optional[Dict[str, Any]]:
    if not promotions:
        return None

    scored = []
    for promo in promotions:
        score = score_promotion(promo, season)
        scored.append((score, promo))

    # Sort by:
    # 1. score (desc)
    # 2. discount_value (desc)
    # 3. valid_until (asc)
    # 4. original order
    def sort_key(item):
        score, promo = item
        try:
            discount_value = float(promo.get("discount_value", 0))
        except Exception:
            discount_value = 0.0
        valid_until = parse_date(promo.get("valid_until")) or datetime.max
        return (-score, -discount_value, valid_until)

    scored.sort(key=sort_key)
    return scored[0][1]


def format_success_response(promo: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "promotion_id": promo.get("promotion_id"),
        "title": promo.get("title"),
        "description": promo.get("description"),
        "discount_type": promo.get("discount_type"),
        "discount_value": promo.get("discount_value"),
        "valid_until": promo.get("valid_until"),
        "terms": promo.get("terms", ""),
        "language": "en",
    }


def format_no_promotion_response() -> Dict[str, Any]:
    return {
        "promotion_id": None,
        "title": "No active promotions",
        "description": "There are no promotions available for this product.",
        "discount_type": "none",
        "discount_value": 0,
        "valid_until": None,
        "terms": "",
        "language": "en",
    }


def format_error_response(message: str) -> Dict[str, Any]:
    return {
        "error": message,
    }


def validate_input(body: Dict[str, Any]) -> Optional[str]:
    required_fields = ["category", "customer_segment", "cart_value", "season", "language"]
    for field in required_fields:
        if field not in body:
            return f"Missing required field: {field}"

    # Basic type checks
    if not isinstance(body.get("category"), str):
        return "Invalid category"
    if not isinstance(body.get("customer_segment"), str):
        return "Invalid customer_segment"
    if not isinstance(body.get("season"), str):
        return "Invalid season"
    if not isinstance(body.get("language"), str):
        return "Invalid language"

    try:
        float(body.get("cart_value"))
    except Exception:
        return "Invalid cart_value"

    return None


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Promotion Engine: get_promotions called")

    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps(format_error_response("Invalid JSON payload")),
            status_code=400,
            mimetype="application/json",
        )

    error = validate_input(body)
    if error:
        return func.HttpResponse(
            json.dumps(format_error_response(error)),
            status_code=400,
            mimetype="application/json",
        )

    category = body["category"]
    segment = body["customer_segment"]
    cart_value = float(body["cart_value"])
    season = body["season"]
    location = body.get("location")

    promotions = load_promotions()
    if not promotions:
        return func.HttpResponse(
            json.dumps(format_error_response("Promotion data unavailable")),
            status_code=500,
            mimetype="application/json",
        )

    filtered = filter_promotions(
        promotions=promotions,
        category=category,
        segment=segment,
        season=season,
        cart_value=cart_value,
        location=location,
    )

    best = select_best_promotion(filtered, season)

    if not best:
        response = format_no_promotion_response()
    else:
        response = format_success_response(best)

    return func.HttpResponse(
        json.dumps(response),
        status_code=200,
        mimetype="application/json",
    )
