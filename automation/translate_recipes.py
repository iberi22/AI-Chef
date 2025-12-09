#!/usr/bin/env python3
"""
Script para traducir recetas del chino al español usando Google Gemini API.
Mantiene el formato markdown original y crea archivos .es.md paralelos.

Uso:
    python translate_recipes.py --input dishes/aquatic/红烧鱼.md
    python translate_recipes.py --batch dishes/aquatic/  # Traducir todo el directorio
    python translate_recipes.py --all  # Traducir todas las recetas

Requisitos:
    pip install google-generativeai
    
Variables de entorno:
    GEMINI_API_KEY: Tu API key de Google AI Studio
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional
import google.generativeai as genai

# Configuración
GEMINI_MODEL = "gemini-1.5-flash"
TEMPERATURE = 0.2

# Prompt de traducción
TRANSLATION_PROMPT = """Eres un traductor experto especializado en recetas de cocina. Tu tarea es traducir esta receta del chino al español manteniendo:

1. TODO el formato markdown original (títulos, listas, negrita, etc.)
2. Los nombres originales entre paréntesis cuando sea relevante (ej: "Pescado en Salsa Roja (红烧鱼)")
3. Términos culinarios precisos y naturales en español
4. Medidas exactas sin conversión
5. Advertencias y notas de seguridad traducidas fielmente

IMPORTANTE:
- Mantén la estructura exacta del documento
- Si hay imágenes, conserva los enlaces tal cual
- Traduce "附加内容" como "Contenido adicional"
- Traduce "预估烹饪难度" como "Dificultad estimada"

Receta a traducir:

"""


def setup_gemini_api(api_key: Optional[str] = None) -> None:
    """Configura la API de Gemini."""
    if api_key is None:
        api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ Error: GEMINI_API_KEY no encontrada")
        print("Configura la variable de entorno o pasa --api-key")
        sys.exit(1)
    
    genai.configure(api_key=api_key)


def translate_recipe(content: str) -> str:
    """Traduce el contenido de una receta usando Gemini."""
    model = genai.GenerativeModel(GEMINI_MODEL)
    
    prompt = TRANSLATION_PROMPT + content
    
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=TEMPERATURE,
        )
    )
    
    return response.text


def process_recipe_file(input_path: Path, force: bool = False) -> bool:
    """
    Procesa un archivo de receta individual.
    
    Args:
        input_path: Ruta al archivo de receta en chino
        force: Si True, sobreescribe archivos existentes
    
    Returns:
        True si se tradujo exitosamente, False en caso contrario
    """
    # Verificar que es un archivo .md (no .es.md)
    if input_path.suffix != ".md" or ".es.md" in input_path.name:
        return False
    
    # Generar nombre de archivo de salida
    output_path = input_path.with_suffix(".es.md")
    
    # Verificar si ya existe
    if output_path.exists() and not force:
        print(f"⏭️  Saltando {input_path.name} (ya existe {output_path.name})")
        return False
    
    try:
        # Leer contenido original
        print(f"📖 Leyendo {input_path.name}...")
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Traducir
        print(f"🔄 Traduciendo con Gemini...")
        translated = translate_recipe(content)
        
        # Guardar traducción
        print(f"💾 Guardando {output_path.name}...")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(translated)
        
        print(f"✅ Traducción completada: {output_path.name}\n")
        return True
        
    except Exception as e:
        print(f"❌ Error procesando {input_path.name}: {e}\n")
        return False


def find_recipe_files(base_path: Path) -> list[Path]:
    """Encuentra todos los archivos de recetas (chinos) en un directorio."""
    recipes = []
    
    for md_file in base_path.rglob("*.md"):
        # Excluir archivos ya traducidos y archivos especiales
        if (
            ".es.md" not in md_file.name
            and md_file.name not in ["README.md", "CONTRIBUTING.md", "LICENSE.md"]
        ):
            recipes.append(md_file)
    
    return recipes


def main():
    parser = argparse.ArgumentParser(
        description="Traduce recetas del chino al español usando Gemini"
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Archivo o directorio de recetas a traducir"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Traducir todas las recetas en dishes/"
    )
    parser.add_argument(
        "--batch",
        type=Path,
        help="Traducir todo un directorio"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="API key de Gemini (o usar variable GEMINI_API_KEY)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Sobreescribir archivos existentes"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limitar número de recetas a traducir (útil para pruebas)"
    )
    
    args = parser.parse_args()
    
    # Configurar API
    setup_gemini_api(args.api_key)
    
    # Determinar qué archivos procesar
    recipes_to_process: list[Path] = []
    
    if args.all:
        base_dir = Path("dishes")
        recipes_to_process = find_recipe_files(base_dir)
        print(f"🔍 Encontradas {len(recipes_to_process)} recetas en dishes/\n")
        
    elif args.batch:
        recipes_to_process = find_recipe_files(args.batch)
        print(f"🔍 Encontradas {len(recipes_to_process)} recetas en {args.batch}\n")
        
    elif args.input:
        if args.input.is_file():
            recipes_to_process = [args.input]
        elif args.input.is_dir():
            recipes_to_process = find_recipe_files(args.input)
            print(f"🔍 Encontradas {len(recipes_to_process)} recetas en {args.input}\n")
        else:
            print(f"❌ Error: {args.input} no existe")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)
    
    # Aplicar límite si se especificó
    if args.limit:
        recipes_to_process = recipes_to_process[:args.limit]
        print(f"⚠️  Limitando a {args.limit} recetas\n")
    
    # Procesar recetas
    total = len(recipes_to_process)
    success = 0
    
    print(f"🚀 Iniciando traducción de {total} recetas...\n")
    print("=" * 60 + "\n")
    
    for i, recipe_path in enumerate(recipes_to_process, 1):
        print(f"[{i}/{total}] Procesando {recipe_path.relative_to(Path.cwd())}...")
        
        if process_recipe_file(recipe_path, force=args.force):
            success += 1
    
    # Resumen
    print("=" * 60)
    print(f"\n✨ Traducción completada:")
    print(f"   - Exitosas: {success}/{total}")
    print(f"   - Fallidas: {total - success}/{total}")
    
    if success > 0:
        print(f"\n💡 Siguiente paso: revisar las traducciones y hacer commit")
        print(f"   git add dishes/**/*.es.md")
        print(f"   git commit -m 'feat: add Spanish translations for {success} recipes'")


if __name__ == "__main__":
    main()
