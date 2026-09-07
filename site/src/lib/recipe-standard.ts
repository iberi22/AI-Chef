// site/src/lib/recipe-standard.ts — estándar de ficha de receta.
//
// Cobertura medida (405 platos, 2026-09-07):
// - title/region 94% · difficulty 100% (estrellas) · prep/cook/servings 86%
// - sensory 89% · main_ingredients 87% (280× "Ingrediente principal N" basura)
// - country/origin 0% como campo → se deriva del slug (american/…)
// - nutrition usa clave `nutrition` {calories, macros}, NO nutrition_per_serving
// Regla UI: lo faltante o en cero se oculta (sin ruido "No indicado").
export const COUNTRY_MAP: Record<string, string> = {
  american: 'Estados Unidos',
  argentinian: 'Argentina',
  brazilian: 'Brasil',
  chilean: 'Chile',
  colombian: 'Colombia',
  cuban: 'Cuba',
  dominican: 'República Dominicana',
  french: 'Francia',
  greek: 'Grecia',
  indian: 'India',
  italian: 'Italia',
  japanese: 'Japón',
  mexican: 'México',
  moroccan: 'Marruecos',
  peruvian: 'Perú',
  'puerto-rican': 'Puerto Rico',
  spanish: 'España',
  thai: 'Tailandia',
}

/** País derivado del primer segmento del slug (american/… → Estados Unidos). */
export function countryFromSlug(slug: string): string | null {
  const top = (slug || '').split('/')[0] || ''
  if (COUNTRY_MAP[top]) return COUNTRY_MAP[top]
  if (!top) return null
  return top.charAt(0).toUpperCase() + top.slice(1).replace(/-/g, ' ')
}

const JUNK_INGREDIENT = /^ingrediente principal \d+$/i

/** Filtra placeholders de contenido ("Ingrediente principal 1"). */
export function isJunkIngredient(name: unknown): boolean {
  return (
    typeof name !== 'string' ||
    name.trim() === '' ||
    JUNK_INGREDIENT.test(name.trim())
  )
}

const STOPWORDS = new Set(
  'de la el en y o con para un una del al seco seca fresco fresca grande grandes mediano mediana medianos pequeno pequena rallado rallada picado picada limpio cucharada cucharadita cucharaditas manojo taza tazas pizca diente dientes rodaja rodajas trozo trozos lata sobre vaso kilo gramos copa copas'.split(
    ' ',
  ),
)

function tokens(s: string): Set<string> {
  const ascii = s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
  const words: string[] = ascii.match(/[a-z]+/g) || []
  return new Set(words.filter((w) => !STOPWORDS.has(w) && w.length > 1))
}

export interface IngredientRef {
  id: string
  name: string
}

/**
 * Enlazador plato→ingrediente. Exacto por tokens, si no subconjunto único.
 * Plusieurs candidatos → null (no inventar enlaces). Medido: ~26% enlaza.
 */
export function buildIngredientLinker(
  refs: IngredientRef[],
): (raw: string) => string | null {
  const index = refs
    .map((r) => ({ id: r.id, t: tokens(r.name) }))
    .filter((e) => e.t.size > 0)
  return (raw: string): string | null => {
    if (isJunkIngredient(raw)) return null
    const dt = tokens(raw)
    if (dt.size === 0) return null
    const exact = index.find(
      (e) => e.t.size === dt.size && [...dt].every((w) => e.t.has(w)),
    )
    if (exact) return exact.id
    const cands = index.filter((e) => [...dt].every((w) => e.t.has(w)))
    return cands.length === 1 ? cands[0].id : null
  }
}

/** "45" → "45 min". Si el string ya trae unidad ("1 hora"), se respeta. */
export function formatMinutes(v: unknown): string | null {
  if (typeof v === 'number' && Number.isFinite(v) && v > 0) return `${v} min`
  if (typeof v === 'string') {
    const t = v.trim()
    if (t === '') return null
    if (/^\d+(\.\d+)?$/.test(t)) return `${t} min`
    return t
  }
  return null
}

export interface NutritionInfo {
  calories?: unknown
  macros?: { protein_g?: unknown; fat_g?: unknown; carbs_g?: unknown }
}

const positive = (v: unknown): boolean => typeof v === 'number' && v > 0

/** ¿La nutrición trae datos reales? Filtra {calories: 0, macros en 0}. */
export function hasNutrition(n: NutritionInfo | null | undefined): boolean {
  if (!n || typeof n !== 'object') return false
  if (positive(n.calories)) return true
  const m = n.macros
  if (!m || typeof m !== 'object') return false
  return positive(m.protein_g) || positive(m.fat_g) || positive(m.carbs_g)
}
