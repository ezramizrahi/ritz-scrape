from services.scraper.utils import find_best_match
import pytest

def test_basic_similarity():
    title = "Air Bud"
    candidates = ["Aero Buddy", "Air Bud 2", "Airplane Pup"]
    assert find_best_match(title, candidates) == "Air Bud 2"

def test_case_sensitivity():
    title = "air bud"
    candidates = ["Aero Buddy", "Air Bud 2", "Airplane Pup"]
    assert find_best_match(title, candidates).lower() == "air bud 2"

def test_empty_candidates():
    title = "Air Bud"
    candidates = []
    with pytest.raises(IndexError):
        find_best_match(title, candidates)

def test_single_candidate():
    title = "Air Bud"
    candidates = ["Air Bud 2"]
    assert find_best_match(title, candidates) == "Air Bud 2"

def test_identical_titles():
    title = "Air Bud"
    candidates = ["Air Bud", "Aero Buddy", "Air Bud 2"]
    assert find_best_match(title, candidates) == "Air Bud"