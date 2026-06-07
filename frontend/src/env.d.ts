/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

declare module 'marked' {
  export function marked(text: string): string
}

declare module 'mermaid' {
  const mermaid: {
    initialize(config: any): void
    render(id: string, text: string): Promise<{ svg: string }>
  }
  export default mermaid
}
