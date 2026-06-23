import time
import logging

logger = logging.getLogger("api_retries")
logger.setLevel(logging.WARNING)

# Primary and fallback models
PRIMARY_MODEL = "gemini-2.5-flash"
FALLBACK_MODEL = "gemini-1.5-flash"

def generate_content_with_retry(client, contents, config, max_retries=3):
    """
    Executes a Gemini API call with retries, exponential backoff, and model fallback.
    """
    delays = [2, 4, 8]
    models_to_try = [PRIMARY_MODEL, FALLBACK_MODEL]
    
    last_exception = None
    
    for model in models_to_try:
        try_count = 0
        while try_count <= max_retries:
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=config
                )
                return response
            except Exception as e:
                last_exception = e
                # Log the failure
                logger.warning(f"API generation failed for model {model} on attempt {try_count + 1}. Error: {str(e)}")
                
                if try_count < max_retries:
                    # Exponential backoff
                    delay = delays[try_count] if try_count < len(delays) else 8
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                
                try_count += 1
                
    # If all retries and fallback models fail, raise a specific error that agents can catch
    raise RuntimeError(f"All API attempts failed. Last error: {str(last_exception)}")
