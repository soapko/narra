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
   pip install openai python-dotenv
   ```

3. **Configure API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key:
   # OPENAI_API_KEY=sk-your-actual-key-here
   ```

### Running Narra

**Preferred method:**
```bash
python Narra.py
```

This runs the complete schema pipeline starting from the first schema in the execution order.

**Starting from a specific schema:**
To begin processing from a particular point in your pipeline, modify the last line in `Narra.py`:
```python
# Instead of:
tool.run_from_schema('setting_schema')

# Use any schema from your execution order:
tool.run_from_schema('characters_schema')  # Starts from characters onward
tool.run_from_schema('evidence_schema')    # Starts from evidence onward
```

**Alternative programmatic usage:**
```python
from Narra import ContentGenerationTool

tool = ContentGenerationTool('.')
tool.run_from_schema('setting_schema')  # Run complete pipeline
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

## 🛠️ Creating Your Own Schemas

**Important**: You must create your own schemas before using Narra. The framework does not generate content without properly defined schema files.

### Schema Structure

Every schema file follows this structure:

```
# Metadata
Max tokens: 1024        # Token limit for this generation
Temperature: 0.8        # Creativity level (0.0-1.0)
Model: gpt-4o          # OpenAI model to use

# Your generation instructions
Generate compelling character backgrounds that establish...

@include {setting_content}    # Reference previous schema output

## Use this schema:
~~~
## Character Profile:
Name: {character_name}
Role: {character_role}
...
~~~

---

### Example:
~~~
## Character Profile:
Name: Dr. Sarah Chen
Role: Marine biologist
~~~
```

### Leverage-First Philosophy

Narra's power comes from starting with **highly leveraged details** that scaffold future content generation:

1. **Start with Foundation Elements**: Begin with schemas that establish the most influential aspects of your narrative
   - **Setting**: Creates atmosphere and constraints for all future content
   - **Core Characters**: Psychological profiles that drive plot decisions
   - **Central Conflict**: The engine that powers narrative tension

2. **Build Increasing Definition**: Use subsequent schemas to flesh out details
   - **Character Relationships**: How foundation characters interact
   - **Plot Complications**: Events that test established character motivations
   - **Resolution Elements**: Outcomes that feel inevitable given the foundation

3. **Cross-Reference Strategically**: Later schemas should `@include` earlier content to:
   - Maintain consistency with established facts
   - Build upon character motivations and relationships
   - Create callbacks and foreshadowing

### Example: Murder Mystery Leverage Strategy
```
1. setting_schema     → Establishes atmosphere and constraints
2. characters_schema  → Creates psychological foundation for all actions  
3. evidence_schema    → Builds clues that reflect character psychology
4. crime_schema       → Event that leverages character motivations
5. resolution_schema  → Outcome that feels inevitable given foundations
```

## 🔧 Creating New Domains

Narra can be extended to any narrative domain:

### Fantasy Epics
- World-building → Character origins → Political tensions → Quest catalysts

### Business Case Studies  
- Market context → Stakeholder analysis → Problem progression → Solution development

### Educational Scenarios
- Concept introduction → Complexity building → Real-world applications

### Steps to Create New Domain

1. **Design Schema Sequence**: Map logical progression from highest to lowest leverage
2. **Create Schema Files**: Place `.txt` files in `schemas/` directory with proper metadata
3. **Define Dependencies**: Set up `@include` directives to reference previous content
4. **Configure Execution Order**: ⚠️ **Currently requires manual code editing**

### ⚠️ Configuring Execution Order (Temporary Limitation)

For now, you must manually edit the `execution_order` array in `Narra.py`:

```python
class ContentGenerationTool:
    def __init__(self, base_drive_path):
        # ... other code ...
        
        # Edit this array to match your schema sequence:
        self.execution_order = [
            "your_foundation_schema",
            "your_character_schema", 
            "your_conflict_schema",
            "your_resolution_schema"
        ]
```

**Future Enhancement**: A user-friendly GUI for managing execution order is planned for future releases.

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
