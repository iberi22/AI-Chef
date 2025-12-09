# Próximos Pasos - AI-Chef

Este documento detalla las acciones inmediatas después de completar las correcciones de seguridad y la infraestructura de traducción.

## 📊 Estado Actual

### ✅ Completado

1. **Seguridad:**
   - Corregidas vulnerabilidades CVE-2025-64718 (js-yaml) y CVE-2025-64756 (glob)
   - 0 vulnerabilidades detectadas por `npm audit`
   - Documentado en `docs/SECURITY_UPDATES.md`

2. **Infraestructura de Traducción:**
   - ✅ 2 recetas de ejemplo traducidas al español:
     - `dishes/aquatic/红烧鱼.es.md` (Pescado en Salsa Roja)
     - `dishes/breakfast/完美水煮蛋.es.md` (Huevo Cocido Perfecto)
   - ✅ Script de traducción automatizada: `automation/translate_recipes.py`
   - ✅ Guía de traducción completa: `docs/TRANSLATION_GUIDE.md`

3. **Documentación:**
   - ✅ Actualizado `AGENTS.md` con historial de Jules y mejores prácticas
   - ✅ Actualizado `README.md` con sección de seguridad y automatización

### 🔄 En Progreso

- **GitHub Pages:** Pendiente configuración inicial

### ❌ Limitaciones Identificadas

- **Jules Bot:** No puede crear múltiples archivos nuevos ni configurar frameworks completos
  - PR #34 (traducción): Cerrado por error "Unable to create files"
  - PR #35 (GitHub Pages): Cerrado por complejidad excesiva

## 🎯 Próximos Pasos Inmediatos

### 1. 🧪 Probar Script de Traducción (Prioridad: ALTA)

**Objetivo:** Verificar que el script funciona correctamente antes de traducir en lote.

**Comandos:**

```powershell
# 1. Configurar API key de Gemini
$env:GEMINI_API_KEY = "tu-api-key-aqui"

# 2. Instalar dependencias
pip install google-generativeai

# 3. Prueba con 1 receta
python automation/translate_recipes.py --input dishes/aquatic/咖喱炒蟹.md

# 4. Si funciona, probar con lote pequeño
python automation/translate_recipes.py --batch dishes/breakfast/ --limit 3
```

**Criterios de éxito:**

- ✅ Script se ejecuta sin errores
- ✅ Archivos `.es.md` se crean correctamente
- ✅ Formato markdown se mantiene
- ✅ Calidad de traducción es aceptable

**Tiempo estimado:** 30-60 minutos

---

### 2. 📚 Traducción en Lote (Prioridad: MEDIA)

**Objetivo:** Traducir recetas de categorías prioritarias al español.

**Categorías sugeridas:**

1. `dishes/breakfast/` - 22 recetas
2. `dishes/aquatic/` - 29 recetas (incluyendo subdirectorios)
3. `dishes/condiment/` - 9 recetas
4. `dishes/drink/` - 22 recetas

**Comandos:**

```powershell
# Traducir desayunos (sin límite)
python automation/translate_recipes.py --batch dishes/breakfast/

# Traducir platillos acuáticos
python automation/translate_recipes.py --batch dishes/aquatic/

# Traducir condimentos
python automation/translate_recipes.py --batch dishes/condiment/

# Traducir bebidas
python automation/translate_recipes.py --batch dishes/drink/
```

**Flujo de trabajo:**

1. Ejecutar script por categoría
2. Revisar manualmente 2-3 traducciones por lote
3. Corregir errores si los hay
4. Commit y push

**Tiempo estimado:** 2-4 horas (incluye revisión)

---

### 3. 🌐 Configurar GitHub Pages con Astro (Prioridad: MEDIA)

**Objetivo:** Crear sitio web interactivo para visualizar recetas.

#### Opción A: Configuración Manual (Recomendado)

```powershell
# 1. Crear proyecto Astro
cd E:\scripts-python\AI-Chef
npm create astro@latest site

# Durante la instalación, elegir:
# - Template: "Empty"
# - TypeScript: Yes (strict)
# - Install dependencies: Yes
# - Git: No (ya está en repo)

# 2. Configurar para GitHub Pages
cd site
# Editar astro.config.mjs para añadir:
# export default defineConfig({
#   site: 'https://iberi22.github.io',
#   base: '/AI-Chef',
# })

# 3. Crear página de índice
# src/pages/index.astro - listar todas las recetas

# 4. Probar localmente
npm run dev
# Abrir http://localhost:4321
```

**Estructura esperada:**

```text
site/
├── astro.config.mjs
├── package.json
├── tsconfig.json
├── src/
│   ├── pages/
│   │   ├── index.astro        # Página principal
│   │   ├── recetas/
│   │   │   └── [slug].astro   # Plantilla dinámica
│   └── components/
│       ├── RecipeCard.astro   # Tarjeta de receta
│       └── Navigation.astro   # Navegación
└── public/
    └── styles/
```

#### Opción B: Delegar a Jules (Riesgos)

**NO recomendado** basado en experiencia previa. Si decides intentarlo:

