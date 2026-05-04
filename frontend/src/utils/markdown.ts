import { Marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/atom-one-dark.css'

const marked = new Marked({
  renderer: {
    code({ text, lang }: { text: string; lang?: string }) {
      const language = lang && hljs.getLanguage(lang) ? lang : 'plaintext'
      const highlighted = hljs.highlight(text, { language }).value
      return `<pre class="code-block"><code class="hljs language-${language}">${highlighted}</code></pre>`
    },
  },
})

export function renderMarkdown(content: string): string {
  return marked.parse(content) as string
}
