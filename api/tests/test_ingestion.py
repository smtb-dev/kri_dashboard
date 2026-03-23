def test_upload_rejects_missing_columns(client) -> None:
    # Missing SubCategory and CurrentValue
    csv_content = "EntryDate,Category\n1/1/2025,Security Event Continuous Monitoring\n"
    response = client.post(
        "/api/uploads",
        files={"file": ("bad.csv", csv_content, "text/csv")},
    )
    assert response.status_code == 400
    assert "Missing required columns" in response.text
