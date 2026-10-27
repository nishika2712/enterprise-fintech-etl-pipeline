import pytest
from etl.transform_spark import create_spark_session, clean_and_transform

@pytest.fixture(scope="module")
def spark():
    session = create_spark_session()
    yield session
    session.stop()

def test_clean_and_transform(spark):
    # Mock input data
    data = [
        {"transaction_id": "T1", "customer_id": "C1", "amount": 100.0, "status": "COMPLETED"},
        {"transaction_id": "T2", "customer_id": "C1", "amount": -10.0, "status": "FAILED"} # Should be dropped
    ]
    df = spark.createDataFrame(data)
    result_df = clean_and_transform(df)
    
    results = result_df.collect()
    assert len(results) == 1
    assert results[0]["customer_id"] == "C1"
    assert results[0]["total_spent"] == 100.0