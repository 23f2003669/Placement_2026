export function isAuthenticated() {
  return !!localStorage.getItem('token')
}

export function getCurrentUser() {
  const user = localStorage.getItem('user')

  if (!user) return null

  return JSON.parse(user)
}