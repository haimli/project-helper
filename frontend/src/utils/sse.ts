export interface SSEEvent {
  event: string
  data: any
}

export function createSSEConnection(
  url: string,
  body: object,
  onEvent: (event: SSEEvent) => void,
  onError?: (error: Error) => void,
): AbortController {
  const controller = new AbortController()

  fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
    signal: controller.signal,
  })
    .then(async (response) => {
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      const reader = response.body?.getReader()
      if (!reader) return

      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        let currentEvent = ''
        for (const line of lines) {
          if (line.startsWith('event:')) {
            currentEvent = line.slice(6).trim()
          } else if (line.startsWith('data:')) {
            const rawData = line.slice(5).trim()
            try {
              const data = JSON.parse(rawData)
              onEvent({ event: currentEvent || 'message', data })
            } catch {
              onEvent({ event: currentEvent || 'message', data: rawData })
            }
            currentEvent = ''
          }
        }
      }
    })
    .catch((err) => {
      if (err.name !== 'AbortError' && onError) {
        onError(err)
      }
    })

  return controller
}

export function createProgressSSE(
  url: string,
  onEvent: (event: SSEEvent) => void,
  onError?: (error: Error) => void,
): void {
  const eventSource = new EventSource(url)

  eventSource.addEventListener('progress', (e) => {
    try {
      const data = JSON.parse(e.data)
      onEvent({ event: 'progress', data })
    } catch {
      onEvent({ event: 'progress', data: e.data })
    }
  })

  eventSource.onerror = () => {
    eventSource.close()
    if (onError) onError(new Error('SSE connection closed'))
  }
}
