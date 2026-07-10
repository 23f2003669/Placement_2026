function toDate(value) {
  if (!value) return null
  const d = new Date(value)
  return isNaN(d.getTime()) ? null : d
}

export function formatDate(value, locale = 'en-IN') {
  const d = toDate(value)
  if (!d) return '—'
  return new Intl.DateTimeFormat(locale, {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  }).format(d) // e.g. 10 Jul 2026
}

export function formatDateTime(value, locale = 'en-IN') {
  const d = toDate(value)
  if (!d) return '—'
  return new Intl.DateTimeFormat(locale, {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  }).format(d) // e.g. 10 Jul 2026, 09:30 PM
}

export function formatDateTimeWithZone(value, locale = 'en-IN') {
  const d = toDate(value)
  if (!d) return '—'
  return new Intl.DateTimeFormat(locale, {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
    timeZoneName: 'short'
  }).format(d) // e.g. 10 Jul 2026, 09:30 PM IST
}