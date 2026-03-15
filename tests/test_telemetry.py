from core.telemetry import track_metrics

def test_track_metrics_decorator():
    """
    Unit test for the telemetry decorator to ensure it captures metrics.
    """
    @track_metrics(agent_name="TestAgent")
    def mock_node(state, config):
        return {"messages": ["success"]}

    initial_state = {"metrics": {}}
    config = {}
    
    result = mock_node(initial_state, config)
    
    assert "metrics" in result
    assert "TestAgent" in result["metrics"]
    metrics = result["metrics"]["TestAgent"][0]
    
    assert "lead_time" in metrics
    assert "tokens" in metrics
    assert "cost" in metrics
    assert metrics["tokens"]["input"] == 150
