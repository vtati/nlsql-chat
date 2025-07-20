# Project Structure

## Root Directory Layout
```
├── api/                     # Backend API (FastAPI)
├── web/                     # Frontend Web Application (React)
├── docs/                    # Project documentation
├── scripts/                 # Project-level scripts
├── .kiro/                   # Kiro IDE configuration
├── README.md               # Main project documentation
└── deployment configs      # Various deployment configurations
```

## API Structure (`api/`)
```
api/
├── src/                    # Source code
│   ├── core/              # Core business logic & settings
│   │   ├── __init__.py    # Core exports
│   │   └── settings.py    # Application settings & configuration
│   ├── database/          # Database layer & adapters
│   │   ├── __init__.py    # Database exports
│   │   ├── adapters.py    # Database adapters (SQLite, PostgreSQL, MySQL)
│   │   ├── factory.py     # Database factory pattern
│   │   └── manager.py     # Database manager
│   ├── services/          # Business services
│   │   ├── __init__.py    # Services exports
│   │   ├── llm_service.py # LLM integration service
│   │   └── query_service.py # Query processing service
│   ├── models/            # Data models & schemas
│   │   ├── __init__.py    # Models exports
│   │   └── query_models.py # Pydantic models for API
│   ├── api/               # API routes & endpoints
│   │   ├── __init__.py    # API exports
│   │   └── routes.py      # FastAPI route definitions
│   ├── utils/             # Utilities & exceptions
│   │   ├── __init__.py    # Utils exports
│   │   ├── logging.py     # Logging configuration
│   │   └── exceptions.py  # Custom exceptions
│   └── main.py            # Application entry point
├── config/                # Configuration files
│   ├── requirements.txt   # Python dependencies
│   ├── .env.example      # Environment template
│   └── .env              # Environment variables (not in git)
├── scripts/               # Setup & utility scripts
│   ├── test_connections.py # Database connection testing
│   └── setup_database.py  # Database initialization
└── tests/                 # Test files (future)
```

## Web Structure (`web/`)
```
web/
├── src/                   # Source code
│   ├── components/        # React components
│   │   ├── QueryInput.js     # Natural language input component
│   │   ├── QueryInput.css    # Input component styles
│   │   ├── ResultsTable.js   # Query results display
│   │   ├── ResultsTable.css  # Results component styles
│   │   ├── DatabaseStatus.js # Database status component
│   │   └── DatabaseStatus.css # Status component styles
│   ├── services/          # API services
│   │   └── apiService.js     # Backend API communication
│   ├── hooks/             # Custom React hooks
│   │   ├── useQuery.js       # Query execution hook
│   │   └── useDatabase.js    # Database info hook
│   ├── utils/             # Frontend utilities
│   ├── types/             # TypeScript types (future)
│   ├── App.js            # Main React application
│   ├── App.css           # Main application styles
│   ├── index.js          # React entry point
│   └── index.css         # Global styles
├── public/               # Static assets
├── package.json          # Node.js dependencies and scripts
└── package-lock.json     # Dependency lock file
```

## Documentation Structure (`docs/`)
```
docs/
├── requirements.md       # Functional and non-functional requirements
├── design-document.md    # Technical architecture and design
└── api-documentation.md  # API endpoints and usage examples
```

## Key File Purposes

### Backend Core Files
- `main.py` - FastAPI app with CORS, routes, and request/response models
- `database.py` - DatabaseManager class for schema extraction and query execution
- `llm_service.py` - LLMService class for OpenAI integration and SQL generation

### Frontend Core Files
- `ChatInterface.js` - Main chat UI component handling user input and message display
- `App.js` - Root React component with routing and global state

### Configuration Files
- `.env` files - Environment-specific configuration (API keys, database URLs)
- `requirements.txt` - Python package dependencies
- `package.json` - Node.js dependencies and build scripts

## Naming Conventions
- **Python files**: snake_case (e.g., `llm_service.py`, `setup_sample_db.py`)
- **JavaScript files**: PascalCase for components (e.g., `ChatInterface.js`)
- **Database files**: lowercase with underscores (e.g., `sample_database.db`)
- **Documentation**: kebab-case (e.g., `design-document.md`)

## Import Patterns
- **Backend**: Relative imports within modules, absolute for external packages
- **Frontend**: ES6 imports, React components imported by name

## Database Files
- `sample_database.db` - Main SQLite database with customers, products, orders
- `northwind.db` - Additional sample database
- Schema includes proper foreign key relationships between tables

## Development Workflow
1. Backend runs on `localhost:8000` with auto-reload
2. Frontend runs on `localhost:3000` with hot reload
3. CORS configured to allow frontend-backend communication
4. Use `start.bat` for quick Windows development setup