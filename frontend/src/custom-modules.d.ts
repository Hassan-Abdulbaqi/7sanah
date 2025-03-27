declare module './locales/index.js' {
  const messages: Record<string, Record<string, string>>
  export default messages
}

declare module './directives/clickOutside.js' {
  import { Directive } from 'vue'
  export const clickOutside: Directive
} 