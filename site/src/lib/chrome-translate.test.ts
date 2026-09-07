import { describe, expect, it } from 'vitest'
import {
  collectChunks,
  isSupported,
  restoreOriginal,
  SOURCE_LANG,
  TARGET_LANGS,
  translatePage,
} from './chrome-translate'

describe('TARGET_LANGS', () => {
  it('cubre los 5 idiomas más hablados con ES como fuente', () => {
    expect(SOURCE_LANG).toBe('es')
    expect(TARGET_LANGS.map((l) => l.code)).toEqual([
      'es',
      'en',
      'zh',
      'hi',
      'fr',
    ])
  })
})

describe('isSupported', () => {
  it('false sin window.Translator (jsdom)', () => {
    expect(isSupported()).toBe(false)
  })
})

describe('collectChunks', () => {
  it('agrupa texto y salta script/style', () => {
    document.body.innerHTML =
      '<main><h1>Hola mundo</h1><p>Receta rica</p><script>var x = 1;</script><style>.a{}</style></main>'
    const chunks = collectChunks(document.querySelector('main') as HTMLElement)
    const all = chunks.map((c) => c.text).join('|')
    expect(all).toContain('Hola mundo')
    expect(all).toContain('Receta rica')
    expect(all).not.toContain('var x')
    expect(all).not.toContain('.a{}')
  })
  it('respeta el tope por lote', () => {
    document.body.innerHTML = `<main><p>${'a'.repeat(900)}</p><p>${'b'.repeat(900)}</p></main>`
    const chunks = collectChunks(document.querySelector('main') as HTMLElement)
    expect(chunks.length).toBeGreaterThanOrEqual(2)
    for (const c of chunks) expect(c.text.length).toBeLessThanOrEqual(900)
  })
})

describe('translatePage sin API', () => {
  it('reporta error honesto y no rompe el DOM', async () => {
    document.body.innerHTML = '<main><p>Contenido original</p></main>'
    const phases: string[] = []
    await translatePage('en', (p) => phases.push(p.phase))
    expect(phases).toContain('error')
    expect(document.querySelector('main')?.textContent).toContain(
      'Contenido original',
    )
  })
  it('restoreOriginal sin estado activo no falla', () => {
    expect(() => restoreOriginal()).not.toThrow()
  })
  it('volver a es reporta done', async () => {
    const phases: string[] = []
    await translatePage('es', (p) => phases.push(p.phase))
    expect(phases).toEqual(['done'])
  })
})
