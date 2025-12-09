# Guía de Traducción de Recetas

Esta guía explica cómo traducir recetas del chino al español manteniendo la calidad y estructura original.

## 📋 Índice

1. [Convenciones de nomenclatura](#convenciones-de-nomenclatura)
2. [Estructura de archivos](#estructura-de-archivos)
3. [Métodos de traducción](#métodos-de-traducción)
4. [Directrices de calidad](#directrices-de-calidad)
5. [Ejemplos](#ejemplos)

## Convenciones de nomenclatura

### Sufijo `.es.md`

Todas las traducciones al español deben usar el sufijo `.es.md`:

```text
dishes/aquatic/红烧鱼.md         # Original en chino
dishes/aquatic/红烧鱼.es.md      # Traducción en español
```

### Nombres de archivo

- **NO cambies** el nombre del archivo original
- Mantén el nombre en chino y simplemente agrega `.es.md`
- Esto permite vincular fácilmente las versiones original y traducida

## Estructura de archivos

### Organización por idiomas

```text
dishes/
├── aquatic/
│   ├── 红烧鱼.md        # Original (chino)
│   ├── 红烧鱼.es.md     # Español
│   └── 红烧鱼.en.md     # Inglés (futuro)
├── breakfast/
│   ├── 完美水煮蛋.md
│   └── 完美水煮蛋.es.md
```

### Mantener estructura paralela

- Los archivos `.es.md` deben estar en el mismo directorio que el original
- Facilita la navegación y mantenimiento
- Permite scripts automatizados para validar traducciones

## Métodos de traducción

### 1. Traducción Manual ✍️

**Cuándo usar:**

- Recetas complejas con terminología especializada
- Primera traducción de referencia
- Validación de traducciones automáticas

**Proceso:**

1. Leer la receta completa en el original
2. Investigar términos culinarios desconocidos
3. Traducir manteniendo el formato markdown
4. Revisar y corregir

### 2. Traducción Automatizada 🤖

**Cuándo usar:**

- Traducción en lote de muchas recetas
- Traducciones que luego serán revisadas manualmente

**Herramienta:**

```bash
# Traducir una receta
python automation/translate_recipes.py --input dishes/aquatic/红烧鱼.md

# Traducir un directorio completo
python automation/translate_recipes.py --batch dishes/breakfast/

# Traducir todo el repositorio
python automation/translate_recipes.py --all --limit 10  # Limitar a 10 recetas
```

**Requisitos:**

```bash
pip install google-generativeai
export GEMINI_API_KEY="tu-api-key"
```

## Directrices de calidad

### ✅ Lo que DEBES hacer

1. **Mantener formato markdown exacto:**

   ```markdown
   # Título principal
   ## Subtítulo
   - Lista
   * Otra lista
   **Negrita**
   ```

2. **Preservar nombre original entre paréntesis:**

   ```markdown
   # Pescado en Salsa Roja (红烧鱼)
   ```

3. **Traducir terminología culinaria con precisión:**
   - 红烧 → "en salsa roja" (no "cocido rojo")
   - 水煮 → "cocido en agua" o "hervido"
   - 清蒸 → "al vapor"
   - 油炸 → "frito"

4. **Mantener medidas sin conversión:**

   ```markdown
   - Sal: 10g    # NO convertir a cucharadas
   - Agua: 500ml # Mantener mililitros
   ```

5. **Traducir advertencias fielmente:**

   ```markdown
   - **ADVERTENCIA**: Si nunca has usado un cuchillo...
   ```

6. **Conservar enlaces e imágenes:**

   ```markdown
   ![Pescado](https://ejemplo.com/imagen.jpg)  # No modificar
   ```

### ❌ Lo que NO debes hacer

1. **Cambiar estructura del documento**
2. **Omitir secciones** (incluso si parecen redundantes)
3. **Añadir contenido nuevo** no presente en el original
4. **Traducir nombres de archivo o rutas**
5. **Convertir unidades de medida** (mantener sistema métrico)

## Ejemplos

### Ejemplo 1: Receta Simple

**Original (`完美水煮蛋.md`):**

```markdown
# 完美水煮蛋的做法

预估烹饪难度：★★★★★

## 必备原料和工具

- 新鲜鸡蛋（推荐 AA 级）
- 100°C 沸水锅
```

**Traducción (`完美水煮蛋.es.md`):**

```markdown
# Huevo Cocido Perfecto (完美水煮蛋)

Dificultad estimada: ★★★★★

## Ingredientes y herramientas esenciales

- Huevos frescos (recomendado grado AA)
- Olla de agua hirviendo a 100°C
```

### Ejemplo 2: Secciones estándar

| Chino | Español |
| --- | --- |
| 的做法 | Preparación de / Cómo hacer |
| 预估烹饪难度 | Dificultad estimada |
| 必备原料和工具 | Ingredientes y herramientas esenciales |
| 计算 | Cantidades |
| 操作 | Preparación / Procedimiento |
| 附加内容 | Contenido adicional |

### Ejemplo 3: Términos culinarios comunes

| Chino | Español |
| --- | --- |
| 切碎 | picar |
| 切片 | cortar en rodajas |
| 切丝 | cortar en tiras |
| 翻炒 | saltear |
| 煎 | freír (poca aceite) |
| 炸 | freír (mucho aceite) |
| 蒸 | cocinar al vapor |
| 煮 | hervir/cocinar |
| 烤 | hornear/asar |
| 炖 | guisar/estofar |

## Flujo de trabajo recomendado

### Para contribuidores individuales

1. **Seleccionar receta** sin traducción al español
2. **Traducir manualmente** o usar el script
3. **Revisar calidad** comparando con ejemplos
4. **Crear PR** con el archivo `.es.md`

### Para traducción en lote

1. **Configurar entorno:**

   ```bash
   export GEMINI_API_KEY="tu-api-key"
   pip install google-generativeai
   ```

2. **Traducir lote:**

   ```bash
   # Ejemplo: traducir todas las recetas de desayuno
   python automation/translate_recipes.py --batch dishes/breakfast/ --limit 5
   ```

3. **Revisar manualmente** las traducciones generadas

4. **Corregir errores** si los hay

5. **Commit y PR:**

   ```bash
   git add dishes/**/*.es.md
   git commit -m "feat: add Spanish translations for breakfast recipes"
   git push origin feature/spanish-breakfast
   ```

## Validación de calidad

### Checklist antes de hacer commit

- [ ] Formato markdown intacto (títulos, listas, negritas)
- [ ] Nombre original entre paréntesis en título principal
- [ ] Terminología culinaria precisa
- [ ] Medidas sin convertir
- [ ] Advertencias de seguridad traducidas fielmente
- [ ] Enlaces e imágenes preservados
- [ ] Sin contenido añadido o removido
- [ ] Ortografía y gramática correctas

### Herramientas de validación

```bash
# Verificar formato markdown
markdownlint dishes/**/*.es.md

# Comparar estructura de archivos
diff -u dishes/aquatic/红烧鱼.md dishes/aquatic/红烧鱼.es.md
```

## Contribuir mejoras

Si encuentras:

- Errores en traducciones existentes
- Términos culinarios que se pueden mejorar
- Problemas con el script de traducción

Por favor abre un **Issue** o **Pull Request** en:
<https://github.com/iberi22/AI-Chef/issues>

## Recursos adicionales

- [CONTRIBUTING.es.md](../CONTRIBUTING.es.md) - Guía general de contribución
- [METODOLOGIA.md](../METODOLOGIA.md) - Metodología del proyecto
- [automation/translate_recipes.py](../automation/translate_recipes.py) - Script de traducción

---

**Última actualización:** Diciembre 2025  
**Idiomas disponibles:** Español (es), próximamente Inglés (en), Portugués (pt)
