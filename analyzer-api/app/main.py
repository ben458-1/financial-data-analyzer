import uvicorn
from fastapi import FastAPI, Request
from app.lifespans.app_lifespan import app_lifespan
from api import articles, article_meta_api, application
from fastapi.middleware.cors import CORSMiddleware

from app.rate_limiter import RateLimiterService

app = FastAPI(lifespan=app_lifespan)

# 👇 Add CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🚨 Replace * with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Init limiter
rate_limiter = RateLimiterService()
rate_limiter.init_app(app)


@app.middleware("http")
async def add_rate_limit_headers(request: Request, call_next):
    response = await call_next(request)

    if hasattr(request.state, "view_rate_limit"):
        limit_info = request.state.view_rate_limit
        if limit_info is not None and isinstance(limit_info, tuple):
            request_limit, window_stats = limit_info

            # If window_stats is a list, it likely means we got the wrong value.
            # Let's ignore the list and assume it's either not necessary or malformed.
            if isinstance(window_stats, list):
                window_stats = {}  # Reset to empty dictionary

            # Ensure window_stats is a dictionary (as expected)
            if not isinstance(window_stats, dict):
                window_stats = {}

            # Set the rate limit headers
            response.headers["X-RateLimit-Limit"] = str(request_limit)
            response.headers["X-RateLimit-Remaining"] = str(window_stats.get("remaining", 0))
            response.headers["X-RateLimit-Reset"] = str(int(window_stats.get("reset", 0)))

    return response


# Include your API routes
app.include_router(articles.router)
app.include_router(article_meta_api.article_meta)
app.include_router(application.app)

if __name__ == '__main__':
    uvicorn.run(app=app, host="127.0.0.1", port=8001)
