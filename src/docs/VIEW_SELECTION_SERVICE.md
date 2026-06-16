# View Selection Service Implementation

## Overview

A new **View Selection Service** has been implemented that uses LLM to intelligently select the most relevant database views for natural language questions.

## Architecture Flow

```
Question
  ↓
Deterministic metadata narrowing (get_metrics_metadata)
  ↓
LLM view selection (ViewSelectionService)
  ↓
[Return selected views with reasoning]
```

## Key Components

### 1. ViewSelectionService (`backend/app/services/view_selection_service.py`)

**Purpose**: Select relevant database views using LLM

**Features**:
- Loads all available view metadata (schema descriptions, purposes, columns, example questions)
- Constructs a detailed prompt with all view information
- Calls Azure OpenAI to select the best views
- Returns structured result with selected views and reasoning
- Graceful fallback if LLM is not configured

**API**:
```python
async def select_views(self, question: str) -> Dict[str, Any]:
    """
    Returns:
    {
        "question": "Which articles had the most comments last week?",
        "selected_views": ["analytics.vw_article_engagement"],
        "reason": "Question refers to articles and comment volume."
    }
    """
```

### 2. API Endpoint

**Endpoint**: `POST /api/v0/metadata/select-views`

**Request**:
```bash
curl -X POST "http://localhost:8000/api/v0/metadata/select-views?question=Which+articles+had+the+most+comments+last+week%3F"
```

**Response**:
```json
{
  "question": "Which articles had the most comments last week?",
  "selected_views": ["analytics.vw_article_engagement"],
  "reason": "Question refers to articles and comment volume."
}
```

### 3. Metadata Structure

The service leverages existing metadata YAML files:

**Schema Descriptions** (`metadata/schema_descriptions/*.yml`):
- View name
- Column names and descriptions
- Data types

**Metrics** (`metadata/metrics/*.yml`):
- Purpose and business meaning
- Example questions
- Limitations
- Expected SQL patterns

## Integration Points

### Updated Files:

1. **`backend/app/services/view_selection_service.py`** (NEW)
   - Main service implementation
   - LLM integration with fallback logic

2. **`backend/app/api/routes.py`** (MODIFIED)
   - Added import for ViewSelectionService
   - Added POST endpoint `/metadata/select-views`

3. **`backend/tests/test_services.py`** (MODIFIED)
   - Added test for ViewSelectionService
   - Tests mocking of metadata and LLM responses

## Usage Example

```python
from backend.app.services.view_selection_service import ViewSelectionService

service = ViewSelectionService()
result = await service.select_views("Which articles had the most comments last week?")

# Result:
# {
#     "question": "Which articles had the most comments last week?",
#     "selected_views": ["analytics.vw_article_engagement"],
#     "reason": "Question refers to articles and comment volume."
# }
```

## Error Handling

- **LLM Not Configured**: Service gracefully falls back to returning first available view
- **Invalid JSON Response**: Catches JSON parsing errors and returns empty selection
- **No Metadata**: Returns empty selection with appropriate message

## Testing

Run the test suite:
```bash
python -m pytest backend/tests/test_services.py::test_view_selection_service -v
```

## Configuration Requirements

For full LLM functionality, set environment variables:
```bash
AZURE_OPENAI_ENDPOINT=<your-azure-endpoint>
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_DEPLOYMENT=<your-deployment-name>
```

Or task-specific deployment:
```bash
AZURE_OPENAI_VIEW_SELECTION_DEPLOYMENT=<deployment-name>
```

## Next Steps

1. **Integrate with SQL Generation**: Pass selected views to SQL generation service
2. **Add Caching**: Cache view selections for repeated questions
3. **Improve Prompting**: Fine-tune LLM prompts based on actual performance
4. **Add Analytics**: Track which views are selected for which types of questions
5. **Support Hierarchical Selection**: Consider multi-step selection for complex queries

## Dependencies

- `openai>=1.0.0` - Azure OpenAI SDK
- `pyyaml` - YAML parsing for metadata
- Existing: `fastapi`, `sqlalchemy`, etc.
