import { describe, expect, it } from 'vitest'
import {
  buildIngredientLinker,
  countryFromSlug,
  formatMinutes,
  hasNutrition,
  isJunkIngredient,
} from './recipe-standard'

describe('countryFromSlug', () => {
  it('mapea el top dir a país en español', () => {
    expect(countryFromSlug('mexican/tacos_al_pastor')).toBe('México')
    expect(countryFromSlug('colombian/andina/x/y')).toBe('Colombia')
    expect(countryFromSlug('puerto-rican/a/b')).toBe('Puerto Rico')
  })
  it('capitaliza desconocidos y null en vacío', () => {
    expect(countryFromSlug('atlante/x')).toBe('Atlante')
    expect(countryFromSlug('')).toBe(null)
  })
})

describe('isJunkIngredient', () => {
  it('filtra placeholders de contenido', () => {
    expect(isJunkIngredient('Ingrediente principal 1')).toBe(true)
    expect(isJunkIngredient('Ingrediente principal 2')).toBe(true)
    expect(isJunkIngredient('')).toBe(true)
    expect(isJunkIngredient('Yuca')).toBe(false)
    expect(isJunkIngredient('Especias')).toBe(false)
  })
})

describe('buildIngredientLinker', () => {
  const link = buildIngredientLinker([
    { id: 'condiments/panela', name: 'Panela' },
    { id: 'fruits/limon', name: 'Limón' },
    {
      id: 'pending_review/cucharada_de_oregano_seco',
      name: 'Cucharada De Orégano Seco',
    },
    { id: 'vegetables/papa_criolla', name: 'Papa Criolla' },
    { id: 'x/sal_marina', name: 'Sal Marina' },
    { id: 'y/sal_rosada', name: 'Sal Rosada' },
  ])
  it('enlaza exactos ignorando cantidad y tildes', () => {
    expect(link('Panela')).toBe('condiments/panela')
    expect(link('Orégano seco')).toBe(
      'pending_review/cucharada_de_oregano_seco',
    )
  })
  it('enlaza subconjunto único y rechaza ambiguos y basura', () => {
    expect(link('Papa criolla')).toBe('vegetables/papa_criolla')
    expect(link('Sal')).toBe(null)
    expect(link('Ingrediente principal 1')).toBe(null)
    expect(link('Unicornio ahumado')).toBe(null)
  })
})

describe('formatMinutes', () => {
  it('normaliza números y respeta unidades existentes', () => {
    expect(formatMinutes(45)).toBe('45 min')
    expect(formatMinutes('45')).toBe('45 min')
    expect(formatMinutes('45 min')).toBe('45 min')
    expect(formatMinutes('1 hora')).toBe('1 hora')
    expect(formatMinutes('3 días (fermentación)')).toBe('3 días (fermentación)')
    expect(formatMinutes(0)).toBe(null)
    expect(formatMinutes(undefined)).toBe(null)
  })
})

describe('hasNutrition', () => {
  it('filtra ceros y acepta datos reales', () => {
    expect(
      hasNutrition({
        calories: 0,
        macros: { protein_g: 0, fat_g: 0, carbs_g: 0 },
      }),
    ).toBe(false)
    expect(
      hasNutrition({
        calories: 6511,
        macros: { protein_g: 780, fat_g: 330, carbs_g: 0.4 },
      }),
    ).toBe(true)
    expect(hasNutrition(null)).toBe(false)
    expect(hasNutrition({} as never)).toBe(false)
  })
})
