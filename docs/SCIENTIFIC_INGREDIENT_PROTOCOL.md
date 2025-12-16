# Protocolo de Ingredientes Científicos

Este documento define el estándar para la creación y enriquecimiento de "Ingredientes Científicos" en el repositorio AI-Chef.

## Objetivos

Transformar ingredientes culinarios simples en entidades de datos enriquecidas que incluyan perfiles de seguridad, nutrición detallada, compuestos activos y taxonomía científica.

## Esquema Front Matter (YAML)

Cada archivo de ingrediente (`ingredients/**/*.md`) debe cumplir con el siguiente esquema extendido:

```yaml
---
name: "Tomato" # Primary ID (English preferred for filename/ID)
scientific_name: "Solanum lycopersicum"
group: "Vegetable"
image: "../../images/nombre_ingrediente.jpg"

# --- Internationalization (I18n) ---
i18n:
  en:
    common_name: "Tomato"
    other_names: []
    culinary_intro: "The edible berry of the plant Solanum lycopersicum."
  es:
    common_name: "Tomate"
    other_names: ["Jitomate"]
    culinary_intro: "Fruto de la planta Solanum lycopersicum, básico en guisos."
  zh:
    common_name: "番茄"
    other_names: ["西红柿"]
    culinary_intro: "茄科茄属植物的果实."

# --- Taxonomía y Clasificación ---
scientific_registry:
  family: "Solanaceae" # Familia botánica
  genus: "Solanum"
  synonyms: ["Nombre alternativo 1", "Nombre regional"]
  cultivars: ["Cherry", "Roma", "Beefsteak"]

# --- Perfil Nutricional (por 100g) ---
portions:
  default_g: 100
nutrition_per_100g:
  calories: 18
  protein_g: 0.9
  fat_g: 0.2
  carbs_g: 3.9
  fiber_g: 1.2
  sugar_g: 2.6

# --- Micronutrientes Clave ---
micronutrients:
  vitamin_c_mg: 13.7
  potassium_mg: 237
  magnesium_mg: 11

# --- Compuestos Activos ---
active_compounds:
  - name: "Licopeno"
    type: "Carotenoid"
    benefit: "Antioxidante potente, salud prostática."
    solubility: "Liposoluble (necesita grasa)"
    scientific_ref: "NIH/PubMed ID"

# --- Perfil de Seguridad y Alergias (NUEVO) ---
safety_profile:
  safety_score: 95 # 0-100 (100 = Muy seguro)
  consumption_limit: "Ninguno para población general"
  concerns:
    - condition: "Acidez"
      risk: "Puede causar reflujo en personas sensibles."
    - condition: "Toxicidad (Hojas)"
      risk: "Las hojas contienen solanina, son tóxicas."

allergy_profile:
  risk_level: "Low" # Low, Medium, High
  allergens: ["LTP (Lipid Transfer Protein)", "Profilin"]
  cross_reactivity: ["Polen de pasto", "Látex"]
  prevalence_percent: 1.5 # % estimado de población afectada

# --- Perfil Sensorial ---
sensory_profile:
  taste_notes: ["Ácido", "Dulce", "Umami"]
  texture_notes: ["Jugoso", "Firme"]
  spice_level: 0 # Escala Scoville o 0-10

# --- Metadatos de Enriquecimiento ---
embedding_version: 2
last_updated: "YYYY-MM-DD"
---
```

## Estructura del Markdown

El cuerpo del archivo debe contener:

1. **Descripción General**: Resumen botánico y culinario.
2. **Uso Culinario**: Técnicas recomendadas para maximizar biodisponibilidad (ej. "Cocinar con aceite para liberar licopeno").
3. **Beneficios para la Salud**: Explicación basada en evidencia de los `active_compounds`.
4. **Riesgos y Precauciones**: Detalles sobre las secciones de `safety_profile` y `allergy_profile`.
5. **Referencias**: Lista de estudios o bases de datos (USDA, NIH, PubChem).

## Reglas de Generación

1. **Veracidad**: Usar fuentes confiables (USDA, EFSA, FDA).
2. **Neutralidad**: Indicar "Evidencia limitada" si los estudios no son concluyentes.
3. **Seguridad**: Ser conservador con los límites de consumo y advertencias de toxicidad.
