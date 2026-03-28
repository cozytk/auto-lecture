import { defineMermaidSetup } from '@slidev/types'

export default defineMermaidSetup(() => {
  return {
    theme: 'dark',
    themeVariables: {
      primaryColor: '#3b82f6',
      primaryTextColor: '#f8fafc',
      primaryBorderColor: '#60a5fa',
      secondaryColor: '#1e293b',
      secondaryTextColor: '#e2e8f0',
      tertiaryColor: '#334155',
      lineColor: '#94a3b8',
      textColor: '#e2e8f0',
      mainBkg: '#1e293b',
      nodeBorder: '#60a5fa',
      clusterBkg: '#0f172a',
      clusterBorder: '#475569',
      titleColor: '#f8fafc',
      edgeLabelBackground: '#1e293b',
      nodeTextColor: '#f8fafc',
    },
  }
})
