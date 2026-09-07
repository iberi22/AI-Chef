<script lang="ts">
import type GraphType from 'graphology'
import type { Sigma as SigmaType } from 'sigma'
import { onMount, tick } from 'svelte'

// Shared graph types for the explorer
interface GNodeDatum {
  id: string
  label?: string
  type?: string
  size?: number
  x?: number
  y?: number
}
interface GEdgeDatum {
  source: string
  target: string
}
interface GraphData {
  nodes: GNodeDatum[]
  edges: GEdgeDatum[]
}

let container = $state<HTMLDivElement | null>(null)
let renderer: SigmaType | null = null
let stats = $state({ nodes: 0, edges: 0, recipes: 0, ingredients: 0 })
let loading = $state(true)
let error = $state<string | null>(null)
let selected = $state<{
  id: string
  label: string
  type: string
  conns: number
} | null>(null)
let fullData: GraphData | null = null

const COLORS: Record<string, string> = {
  recipe: '#FF6B6B',
  ingredient: '#4ECDC4',
  vitamin: '#F9C74F',
  nutrient: '#F9C74F',
  flavor: '#FFE66D',
  texture: '#F38181',
  technique: '#AA96DA',
  region: '#7D61FF',
  place: '#B2E2F2',
  category: '#90BE6D',
  condition: '#F94144',
  substance: '#9D4EDD',
  diet: '#06D6A0',
}

const LABELS: Record<string, string> = {
  recipe: 'Recetas',
  ingredient: 'Ingredientes',
  vitamin: 'Vitaminas',
  nutrient: 'Vitaminas',
  flavor: 'Sabores',
  texture: 'Texturas',
  technique: 'Técnicas',
  region: 'Regiones',
  place: 'Lugares',
  category: 'Categorías',
  condition: 'Afecciones',
  substance: 'Substancias',
  diet: 'Dietas',
}

async function loadGraphData(): Promise<GraphData> {
  const base = (import.meta.env.BASE_URL || '/').replace(/\/$/, '')
  const candidates = [
    `${base}/graph-data.json`,
    '/graph-data.json',
    `./graph-data.json`,
  ]
  for (const url of candidates) {
    try {
      const r = await fetch(url)
      if (r.ok) return (await r.json()) as GraphData
    } catch {}
  }
  throw new Error('graph-data.json no encontrado')
}

onMount(() => {
  void (async () => {
    try {
      // Imports dinámicos: sigma/WebGL solo existe en cliente.
      // Import estático revienta el SSR (dev) con WebGL2RenderingContext is not defined.
      const [{ default: Graph }, { default: Sigma }] = await Promise.all([
        import('graphology'),
        import('sigma'),
      ])
      const data = await loadGraphData()
      fullData = data
      stats = {
        nodes: data.nodes?.length || 0,
        edges: data.edges?.length || 0,
        recipes: data.nodes?.filter((n) => n.type === 'recipe').length || 0,
        ingredients:
          data.nodes?.filter((n) => n.type === 'ingredient').length || 0,
      }
      loading = false
      await tick()
      if (container) renderSigma(container, data, Graph, Sigma)
      else error = 'graph container not mounted'
    } catch (e) {
      error = e instanceof Error ? e.message : String(e)
      loading = false
    }
  })()
  return () => {
    renderer?.kill()
    renderer = null
  }
})

