import { describe, expect, it } from 'vitest'
import {
  INGREDIENT_PLACEHOLDER,
  isValidImageUrl,
  RECIPE_PLACEHOLDER,
  resolveDishHero,
  resolveIngredientHero,
} from './images'

const LOCAL_MAP: Record<string, string> = {
  'colombian/andina/bandeja_paisa/bandeja_paisa':
    '/dishes/colombian/andina/bandeja_paisa/images/3.webp',
}

describe('isValidImageUrl', () => {
  it('acepta http(s) con extensión de imagen', () => {
    expect(isValidImageUrl('https://www.misrecetas.com/fotos/x.jpg')).toBe(true)
    expect(isValidImageUrl('http://x.com/a.PNG?v=1')).toBe(true)
  })
  it('acepta Unsplash por ID aunque no tenga extensión', () => {
    expect(
      isValidImageUrl(
        'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600',
      ),
    ).toBe(true)
  })
  it('rechaza basura medida del contenido', () => {
    expect(isValidImageUrl('pending')).toBe(false)
    expect(isValidImageUrl('>-')).toBe(false)
    expect(isValidImageUrl('https://www.recetaschilenas.cl/')).toBe(false)
    expect(isValidImageUrl('https://www.recetasargentinas.net/')).toBe(false)
    expect(isValidImageUrl('./images/1.png')).toBe(false)
    expect(isValidImageUrl(undefined)).toBe(false)
    expect(isValidImageUrl('')).toBe(false)
  })
  it('acepta rutas locales /dishes e imágenes con extensión', () => {
    expect(isValidImageUrl('/dishes/colombian/andina/x/images/1.webp')).toBe(
      true,
    )
    expect(isValidImageUrl('/images/placeholders/recipe.svg')).toBe(true)
  })
})

describe('resolveDishHero', () => {
  it('prioriza images[0] válido', () => {
    expect(
      resolveDishHero(
        {
          images: [{ url: 'https://x.com/a.jpg' }],
          image: 'https://x.com/b.jpg',
        },
        'z',
        LOCAL_MAP,
      ),
    ).toBe('https://x.com/a.jpg')
  })
  it('salta basura y usa image singular', () => {
    expect(
      resolveDishHero(
        { images: [{ url: 'pending' }], image: 'https://x.com/b.jpg' },
        'z',
        LOCAL_MAP,
      ),
    ).toBe('https://x.com/b.jpg')
  })
  it('usa foto local mapeada cuando el frontmatter no sirve', () => {
    expect(
      resolveDishHero(
        { images: [{ url: 'pending' }] },
        'colombian/andina/bandeja_paisa/bandeja_paisa',
        LOCAL_MAP,
      ),
    ).toBe('/dishes/colombian/andina/bandeja_paisa/images/3.webp')
  })
  it('cae al placeholder sin nada válido', () => {
    expect(resolveDishHero({ images: [{ url: 'pending' }] }, 'x', {})).toBe(
      RECIPE_PLACEHOLDER,
    )
    expect(resolveDishHero(null, 'x', {})).toBe(RECIPE_PLACEHOLDER)
  })
})

describe('resolveIngredientHero', () => {
  it('usa image válida o placeholder', () => {
    expect(resolveIngredientHero({ image: 'https://x.com/a.webp' })).toBe(
      'https://x.com/a.webp',
    )
    expect(resolveIngredientHero({})).toBe(INGREDIENT_PLACEHOLDER)
    expect(resolveIngredientHero(null)).toBe(INGREDIENT_PLACEHOLDER)
  })
})