1. Crear estructura de directorios manualmente primero:

   ```powershell
   mkdir site
   mkdir site/src
   mkdir site/src/pages
   mkdir site/src/components
   ```

2. Crear issue específico para Jules:

   ```markdown
   Título: [Jules] Add Astro component for recipe display
   
   Descripción:
   Create a single Astro component in site/src/components/RecipeCard.astro
   that displays a recipe card with:
   - Recipe title
   - Difficulty (stars)
   - Cooking time
   - Link to full recipe
   
   Use TypeScript and follow Astro best practices.
   ```

**Tiempo estimado:** 3-6 horas (manual) o 1-2 días (Jules)

---

### 4. 🤖 Automatización con GitHub Actions (Prioridad: BAJA)

**Objetivo:** Desplegar automáticamente el sitio cuando se haga push.

**Archivo:** `.github/workflows/deploy-pages.yml`

```yaml
name: Deploy Astro to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - name: Install dependencies
        run: |
          cd site
          npm ci
      - name: Build
        run: |
          cd site
          npm run build
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./site/dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**Configuración en GitHub:**

1. Ir a Settings → Pages
2. Source: GitHub Actions
3. Guardar

**Tiempo estimado:** 1 hora

---

### 5. 📖 Crear Guía de Contribución Mejorada (Prioridad: BAJA)

**Objetivo:** Facilitar que otros contribuyan con traducciones.

**Archivo:** `docs/contribuir.md` (actualizar)

Añadir sección:

```markdown
## 🌍 Cómo contribuir con traducciones

### Requisitos
- Python 3.8+
- API Key de Google Gemini

### Pasos
1. Clonar el repositorio
2. Ver ejemplos en `dishes/aquatic/红烧鱼.es.md`
3. Leer `docs/TRANSLATION_GUIDE.md`
4. Traducir usando `automation/translate_recipes.py`
5. Revisar calidad manualmente
6. Crear Pull Request

### Checklist de calidad
- [ ] Formato markdown intacto
- [ ] Nombre original entre paréntesis
- [ ] Terminología culinaria precisa
```

**Tiempo estimado:** 1 hora

---

## 📅 Cronograma Sugerido

| Semana | Tarea | Tiempo |
| ------ | ----- | ------ |
| **Semana 1** | Probar script de traducción | 1h |
| | Traducir breakfast + aquatic | 3h |
| | Commit y push traducciones | 30min |
| **Semana 2** | Configurar proyecto Astro | 4h |
| | Crear componentes básicos | 3h |
| | Probar localmente | 1h |
| **Semana 3** | Configurar GitHub Actions | 2h |
| | Deploy inicial | 1h |
| | Ajustes y correcciones | 2h |
| **Semana 4** | Traducir categorías restantes | 4h |
| | Documentación mejorada | 2h |
| | Anunciar en README | 1h |

**Total:** ~25 horas distribuidas en 4 semanas

---

## 🎬 Comandos Rápidos de Inicio

### Para empezar HOY con traducciones

```powershell
# 1. Configurar entorno
$env:GEMINI_API_KEY = "tu-api-key"
pip install google-generativeai

# 2. Traducir 5 recetas de prueba
python automation/translate_recipes.py --batch dishes/breakfast/ --limit 5

# 3. Revisar resultados
ls dishes/breakfast/*.es.md

# 4. Si todo está bien, traducir más
python automation/translate_recipes.py --batch dishes/breakfast/
python automation/translate_recipes.py --batch dishes/aquatic/

# 5. Commit
git add dishes/**/*.es.md
git commit -m "feat: add Spanish translations for breakfast and aquatic dishes"
git push origin main
```

### Para empezar HOY con GitHub Pages

```powershell
# 1. Crear proyecto Astro
npm create astro@latest site

# 2. Configurar base path en astro.config.mjs
# site: 'https://iberi22.github.io'
# base: '/AI-Chef'

# 3. Crear página básica
# Ver ejemplos en docs/

# 4. Probar localmente
cd site
npm run dev
```

---

## 🚧 Problemas Conocidos y Soluciones

### Problema: Script de traducción falla con API key

**Solución:**

```powershell
# Verificar que la variable esté configurada
echo $env:GEMINI_API_KEY

# Si está vacía, configurar de nuevo
$env:GEMINI_API_KEY = "tu-api-key"

# O pasar directamente al script
python automation/translate_recipes.py --api-key "tu-api-key" --input ...
```

### Problema: Jules no puede crear archivos

**Solución:** No usar Jules para tareas que requieran crear múltiples archivos nuevos. Usar scripts o hacer manualmente.

### Problema: Traducciones pierden formato

**Solución:** Revisar manualmente y corregir. El script preserva markdown pero puede haber casos especiales. Ver `docs/TRANSLATION_GUIDE.md`.

---

## 📞 Ayuda y Soporte

- **Issues:** <https://github.com/iberi22/AI-Chef/issues>
- **Documentación:** Ver `docs/` directory
- **Ejemplos:** Ver `dishes/aquatic/红烧鱼.es.md` y `dishes/breakfast/完美水煮蛋.es.md`

---

**Última actualización:** Diciembre 2025  
**Siguiente revisión:** Después de completar traducciones de categorías prioritarias
