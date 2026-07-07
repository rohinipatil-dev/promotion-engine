import json
import os
from datetime import datetime

import pytest

# Import functions directly from your Azure Function logic
# Adjust the import path if your structure changes
from src.azure_functions.get_promotions.index import (
    load_promotions,
    filter_promotions,
    select_best_promotion,
    format_no_promotion_response,
)

PROMOTIONS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "src",
    "data",
    "promotions.json"
)

@pytest.fixture
def promotions():
    """Load promotions.json for all tests."""
    with open(PROMOTIONS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------------------------------------------------
# 1. Seasonal Promotion Test
# ---------------------------------------------------------
def test_seasonal_promotion_selected(promotions):
    filtered = filter_promotions(
        promotions,
        category="sofa",
        segment="high_value",
        season="eid",
        cart_value=850,
        location=None
    )
    best = select_best_promotion(filtered, season="eid")

    assert best is not None
    assert best["promotion_id"] == "eid_sofa_10"


# ---------------------------------------------------------
# 2. Cart Threshold Test
# ---------------------------------------------------------
def test_cart_threshold_excludes_promotion(promotions):
    filtered = filter_promotions(
        promotions,
        category="sofa",
        segment="high_value",
        season="eid",
        cart_value=200,  # too low for eid_sofa_10 (min_cart_value=500)
        location=None
    )
    best = select_best_promotion(filtered, season="eid")

    assert best is None  # No promotion should pass


# ---------------------------------------------------------
# 3. Location-Based Promotion Test
# ---------------------------------------------------------
def test_location_based_promotion(promotions):
    filtered = filter_promotions(
        promotions,
        category="sofa",
        segment="high_value",
        season="none",
        cart_value=500,
        location="dubai"
    )
    best = select_best_promotion(filtered, season="none")

    assert best is not None
    assert best["promotion_id"] == "dubai_exclusive_7"


# ---------------------------------------------------------
# 4. Generic Promotion Test (no season)
# ---------------------------------------------------------
def test_generic_promotion_selected(promotions):
    filtered = filter_promotions(
        promotions,
        category="bed",
        segment="high_value",
        season="none",
        cart_value=500,
        location=None
    )
    best = select_best_promotion(filtered, season="none")

    assert best is not None
    assert best["promotion_id"] == "clearance_bed_20"


# ---------------------------------------------------------
# 5. No Promotion Case
# ---------------------------------------------------------
def test_no_promotion_case(promotions):
    filtered = filter_promotions(
        promotions,
        category="sofa",
        segment="new_customer",
        season="eid",
        cart_value=10,
        location=None
    )
    best = select_best_promotion(filtered, season="eid")

    if best is None:
        response = format_no_promotion_response()
        assert response["promotion_id"] is None
        assert response["discount_value"] == 0
    else:
        pytest.fail("Expected no promotion but got one.")


# ---------------------------------------------------------
# 6. High Cart Value Promotion Test
# ---------------------------------------------------------
def test_high_cart_value_bonus(promotions):
    filtered = filter_promotions(
        promotions,
        category="sofa",
        segment="returning",
        season="none",
        cart_value=1200,
        location=None
    )
    best = select_best_promotion(filtered, season="none")

    assert best is not None
    assert best["promotion_id"] == "cart_bonus_50"
