export const sendMessage = message => {
	if (typeof window === 'undefined') return
	const iframe = document.querySelector('iframe.giscus-frame') as any
	if (!iframe) return
	iframe.contentWindow.postMessage({ giscus: message }, 'https://islamicrevival.github.io')
}
q
export const getCommentTheme = (isDark: boolean) => isDark ? 'dark' : 'light'

export const setCommentTheme = (isDark: boolean) => sendMessage({ setConfig: { theme: getCommentTheme(isDark) } })