function renderSigma(
  el: HTMLDivElement,
  data: GraphData,
  Graph: typeof GraphType,
  Sigma: new (
    graph: GraphType,
    container: HTMLElement,
    settings?: Record<string, unknown>,
  ) => SigmaType,
) {
  // Mini-grafo home: muestra estratificada por tipo con posiciones FA2
  // precomputadas (build). Cero fisica en cliente: render WebGL estatico.
  const byType = new Map<string, GNodeDatum[]>()
  for (const n of data.nodes || []) {
    const t = n.type || 'misc'
    const list = byType.get(t)
    if (list) list.push(n)
    else byType.set(t, [n])
  }
  const PER_TYPE = 14
  const subset: GNodeDatum[] = []
  for (const list of byType.values()) {
    const step = Math.max(1, Math.floor(list.length / PER_TYPE))
    for (let i = 0; i < list.length && subset.length < 180; i += step) {
      subset.push(list[i])
      if (subset.filter((s) => s.type === list[i].type).length >= PER_TYPE)
        break
    }
  }
  const nodeIds = new Set(subset.map((n) => n.id))
  const g = new Graph({ multi: true })
  subset.forEach((n, i) => {
    g.addNode(n.id, {
      label: n.label || n.id,
      size: n.size ? Math.max(4, Math.min(10, n.size / 2)) : 5,
      color: COLORS[n.type || ''] || '#888888',
      x: typeof n.x === 'number' ? n.x : Math.cos(i) * 10,
      y: typeof n.y === 'number' ? n.y : Math.sin(i) * 10,
    })
  })
  ;(data.edges || [])
    .filter((e) => nodeIds.has(e.source) && nodeIds.has(e.target))
    .slice(0, 350)
    .forEach((e) => {
      try {
        g.addEdge(e.source, e.target, { color: '#2a2a3e', size: 1 })
      } catch {}
    })

  renderer?.kill()
  renderer = new Sigma(g, el, {
    defaultEdgeColor: '#2a2a3e',
    defaultEdgeType: 'line',
    labelRenderedSizeThreshold: 99999,
    minCameraRatio: 0.05,
    maxCameraRatio: 3,
  })
  // Sin cámara custom: los datos van normalizados a [0,1] y la cámara
  // default de sigma (0.5, 0.5, ratio 1) los encuadra por convención.

  // Click en mini-grafo muestra la ficha SIN salir del index (modal inline).
  // El enlace "Ver en grafo" lleva a /graph?node=<id> para explorar.
  renderer.on('clickNode', (e) => {
    const datum = fullData?.nodes.find((n) => n.id === e.node)
    const conns =
      fullData?.edges.filter(
        (ed) => ed.source === e.node || ed.target === e.node,
      ).length || 0
    selected = {
      id: e.node,
      label: datum?.label || e.node,
      type: datum?.type || 'misc',
      conns,
    }
  })
  renderer.on('clickStage', () => {
    selected = null
  })
}
</script>
<div class="gos-graph-wrap">
  <div class="gos-toolbar">
    <div class="gos-toolbar-left">
      <span class="gos-title">Grafo de conocimiento GOS</span>
      <span class="gos-stats">{stats.nodes} nodos • {stats.edges} aristas • {stats.recipes} recetas</span>
    </div>
    <div class="gos-toolbar-right">
      <a href={`${(import.meta.env.BASE_URL || '/').replace(/\/$/, '')}/graph`} class="gos-btn primary">Ver grafo completo →</a>
    </div>
  </div>
  {#if loading}
    <div class="gos-loading">
      <div class="spinner"></div>
      <span>Cargando grafo global (recetas ↔ ingredientes ↔ vitaminas ↔ afecciones)...</span>
    </div>
  {:else if error}
    <div class="gos-error">No se pudo cargar: {error}</div>
  {:else}
    <div bind:this={container} class="gos-canvas"></div>
  {/if}
  {#if selected}
    <div
      class="gos-modal"
      onclick={() => (selected = null)}
      onkeydown={(e) => {
        if (e.key === 'Escape') selected = null
      }}
      tabindex="0"
      role="presentation"
    >
      <div
        class="gos-modal-card"
        role="dialog"
        tabindex="-1"
        aria-label={selected.label}
        onclick={(e) => e.stopPropagation()}
      >
        <span
          class="dot"
          style={`background:${COLORS[selected.type] || '#888888'}`}
        ></span>
        <strong>{selected.label}</strong>
        <span class="gos-modal-type"
          >{LABELS[selected.type] || selected.type} • {selected.conns}
          conexiones</span
        >
        <div class="gos-modal-actions">
          <a
            href={`${(import.meta.env.BASE_URL || '/').replace(/\/$/, '')}/graph?node=${encodeURIComponent(selected.id)}`}
            class="gos-btn primary">Ver en grafo →</a
          >
          <button class="gos-btn" onclick={() => (selected = null)}
            >Cerrar</button
          >
        </div>
      </div>
    </div>
  {/if}
  <div class="gos-legend">
    {#each Object.entries(COLORS) as [k, c]}
      <span class="legend-item"><span class="dot" style={`background:${c}`}></span>{LABELS[k] || k}</span>
    {/each}
  </div>
</div>

<style>
  .gos-graph-wrap {
    position: relative;
    border: 1px solid var(--swal-border);
    border-radius: 16px;
    overflow: hidden;
    background: var(--swal-surface);
  }
  .gos-toolbar {
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;
    border-bottom: 1px solid var(--swal-border);
    background: color-mix(in srgb, var(--swal-bg) 70%, var(--swal-surface));
  }
  .gos-title {
    font-weight: 700;
    font-size: 12px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--swal-accent);
  }
  .gos-stats {
    font-size: 11px;
    color: var(--swal-text-muted);
    margin-left: 12px;
  }
  .gos-btn {
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    border: 1px solid var(--swal-border);
    color: var(--swal-text);
    text-decoration: none;
  }
  .gos-btn.primary {
    background: var(--swal-accent);
    color: white;
    border-color: var(--swal-accent);
  }
  .gos-modal {
    position: absolute;
    inset: 0;
    z-index: 20;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(5, 5, 8, 0.55);
    padding: 16px;
  }
  .gos-modal-card {
    display: flex;
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
    max-width: 320px;
    width: 100%;
    border: 1px solid var(--swal-border);
    border-radius: 16px;
    padding: 16px;
    background: var(--swal-surface);
  }
  .gos-modal-card strong {
    color: var(--swal-text);
    font-size: 16px;
  }
  .gos-modal-card .dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
  }
  .gos-modal-type {
    font-size: 12px;
    color: var(--swal-text-muted);
  }
  .gos-modal-actions {
    display: flex;
    gap: 8px;
    margin-top: 6px;
    flex-wrap: wrap;
  }
  .gos-modal-actions .gos-btn {
    cursor: pointer;
    font-family: inherit;
  }
  .gos-canvas {
    height: 480px;
    background: radial-gradient(ellipse at top, color-mix(in srgb, var(--swal-accent) 8%, transparent), transparent 60%), var(--swal-bg);
  }
  .gos-loading {
    height: 480px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    align-items: center;
    justify-content: center;
    color: var(--swal-text-muted);
    font-size: 13px;
  }
  .spinner {
    width: 32px;
    height: 32px;
    border: 2px solid var(--swal-border);
    border-top-color: var(--swal-accent);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  .gos-error {
    padding: 32px;
    color: var(--swal-danger);
    text-align: center;
  }
  .gos-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    padding: 10px 16px;
    border-top: 1px solid var(--swal-border);
    background: var(--swal-surface);
  }
  .legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    color: var(--swal-text-secondary);
  }
  .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
  }
</style>
