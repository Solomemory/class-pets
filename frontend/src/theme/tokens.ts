export const themeTokens = {
  color: {
    bgPrimary: '#0b111a',
    bgSecondary: '#121a25',
    surface: '#1a2432',
    surfaceStrong: '#233245',
    line: '#2e3f58',
    textPrimary: '#e8f0ff',
    textSecondary: '#9db2cd',
    accentGold: '#f0c768',
    accentCyan: '#4ed0ff',
    accentPurple: '#8d7bff',
    accentCrimson: '#ff7a59',
    success: '#4ee3a3',
  },
  shadow: {
    glow: '0 0 30px rgba(78, 208, 255, 0.22)',
    goldGlow: '0 0 24px rgba(240, 199, 104, 0.28)',
  },
};

export const rarityPalette: Record<string, { border: string; chip: string }> = {
  稀有: { border: '#4ed0ff', chip: '#15445a' },
  史诗: { border: '#b18cff', chip: '#33295f' },
  传说: { border: '#f0c768', chip: '#4b3a12' },
  普通: { border: '#7f92ad', chip: '#2a3340' },
};
