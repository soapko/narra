# Narra - Schema-Driven Narrative Construction Framework

**Project ID**: `narra`

## Overview

Narra is a framework that transforms LLM narrative generation from a linear process into a structured, schema-driven approach that simulates the planning and forethought that real writers employ. Instead of generating stories sequentially, Narra breaks complex narratives into interconnected schema chunks that build upon each other, creating a "diffusion model" approach to storytelling.

## Core Philosophy

### The Linear Generation Problem

Large Language Models naturally generate content linearly, which creates challenges when constructing complex, nuanced narratives. Real writers work with intent, hidden plans, and information that is strategically revealed or made meaningful as the narrative progresses. LLMs lack this kind of forethought in their generation process.

### Narra's Solution

Narra addresses this limitation by:

1. **Schema-Driven Decomposition**: Breaking narratives into logical, interdependent components
2. **Leverage-First Approach**: Establishing high-leverage details first, then building increasing definition and complexity
3. **Cross-Schema References**: Allowing later schemas to reference and build upon earlier generated content
4. **Sequential Dependency Management**: Ensuring content is generated in the optimal order for narrative coherence

## Technical Architecture

### Schema System

Each schema is a template file (`.txt`) containing:

- **Metadata Section**: Configuration for generation parameters
  ```
  # Metadata
  Max tokens: 4096
  Temperature: 0.8
  Model: gpt-4o
  ```

- **Content Template**: Structured prompts and examples
- **Include Directives**: References to previously generated content using `@include {label}` syntax

### Execution Pipeline

The framework follows a predefined execution order where each schema:

1. Loads its configuration and template
2. Processes include directives to incorporate previous content
3. Generates new content via LLM API calls
4. Saves structured output to JSON files for future reference

### Content Management

- **Schemas Directory**: Template files defining generation rules (`schemas/`)
- **Content Directory**: Generated JSON outputs (`content/`)
- **Cross-Referencing**: Automatic content inclusion and dependency resolution

## File Organization

```
/ ─ schemas/              ← Schema template definitions
│   ├─ setting_schema.txt
│   ├─ characters_schema.txt
│   └─ [domain]_schema.txt
│
├─ content/               ← Generated content outputs
│   ├─ setting_content.json
│   ├─ characters_content.json  
│   └─ [domain]_content.json
│
├─ _archive/              ← Historical schema versions
├─ docs/                  ← Documentation and decisions
└─ Narra.py              ← Core framework implementation
```

## Framework Components

### SchemaManager
- Loads and parses schema files
- Extracts metadata and content templates
- Manages schema dependencies

### DriveStorageManager  
- Handles file I/O operations
- Manages content persistence
- Provides cross-schema content access

### SchemaExecutor
- Processes include directives
- Executes LLM API calls
- Manages generation parameters per schema

### ContentGenerationTool
- Orchestrates the complete pipeline
- Manages execution order
- Provides entry points for different starting schemas

## Domain Extensibility

While the current implementation focuses on murder mystery generation, Narra's architecture supports any narrative domain requiring non-linear planning:

### Potential Applications
- **Fantasy Epics**: World-building, character arcs, plot threads
- **Business Case Studies**: Stakeholder analysis, problem progression, solution development
- **Historical Recreations**: Context establishment, character motivations, event sequences
- **Educational Scenarios**: Concept introduction, complexity building, practical applications
- **Interactive Fiction**: Branching narratives, character development, world consistency

### Creating New Domains

1. **Define Schema Sequence**: Identify logical progression of narrative elements
2. **Create Templates**: Develop schema files with appropriate metadata and prompts  
3. **Establish Dependencies**: Map cross-references between schemas using include directives
4. **Configure Execution Order**: Set up the pipeline sequence in the main tool

## Current Implementation: Murder Mystery

The murder mystery domain serves as a reference implementation demonstrating:

### Schema Progression
1. **Setting**: Establish atmospheric foundation
2. **Characters**: Develop psychological profiles and relationships  
3. **Reports/Locations**: Build investigative context
4. **Evidence/Crime**: Construct central mystery elements
5. **Interrogation**: Create character interactions
6. **Resolution Phases**: Progressive revelation and solving

### Leverage Patterns
- Characters established with high-impact psychological details first
- Evidence and motives built upon character foundations
- Resolution schemas reference all previous content for coherent conclusions

## API Integration

- **OpenAI Integration**: Configurable model selection per schema
- **Retry Logic**: Robust error handling with automatic retries
- **Parameter Control**: Per-schema temperature, token limits, and model selection
- **Rate Limiting**: Built-in delays and error management

## Development Workflow

### Adding New Schemas
1. Create schema file in `schemas/` directory
2. Define metadata and content template
3. Add to execution order in main tool
4. Test generation and cross-references

### Modifying Execution Order
Update the `execution_order` array in `ContentGenerationTool` to reflect new dependencies or sequence changes.

### Content Iteration
Use `run_from_schema()` method to regenerate content from any point in the pipeline, useful for testing changes or exploring variations.

## Future Enhancements

- **Multi-Domain Support**: Framework extensions for handling multiple narrative types simultaneously
- **Interactive Schema Designer**: GUI tools for creating and testing new schema sequences
- **Content Validation**: Automated checking of cross-references and narrative consistency
- **Export Formats**: Support for various output formats beyond JSON
- **Collaborative Features**: Multi-user schema development and content generation

## Configuration

### Netlify Deployment Support

```toml
# netlify.toml — minimum viable scaffold
[functions]
  directory = "netlify/functions"
  node_bundler = "esbuild"
  external_node_modules = ["express"]

[[redirects]]
  from = "/api/*"
  to   = "/.netlify/functions/api/:splat"
  status = 200
  force  = true
```

**Hosting**: netlify

## Getting Started

1. **Install Dependencies**: Set up Python environment with OpenAI library
2. **Configure API**: Set OpenAI API key in environment
3. **Choose Domain**: Use existing murder mystery or create new schema set
4. **Execute Pipeline**: Run `tool.run_from_schema('schema_name')` to generate content
5. **Iterate**: Modify schemas and regenerate as needed

Narra represents a paradigm shift in AI-assisted narrative creation, enabling the construction of complex, interconnected stories that maintain coherence and intentionality throughout the generation process.
