import time
from functools import wraps
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def track_metrics(agent_name: str):
    """
    Decorator to track lead time, token consumption, and estimated cost 
    for each agent invocation.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(state, config, *args, **kwargs):
            start_time = time.time()
            
            # Simulated token tracking (in real usage, extract from Langchain RunTree/Callbacks)
            # e.g., using get_openai_callback() or similar based on provider
            tokens_used = {"input": 150, "output": 50} 
            
            # Simulated cost calculation
            cost = (tokens_used["input"] * 0.000005) + (tokens_used["output"] * 0.000015)
            
            # Execute the node function
            result = func(state, config, *args, **kwargs)
            
            lead_time = time.time() - start_time
            
            # Aggregate metrics in the state
            metrics = state.get("metrics", {}) if state.get("metrics") is not None else {}
            if agent_name not in metrics:
                metrics[agent_name] = []
                
            metrics[agent_name].append({
                "lead_time": round(lead_time, 4),
                "tokens": tokens_used,
                "cost": round(cost, 6)
            })
            
            logger.info(f"[{agent_name}] Execution time: {lead_time:.2f}s | Cost: ${cost:.6f}")
            
            # Some results might just return updates, so merge
            if "metrics" not in result:
                result["metrics"] = metrics
            
            return result
        return wrapper
    return decorator
