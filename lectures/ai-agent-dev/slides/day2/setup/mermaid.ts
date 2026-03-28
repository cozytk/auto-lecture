import { defineMermaidSetup } from '@slidev/types'

export default defineMermaidSetup(() => {
  return {
    theme: 'base',
    themeVariables: {
      // 배경/텍스트
      primaryColor: '#3b82f6',
      primaryTextColor: '#f1f5f9',
      primaryBorderColor: '#60a5fa',
      secondaryColor: '#10b981',
      secondaryTextColor: '#f1f5f9',
      secondaryBorderColor: '#34d399',
      tertiaryColor: '#8b5cf6',
      tertiaryTextColor: '#f1f5f9',
      tertiaryBorderColor: '#a78bfa',

      // 라인/텍스트
      lineColor: '#94a3b8',
      textColor: '#e2e8f0',

      // 노드
      mainBkg: '#1e293b',
      nodeBorder: '#475569',
      nodeTextColor: '#f1f5f9',

      // Flowchart
      clusterBkg: '#1e293b',
      clusterBorder: '#475569',
      defaultLinkColor: '#94a3b8',
      titleColor: '#f1f5f9',
      edgeLabelBackground: '#1e293b',

      // Sequence diagram
      actorBkg: '#1e3a5f',
      actorBorder: '#60a5fa',
      actorTextColor: '#f1f5f9',
      actorLineColor: '#64748b',
      signalColor: '#e2e8f0',
      signalTextColor: '#e2e8f0',
      labelBoxBkgColor: '#1e293b',
      labelBoxBorderColor: '#475569',
      labelTextColor: '#e2e8f0',
      loopTextColor: '#e2e8f0',
      activationBorderColor: '#60a5fa',
      activationBkgColor: '#1e3a5f',
      sequenceNumberColor: '#f1f5f9',

      // Note
      noteBkgColor: '#292524',
      noteTextColor: '#e2e8f0',
      noteBorderColor: '#57534e',

      // Pie
      pie1: '#3b82f6',
      pie2: '#10b981',
      pie3: '#f59e0b',
      pie4: '#ef4444',
      pie5: '#8b5cf6',
      pie6: '#ec4899',
      pieStrokeColor: '#1e293b',
      pieSectionTextColor: '#f1f5f9',
      pieLegendTextColor: '#e2e8f0',
      pieTitleTextColor: '#f1f5f9',

      // Font
      fontFamily: 'Freesentation, sans-serif',
      fontSize: '16px',
    },
  }
})
