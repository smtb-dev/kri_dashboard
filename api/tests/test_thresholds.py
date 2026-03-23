from app.services.thresholds import compute_percentiles


def test_compute_percentiles_defaults() -> None:
    amber, red = compute_percentiles([0, 1, 2, 3, 4, 5, 10, 20, 25, 30])
    assert amber >= 5
    assert red >= amber
