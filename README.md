# Narra - Schema-Driven Narrative Construction CLI Framework

Narra is a Python command-line tool that transforms LLM narrative generation from a linear process into a structured, schema-driven approach that simulates the planning and forethought that real writers employ. Instead of generating stories sequentially, Narra breaks complex narratives into interconnected schema chunks that build upon each other, creating a "diffusion model" approach to storytelling.

## 🌟 Key Features

- **Schema-Driven Generation**: Break narratives into logical, interdependent components
- **Cross-Schema References**: Later schemas can reference and build upon earlier generated content
- **Built-in Evaluation**: Three-step critique process ensures content quality and revision
- **Markdown Output**: Human-readable .md files instead of JSON for better accessibility
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
tool.run_from_schema('characters_schema')    # Starts from characters onward
tool.run_from_schema('relationships_schema') # Starts from relationships onward
tool.run_from_schema('escalation_schema')    # Starts from escalation onward
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

### Example: Workplace Psychological Thriller Pipeline

```
setting_schema → core_incident_schema → characters_schema → relationships_schema
    ↓                    ↓                     ↓                     ↓
Workplace Tension   Triggering Event   Psychological Depth   Hidden Alliances
    ↓                    ↓                     ↓                     ↓
secrets_schema → escalation_schema → clues_schema → confrontations_schema
    ↓                    ↓                ↓                ↓
Personal Stakes    Building Paranoia   Evidence Trails   Breaking Points
    ↓                    ↓                ↓                ↓
        revelation_schema → aftermath_schema
             ↓                     ↓
        Truth Unveiled       Consequences
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
├── core_incident_schema.txt
├── characters_schema.txt
├── relationships_schema.txt
├── secrets_schema.txt
├── escalation_schema.txt
├── clues_schema.txt
├── confrontations_schema.txt
├── revelation_schema.txt
└── aftermath_schema.txt

content/              # Generated markdown outputs (included for demo)
├── setting_content.md
├── core_incident_content.md
├── characters_content.md
├── relationships_content.md
├── secrets_content.md
├── escalation_content.md
├── clues_content.md
├── confrontations_content.md
├── revelation_content.md
└── aftermath_content.md

docs/                 # Documentation
└── app_overview.md   # Detailed architecture guide
```

## 🎯 Current Implementation: Workplace Psychological Thriller

The included schemas demonstrate Narra's approach with a complete workplace psychological thriller generation system:

- **Setting**: Establishes workplace environment and inherent tensions
- **Core Incident**: The triggering event that sets paranoia in motion
- **Characters**: Deep psychological profiles with hidden motives
- **Relationships**: Complex workplace dynamics and secret alliances
- **Secrets**: Personal vulnerabilities that raise stakes
- **Escalation**: Building paranoia and suspicious behavior
- **Clues**: Ambiguous evidence and digital breadcrumbs
- **Confrontations**: Key conflicts and character breakdowns
- **Revelation**: The truth behind the psychological manipulation
- **Aftermath**: Character consequences and emotional fallout

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

### Example: Workplace Psychological Thriller Leverage Strategy
```
1. setting_schema         → Establishes workplace atmosphere and constraints
2. core_incident_schema   → Creates triggering event that drives all paranoia
3. characters_schema      → Psychological foundation for all character actions
4. relationships_schema   → Complex dynamics that amplify tensions
5. secrets_schema         → Personal stakes that make characters vulnerable
6. escalation_schema      → Building paranoia leverages established secrets
7. clues_schema           → Evidence trails that reflect character psychology
8. confrontations_schema  → Conflicts inevitable given established dynamics
9. revelation_schema      → Truth that explains all previous suspicious behavior
10. aftermath_schema      → Consequences that feel earned from foundation
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

## 📝 Schema Format with Built-in Evaluation

Each schema file contains:

```
# Metadata
Max tokens: 1024
Temperature: 0.8
Model: gpt-4o

# Content Template
Your generation instructions here...

@include {previous_schema_content}

## Use this schema:
~~~
## Your Content Section:
{your_content_fields}

## Evaluation:
1. Identify the single biggest flaw or weak point in the above content.
2. Pinpoint any inconsistency or cliché that undermines tension.
3. Rewrite the content above, incorporating fixes for the identified flaws:

## Revised Content:
{revised_content}
~~~

---

### Example:
~~~
## Setup - Workplace Setting:
The setting is: A high-pressure tech startup with glass-walled offices...

## Evaluation:
1. Identify the single biggest flaw or weak point in the above content.
   - The concept feels generic and lacks specific tension-building details.

2. Pinpoint any inconsistency or cliché that undermines tension.
   - Glass-walled offices are overused in workplace thrillers.

3. Rewrite the content above, incorporating fixes for the identified flaws:

## Revised Content:
The setting is: A boutique consulting firm where employees work in cramped cubicles under flickering fluorescent lights, while senior partners monitor productivity through mandatory screen-sharing software that tracks every keystroke and website visit.
~~~
```

**Key Innovation**: The evaluation system forces the AI to critique and actually rewrite content, ensuring subsequent schemas receive polished, final material rather than rough drafts.

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
