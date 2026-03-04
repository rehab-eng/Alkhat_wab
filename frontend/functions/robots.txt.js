export async function onRequest() {
  const body = 'User-agent: *\nDisallow:\n\nSitemap: https://khututalrimal.ly/sitemap.xml\n'

  return new Response(body, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'no-store, max-age=0',
    },
  })
}
