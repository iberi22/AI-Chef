# AI-Chef

**AI-Ready Global Recipe Repository with Semantic Search & Metadata Automation**

[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)
[![Recipes](https://img.shields.io/badge/Recipes-100+-green?style=for-the-badge)](dishes/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-Active-success?style=for-the-badge)](docs/CI_CD.md)

---

## English

### 🌟 What is AI-Chef?

AI-Chef is a modern, open-source recipe repository inspired by [HowToCook](https://github.com/Anduin2017/HowToCook). It provides a structured, AI-ready collection of global recipes enriched with metadata, sensory profiles, nutritional data, and automatic vectorization for semantic search and RAG applications.

### ✨ Key Features

- **📋 Standardized Recipes** - YAML Front Matter with sensory, nutritional, and cultural context
- **🤖 AI-Ready** - Pre-computed vectors (`recipes_vectors.jsonl`) for ChromaDB, Qdrant, and other RAG systems
- **🔄 Automated CI/CD** - Metadata extraction and vectorization on every push to main
- **🌍 Multilingual** - Spanish, English, Portuguese, and Chinese support
- **📚 Well-Documented** - Complete guides for setup, contribution, and AI integration
- **🔐 Protected** - Branch protection with required CI/CD checks

### 🚀 Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/iberi22/AI-Chef.git
   cd AI-Chef
   ```

2. **Install dependencies**

   ```bash
   npm install
   pip install -r requirements.txt
   ```

3. **Set up pre-commit hooks**

   ```bash
   npm run prepare
   ```

4. **Explore recipes**

   ```bash
   ls dishes/colombian/
   cat dishes/colombian/nacionales/ajiaco/ajiaco.md
   ```

### 📚 Documentation

- [CI/CD Workflows](docs/CI_CD.md) - Automated metadata extraction and branch protection
- [Pre-commit Setup](docs/precommit.md) - Code quality hooks with Husky and lint-staged
- [Contributing Guide](docs/contribuir.md) - How to add new recipes
- [Vectorization for AI](docs/vectorizacion.md) - Using recipes with embeddings and RAG
- [Agent Automation](AGENTS.md) - Gemini CLI and Jules bot configuration
- [Security Updates](docs/SECURITY_UPDATES.md) - CVE fixes and security policy

### 🔒 Security & Automation

- **Dependabot**: Automated security updates for npm dependencies
- **Jules Bot**: AI assistant for issue-based task automation (experimental)
- **Auto-merge**: PRs with `automation` label are auto-approved when checks pass
- **Security Audits**: Run `npm audit` on every PR

See [AGENTS.md](AGENTS.md) for details on automation tools and best practices.

### 🛠️ Recipe Format

Each recipe uses YAML Front Matter for metadata:

```yaml
---
title: "Ajiaco Colombiano"
region: "Nacional"
categories: ["Soup", "Traditional", "Comfort Food"]
sensory:
  flavor: ["Earthy", "Herbaceous", "Umami"]
  texture: ["Creamy", "Hearty"]
prep_time: "45 minutos"
servings: 4
difficulty: "★★☆☆☆"
images:
  - url: "https://..."
sources:
  - "https://..."
license: "MIT"
---
```

### 🤝 Contributing

1. Create a branch: `git checkout -b feature/new-recipe`
2. Follow the recipe template and sensory enrichment guidelines
3. Submit a Pull Request
4. CI/CD checks will validate your contribution
5. Once merged, metadata and vectors update automatically

### 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## Español

### 🌟 ¿Qué es AI-Chef?

AI-Chef es un recetario moderno y de código abierto inspirado en [HowToCook](https://github.com/Anduin2017/HowToCook). Proporciona una colección estructurada y lista para IA de recetas globales enriquecidas con metadatos, perfiles sensoriales, datos nutricionales y vectorización automática.

### ✨ Características Principales

- **📋 Recetas Estandarizadas** - YAML Front Matter con contexto sensorial, nutricional y cultural
- **🤖 Lista para IA** - Vectores pre-computados para sistemas RAG
- **🔄 CI/CD Automatizado** - Extracción de metadatos en cada push
- **🌍 Multilingüe** - Soporte en español, inglés, portugués y chino
- **📚 Bien Documentada** - Guías completas para setup y contribución
- **🔐 Protegida** - Protección de rama con checks obligatorios

### 🚀 Inicio Rápido

```bash
# Clonar y configurar
git clone https://github.com/iberi22/AI-Chef.git
cd AI-Chef
npm install && pip install -r requirements.txt

# Explorar recetas
ls dishes/colombian/
cat dishes/colombian/nacionales/ajiaco/ajiaco.md
```

### 📚 Documentación

- [Guía de Contribución](docs/contribuir.md)
- [Flujo CI/CD](docs/CI_CD.md)
- [Vectorización para IA](docs/vectorizacion.md)

### 🤝 Cómo Contribuir

1. Crea una rama con tu receta
2. Sigue la plantilla estándar
3. Haz un Pull Request
4. Los checks automáticos validan tu aporte
5. Al mergear, metadatos y vectores se actualizan

---

## Português

### 🌟 O que é AI-Chef?

AI-Chef é um repositório de receitas moderno e de código aberto inspirado em [HowToCook](https://github.com/Anduin2017/HowToCook). Fornece uma coleção estruturada e pronta para IA de receitas globais enriquecidas com metadados, perfis sensoriais e vetorização automática.

### ✨ Características Principais

- **📋 Receitas Padronizadas** - YAML Front Matter com contexto sensorial e cultural
- **🤖 Pronta para IA** - Vetores pré-computados para sistemas RAG
- **🔄 CI/CD Automatizado** - Extração de metadados em cada push
- **🌍 Multilingue** - Suporte em espanhol, inglês, português e chinês
- **📚 Bem Documentada** - Guias completos para setup e contribuição

### 🚀 Início Rápido

```bash
git clone https://github.com/iberi22/AI-Chef.git
cd AI-Chef
npm install && pip install -r requirements.txt
ls dishes/colombian/
```

### 📚 Documentação

- [Guia de Contribuição](docs/contribuir.md)
- [Fluxo CI/CD](docs/CI_CD.md)
- [Vetorização para IA](docs/vectorizacion.md)

---

## 中文

### 🌟 AI-Chef 是什么？

AI-Chef 是一个受 [HowToCook](https://github.com/Anduin2017/HowToCook) 启发的现代开源食谱库。它提供了一个结构化、AI 就绪的全球食谱集合，包含元数据、感官信息、营养数据和自动矢量化。

### ✨ 主要特性

- **📋 标准化食谱** - YAML Front Matter 包含感官和文化背景
- **🤖 AI 就绪** - 预计算的向量用于 RAG 系统
- **🔄 自动化 CI/CD** - 每次推送时提取元数据
- **🌍 多语言支持** - 西班牙语、英语、葡萄牙语和中文
- **📚 文档完善** - 完整的设置和贡献指南
- **🔐 受保护的** - 分支保护和必需的 CI/CD 检查

### 🚀 快速开始

```bash
git clone https://github.com/iberi22/AI-Chef.git
cd AI-Chef
npm install && pip install -r requirements.txt
ls dishes/colombian/
```

### 📚 文档

- [贡献指南](docs/contribuir.md)
- [CI/CD 流程](docs/CI_CD.md)
- [AI 矢量化](docs/vectorizacion.md)

---

**Made with ❤️ for Global Cuisine & AI Agents**
