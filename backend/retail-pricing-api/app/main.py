from fastapi import FastAPI, Depends, APIRouter
from starlette.middleware.cors import CORSMiddleware
from controllers.masterController import master_router
from utils.db_utils import generate_models_from_db

app = FastAPI(
    title="RETAIL PRICING API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
    expose_headers=["Content-Disposition"]
)

# Adding common route for all API's.
main_router = APIRouter(prefix=f"/api")

# including all routes to the common route.
main_router.include_router(master_router)

# Finally adding the main route to the app.
app.include_router(main_router)