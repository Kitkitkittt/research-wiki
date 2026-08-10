(() => {
  const content = document.querySelector('.docs-content')
  const toc = document.querySelector('[data-docs-toc]')
  if (content && toc) {
    content.querySelectorAll('h2, h3').forEach((heading) => {
      if (!heading.id) return
      const item = document.createElement('li')
      if (heading.tagName === 'H3') item.className = 'subsection'
      const link = document.createElement('a')
      link.href = `#${heading.id}`
      link.textContent = heading.textContent
      item.append(link)
      toc.append(item)
    })
  }

  const button = document.querySelector('[data-copy-handoff]')
  const status = document.querySelector('[data-copy-status]')
  if (!button || !status) return

  button.addEventListener('click', async () => {
    const original = button.textContent
    button.disabled = true
    status.textContent = 'Loading public agent context…'
    try {
      const response = await fetch(button.dataset.copyHandoff, {
        credentials: 'omit',
        headers: { Accept: 'text/plain' },
      })
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      const text = await response.text()
      await navigator.clipboard.writeText(text)
      button.textContent = 'Copied'
      status.textContent = 'Full public documentation copied for agent handoff.'
    } catch {
      status.textContent = 'Copy unavailable. '
      const link = document.createElement('a')
      link.href = button.dataset.copyHandoff
      link.textContent = 'Open the full context bundle.'
      status.append(link)
    } finally {
      button.disabled = false
      window.setTimeout(() => {
        button.textContent = original
      }, 2500)
    }
  })
})()
