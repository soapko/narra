# Narra - Schema-Driven Narrative Construction Framework

Narra transforms LLM narrative generation from a linear process into a structured, schema-driven approach that simulates the planning and forethought that real writers employ. Instead of generating stories sequentially, Narra breaks complex narratives into interconnected schema chunks that build upon each other, creating a "diffusion model" approach to storytelling.

## 🌟 Key Features

- **Schema-Driven Generation**: Break narratives into logical, interdependent components
- **Cross-Schema References**: Later schemas can reference and build upon earlier generated content
- **Configurable Pipeline**: Per-schema control of temperature, tokens, and model selection
- **Domain Agnostic**: Extensible to any narrative domain requiring non-linear planning
- **Leverage-First Approach**: Establish high-impact details first, then build complexity

## 🚀 Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/narra.git
   cd narra
   ```

2. **Set up Python environment**
   ```bash
   python -m venv narra-env
   source narra-env/bin/activate  # On Windows: narra-env\Scripts\activate
   pip install openai
   ```

3. **Configure API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

### Basic Usage

```python
from Narra import ContentGenerationTool

# Initialize the framework
tool = ContentGenerationTool('.')

# Generate a complete murder mystery narrative
tool.run_from_schema('setting_schema')

# Or start from a specific schema
tool.run_from_schema('characters_schema')
```

## 📖 How It Works

### The Problem
LLMs generate content linearly, making it difficult to create complex narratives with hidden plans, foreshadowing, and interconnected plot elements that real writers develop through careful planning.

### The Solution
Narra addresses this by:

1. **Schema Decomposition**: Breaking narratives into logical components (setting, characters, plot points)
2. **Sequential Dependencies**: Each schema builds upon previous outputs using `@include` directives  
3. **Leverage-First Generation**: High-impact details are established first, then refined through subsequent schemas
4. **Cross-Referencing**: Later schemas can reference and expand upon earlier generated content

### Example: Murder Mystery Pipeline

```
setting_schema → characters_schema → locations_schema → evidence_schema 
    ↓                ↓                    ↓                 ↓
 Atmosphere    Deep Psychology    Investigation Sites   Crime Details
    ↓                ↓                    ↓                 ↓
        thecrime_schema → interrogate_schema → solve_schema
             ↓                   ↓                ↓
        Central Event      Character Dynamics    Resolution
```

## 🏗️ Architecture

### Core Components

- **SchemaManager**: Loads and parses schema templates with metadata
- **SchemaExecutor**: Processes include directives and executes LLM calls
- **DriveStorageManager**: Handles content persistence and cross-referencing
- **ContentGenerationTool**: Orchestrates the complete pipeline

### File Structure

```
schemas/              # Schema template definitions
├── setting_schema.txt
├── characters_schema.txt
└── [domain]_schema.txt

content/              # Generated outputs (not in repo)
├── setting_content.json
└── characters_content.json

docs/                 # Documentation
└── app_overview.md   # Detailed architecture guide
```

## 🎯 Current Implementation: Murder Mysteries

The included schemas demonstrate Narra's approach with a complete murder mystery generation system:

- **Setting**: Atmospheric foundation
- **Characters**: Deep psychological profiles with motives and relationships
- **Evidence**: Crime scene details and investigative elements  
- **Plot Progression**: From discovery through resolution

## 🔧 Creating New Domains

Narra can be extended to any narrative domain:

### Fantasy Epics
- World-building → Character origins → Political tensions → Quest catalysts

### Business Case Studies  
- Market context → Stakeholder analysis → Problem progression → Solution development

### Educational Scenarios
- Concept introduction → Complexity building → Real-world applications

### Steps to Create New Domain

1. **Design Schema Sequence**: Map logical progression of narrative elements
2. **Create Schema Files**: Develop templates with appropriate metadata
3. **Define Dependencies**: Set up cross-references using `@include` directives
4. **Configure Pipeline**: Add to execution order in `ContentGenerationTool`

## 📝 Schema Format

Each schema file contains:

```
# Metadata
Max tokens: 4096
Temperature: 0.8
Model: gpt-4o

# Content Template
Your generation instructions here...

@include {previous_schema_content}

## Use this schema:
~~~
Your output format template
~~~
```

## 🌐 Deployment

Narra includes Netlify configuration for web deployment:

```bash
netlify dev    # Local development
netlify deploy # Deploy to production
```

## 📚 Documentation

- **[App Overview](docs/app_overview.md)**: Comprehensive technical documentation
- **Schema Examples**: See `schemas/` directory for templates
- **Generated Content**: Examples in `content/` (create by running the tool)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add new schemas or enhance the framework
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🔗 Links

- [Detailed Architecture Guide](docs/app_overview.md)
- [OpenAI API Documentation](https://platform.openai.com/docs)

---

*Narra represents a paradigm shift in AI-assisted narrative creation, enabling the construction of complex, interconnected stories that maintain coherence and intentionality throughout the generation process.*
