
import os
import re

DISHES_DIR = r"e:\scripts-python\AI-Chef\dishes"
OUTPUT_FILE = r"e:\scripts-python\AI-Chef\docs\RECIPE_COMPLETENESS_REPORT.md"

REQUIRED_SECTIONS = [
    "Análisis Detallado y Sabiduría Colectiva",
    "Categorización Sensorial",
    "Perfil Nutricional",
    "Opiniones"
]

def analyze_recipes():
    results = {
        "complete": [],
        "partial": [],
        "missing": []
    }

    for root, dirs, files in os.walk(DISHES_DIR):
        for file in files:
            if file.endswith(".md") and not file.startswith("_"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()

                        missing_sections = []
                        found_sections = 0

                        # Check main section with flexibility in title
                        if "Análisis Detallado" not in content and "Análisis Sensorial" not in content:
                           missing_sections.append("Sección Principal (Análisis Detallado/Sensorial)")
                        else:
                            found_sections += 1

                        # Check specifics
                        if "Perfil de sabor" not in content and "Categorización Sensorial" not in content:
                            missing_sections.append("Datos Sensoriales")

                        if "nutrition:" not in content and "Perfil Nutricional" not in content:
                             missing_sections.append("Información Nutricional")

                        relative_path = os.path.relpath(path, DISHES_DIR)

                        if not missing_sections:
                            results["complete"].append(relative_path)
                        elif len(missing_sections) < 3: # Has some info
                            results["partial"].append((relative_path, missing_sections))
                        else:
                            results["missing"].append(relative_path)

                except Exception as e:
                    print(f"Error checking {path}: {e}")

    # Generate Report
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("# Reporte de Completitud de Recetas Científicas\n\n")

        f.write(f"## Resumen\n")
        f.write(f"- **Completas (o casi completas):** {len(results['complete'])}\n")
        f.write(f"- **Parciales:** {len(results['partial'])}\n")
        f.write(f"- **Faltantes (Prioridad Alta):** {len(results['missing'])}\n\n")

        f.write("## 🔴 Recetas sin Análisis Detallado (Prioridad)\n")
        for path in sorted(results["missing"]):
            f.write(f"- [ ] `{path}`\n")

        f.write("\n## 🟡 Recetas Parciales (Falta información específica)\n")
        for path, missing in sorted(results["partial"]):
            f.write(f"- [ ] `{path}` _Falta: {', '.join(missing)}_\n")

        f.write("\n## 🟢 Recetas con Estructura Base Completa\n")
        for path in sorted(results["complete"]):
            f.write(f"- [x] `{path}`\n")

if __name__ == "__main__":
    analyze_recipes()
    print(f"Analysis saved to {OUTPUT_FILE}")
