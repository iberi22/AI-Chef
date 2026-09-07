// site/src/lib/chrome-translate.ts — traducción local con la Translator API
// integrada de Chrome/Edge (on-device, gratis, sin locales commiteados).
//
// API verificada (developer.chrome.com/docs/ai/translator-api + guía oficial):
// - Solo `window.Translator` (NO el viejo `window.ai.translator`).
// - `Translator.availability({sourceLanguage, targetLanguage})` →
//   'available' | 'downloadable' | 'downloading' | 'unavailable'.
// - `Translator.create({...mismas opts, monitor})` + `t.translate(text)`.
// - Descargar el paquete de idioma exige GESTO de usuario (create desde click).
// - Solo Chrome 138+ / Edge 148+ de escritorio. Sin soporte: mensaje honesto.
//
// Idiomas: los 5 más hablados (totales, supuesto anotado): ES (fuente, sitio
// en español) + EN, ZH, HI, FR. Sin locales: se traduce el DOM en cliente.
export const SOURCE_LANG = 'es'

export interface TargetLang {
  code: string
  label: string
}

export const TARGET_LANGS: TargetLang[] = [
  { code: 'es', label: 'Español' },
  { code: 'en', label: 'English' },
  { code: 'zh', label: '中文' },
  { code: 'hi', label: 'हिन्दी' },
  { code: 'fr', label: 'Français' },
]

export type Availability =
  | 'available'
  | 'downloadable'
  | 'downloading'
  | 'unavailable'
  | 'unknown'

export interface TranslatorLike {
  translate: (text: string) => Promise<string>
  destroy?: () => void
}

interface TranslatorNS {
  availability?: (opts: {
    sourceLanguage: string
    targetLanguage: string
  }) => Promise<Availability>
  create?: (opts: {
    sourceLanguage: string
    targetLanguage: string
    monitor?: (m: {
      addEventListener: (
        ev: string,
        cb: (e: { loaded: number }) => void,
      ) => void
    }) => void
  }) => Promise<TranslatorLike>
}

function ns(): TranslatorNS | null {
  const T = (globalThis as unknown as { Translator?: TranslatorNS }).Translator
  return typeof T !== 'undefined' && T !== null ? T : null
}

/** ¿Existe la API? (No garantiza modelos descargados.) */
export function isSupported(): boolean {
  const T = ns()
  return (
    !!T &&
    typeof T.availability === 'function' &&
    typeof T.create === 'function'
  )
}

export async function getAvailability(target: string): Promise<Availability> {
  const T = ns()
  if (!T?.availability) return 'unknown'
  try {
    return await T.availability({
      sourceLanguage: SOURCE_LANG,
      targetLanguage: target,
    })
  } catch {
    return 'unknown'
  }
}

export interface TextChunk {
  nodes: Text[]
  text: string
}

const MAX_CHUNK = 800
const SKIP_TAGS = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'CODE', 'PRE'])

/** Agrupa nodos de texto visibles de <main> en lotes ≤800 chars. Puro y testeable. */
export function collectChunks(root: ParentNode): TextChunk[] {
  const chunks: TextChunk[] = []
  let cur: Text[] = []
  let len = 0
  const walker = root.ownerDocument
    ? root.ownerDocument.createTreeWalker(root, 4 /* NodeFilter.SHOW_TEXT */)
    : null
  if (!walker) return chunks
  const flush = () => {
    if (cur.length > 0) {
      chunks.push({ nodes: cur, text: cur.map((n) => n.data).join('') })
      cur = []
      len = 0
    }
  }
  let node = walker.nextNode() as Text | null
  while (node) {
    const el = node.parentElement
    const txt = node.data
    if (el && !SKIP_TAGS.has(el.tagName) && txt.trim() !== '') {
      if (len + txt.length > MAX_CHUNK) flush()
      cur.push(node)
      len += txt.length
    }
    node = walker.nextNode() as Text | null
  }
  flush()
  return chunks
}

export interface TranslateProgress {
  phase: 'checking' | 'downloading' | 'translating' | 'done' | 'error'
  loaded?: number
  current?: number
  total?: number
  message?: string
}

export interface PageTranslation {
  target: string
  chunks: { nodes: Text[]; original: string[] }[]
  destroy: () => void
}

let active: PageTranslation | null = null

/** Restaura el español original (los nodos se guardaron por referencia). */
export function restoreOriginal(): void {
  if (!active) return
  for (const c of active.chunks) {
    c.nodes.forEach((n, i) => {
      n.data = c.original[i]
    })
  }
  try {
    active.destroy()
  } catch {
    /* noop */
  }
  active = null
}

/**
 * Traduce la página al idioma destino. DEBE llamarse desde gesto de usuario
 * la primera vez (descarga del paquete). onProgress informa a la UI.
 */
export async function translatePage(
  target: string,
  onProgress: (p: TranslateProgress) => void,
): Promise<void> {
  restoreOriginal()
  if (target === SOURCE_LANG) {
    onProgress({ phase: 'done' })
    return
  }
  const T = ns()
  if (!T?.create) {
    onProgress({
      phase: 'error',
      message:
        'Tu navegador no soporta traducción local (usa Chrome o Edge de escritorio).',
    })
    return
  }
  const root = document.querySelector('main')
  if (!root) {
    onProgress({
      phase: 'error',
      message: 'No se encontró contenido para traducir.',
    })
    return
  }
  const chunks = collectChunks(root)
  if (chunks.length === 0) {
    onProgress({ phase: 'done' })
    return
  }
  onProgress({ phase: 'checking' })
  let translator: TranslatorLike
  try {
    translator = await T.create({
      sourceLanguage: SOURCE_LANG,
      targetLanguage: target,
      monitor: (m) => {
        try {
          m.addEventListener('downloadprogress', (e) => {
            onProgress({ phase: 'downloading', loaded: e.loaded })
          })
        } catch {
          /* monitor opcional */
        }
      },
    })
  } catch {
    onProgress({
      phase: 'error',
      message:
        'No se pudo preparar la traducción (¿sin conexión para descargar el idioma?).',
    })
    return
  }
  const saved = chunks.map((c) => ({
    nodes: c.nodes,
    original: c.nodes.map((n) => n.data),
  }))
  active = {
    target,
    chunks: saved,
    destroy: () => {
      try {
        translator.destroy?.()
      } catch {
        /* noop */
      }
    },
  }
  for (let i = 0; i < chunks.length; i++) {
    onProgress({ phase: 'translating', current: i + 1, total: chunks.length })
    try {
      const out = await translator.translate(chunks[i].text)
      // Reparte el texto traducido entre los nodos originales proporcionalmente.
      // Simple y seguro: primer nodo recibe todo, resto se vacía. (Supuesto
      // anotado: la segmentación por frase puede variar entre idiomas.)
      chunks[i].nodes.forEach((n, j) => {
        n.data = j === 0 ? out : ''
      })
    } catch {
      // Fallo de un lote: se deja el original y se sigue con el resto.
    }
  }
  onProgress({ phase: 'done' })
}
