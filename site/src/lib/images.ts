// site/src/lib/images.ts — resolución de imagen hero para recetas e ingredientes.
//
// Realidad del contenido (medida 2026-09-07, no supuesta):
// - dishes.images[].url trae basura frecuente: "pending" (311), homepages
//   (recetaschilenas.cl), artefactos YAML (">-") y rutas relativas rotas.
// - Solo 16 fotos locales reales en public/dishes (ver src/data/dish-images.json).
// - 0/552 ingredientes tienen imagen: todos caen al placeholder hasta que el
//   pipeline de contenido las genere (gap anotado, no inventamos fotos).
export const RECIPE_PLACEHOLDER = '/images/placeholders/recipe.svg'
export const INGREDIENT_PLACEHOLDER = '/images/placeholders/ingredient.svg'

const IMAGE_EXT = /\.(jpg|jpeg|png|webp|gif|avif|svg)(\?|#|$)/i

/** ¿URL utilizable como <img>? Filtra "pending", homepages y rutas rotas. */
export function isValidImageUrl(url: unknown): url is string {
  if (typeof url !== 'string') return false
  const u = url.trim().replace(/^['"]|['"]$/g, '')
  if (!u || u === 'pending' || u === '>-' || u === '-') return false
  if (u.startsWith('/')) return IMAGE_EXT.test(u) || u.includes('/dishes/')
  if (/^https?:\/\//i.test(u)) {
    // Unsplash por ID de foto (sin extensión) o cualquier URL con ext. imagen.
    // Se rechazan homepages (https://sitio.cl/) y thumbs de otros sitios.
    if (IMAGE_EXT.test(u)) return true
    if (/images\.unsplash\.com\/photo-\d+/.test(u)) return true
    return false
  }
  return false
}

export interface DishImageEntry {
  url?: string
  description?: string
}

export interface DishHeroInput {
  images?: DishImageEntry[]
  image?: string
}

/**
 * Cadena de resolución hero de receta (primero válido gana):
 * 1. images[].url válido  2. image singular válido
 * 3. foto local mapeada (dish-images.json)  4. placeholder.
 */
export function resolveDishHero(
  data: DishHeroInput | null | undefined,
  dishId: string,
  localMap: Record<string, string>,
): string {
  const cands: unknown[] = []
  if (Array.isArray(data?.images)) {
    for (const im of data.images) cands.push(im?.url)
  }
  cands.push(data?.image)
  cands.push(localMap[dishId])
  for (const c of cands) {
    if (isValidImageUrl(c))
      return (c as string).trim().replace(/^['"]|['"]$/g, '')
  }
  return RECIPE_PLACEHOLDER
}

/** Hero de ingrediente: image válida o placeholder (pipeline pendiente). */
export function resolveIngredientHero(
  data: { image?: string } | null | undefined,
): string {
  if (isValidImageUrl(data?.image)) {
    return (data as { image: string }).image.trim().replace(/^['"]|['"]$/g, '')
  }
  return INGREDIENT_PLACEHOLDER
}
