from core.plugin_manager import PluginRegistration
from core.run_context import RunContext
from core.model.service_definition import ServiceDefinition
from textwrap import dedent


class SamplePlugin:
    def register(self):
        return PluginRegistration(
            name="Backend App Generator",
            block_types=[],
            hooks={
                "on_init": self.on_init,
                "validate": self.validate,
                "transform": self.transform,
                "generate": self.generate,
                "on_finalize": self.on_finalize
            }
        )

    def on_init(self, blocks, context: RunContext):
        # we could validate if we have any entities first
        context.add_service(ServiceDefinition(
            name="backend",
            build_path="services/backend",
            dockerfile="Dockerfile",
            ports=["8000:8000"],
            depends_on=["db"]
        ))

    def validate(self, block, context: RunContext):
        ...

    def transform(self, block, context: RunContext):
        ...

    def generate(self, block, context: RunContext):
        ...

    def on_finalize(self, blocks, context: RunContext):
        self.generate_app_py(context)
        self.generate_db_py(context)
        self.generate_requirements_txt(context)
        self.generate_dockerfile(context)

    def generate_app_py(self, context: RunContext):
        content = '''\
            from fastapi import FastAPI
            from databases import Database
            from pydantic import BaseModel
        
            app = FastAPI()
        
            DATABASE_URL = "postgresql://user:password@db:5432/mydatabase"
            database = Database(DATABASE_URL)
        
            @app.on_event("startup")
            async def startup():
                await database.connect()
        
            @app.on_event("shutdown")
            async def shutdown():
                await database.disconnect()
        
            class Item(BaseModel):
                id: int
                name: str
        
            @app.get("/")
            async def root():
                return {"message": "Hello from FastAPI"}
        
            @app.get("/items/{item_id}")
            async def read_item(item_id: int):
                query = "SELECT id, name FROM items WHERE id = :item_id"
                result = await database.fetch_one(query=query, values={"item_id": item_id})
                if result:
                    return {"id": result['id'], "name": result['name']}
                return {"error": "Item not found"}
        
        '''
        # Save to services/backend/app.py
        context.write_out_file("services/backend", "app.py", dedent(content))

    def generate_db_py(self, context: RunContext):
        db_url = self.get_db_url(context)
        if not db_url:
            context.error("BackendGenerator: No database service named 'db' found")
            return

        content = f'''\
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker, declarative_base
        
            SQLALCHEMY_DATABASE_URL = "{db_url}"
        
            engine = create_engine(SQLALCHEMY_DATABASE_URL)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
            Base = declarative_base()
        '''

        context.write_out_file("services/backend", "db.py", dedent(content))

    def get_db_url(self, context: RunContext):
        db_service = context.services.get("db")
        if not db_service:
            return None

        env = getattr(db_service, "environment", {}) or {}
        user = env.get("POSTGRES_USER", "admin")
        pwd = env.get("POSTGRES_PASSWORD", "adminpass")
        db = env.get("POSTGRES_DB", "prototypo")
        host = "db"
        port = 5432
        return f"postgresql://{user}:{pwd}@{host}:{port}/{db}"

    def generate_dockerfile(self, context: RunContext):
        content = '''\
            FROM python:3.11-slim
        
            WORKDIR /app
        
            COPY requirements.txt .
        
            RUN pip install --no-cache-dir -r requirements.txt
        
            COPY app.py .
        
            CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
        '''
        context.write_out_file("services/backend", "Dockerfile", dedent(content))

    def generate_requirements_txt(self, context: RunContext):
        content = '''\
            fastapi
            uvicorn[standard]
            databases[asyncpg]
            asyncpg
        '''
        context.write_out_file("services/backend", "requirements.txt", dedent(content))

