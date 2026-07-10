function trimNum(x) {
  return parseFloat(x.toFixed(2)).toString()
}

function inr(n) {
  return '₹' + Number(n).toLocaleString('en-IN')
}

function titleCase(s) {
  if (!s) return ''
  return s.charAt(0).toUpperCase() + s.slice(1).toLowerCase()
}

// Compact display text for salary (no brackets)
function compactAnnual(n) {
  if (n < 100000) return inr(n)
  if (n >= 10000000) return `₹${trimNum(n / 10000000)} Cr`
  return `₹${trimNum(n / 100000)} LPA`
}

// Detailed text for tooltip
function detailedAnnual(n) {
  return `${inr(n)} per annum`
}

export function formatSalaryShort(amount) {
  if (amount === null || amount === undefined || amount === '') return '—'
  const n = Number(amount)
  if (isNaN(n) || n < 0) return '—'
  return compactAnnual(n)
}

// Clean table display (no bracket)
export function formatSalary(amount) {
  if (amount === null || amount === undefined || amount === '') return '—'
  const n = Number(amount)
  if (isNaN(n) || n < 0) return '—'
  return compactAnnual(n)
}

// Tooltip/detailed text
export function formatSalaryFull(amount) {
  if (amount === null || amount === undefined || amount === '') return '—'
  const n = Number(amount)
  if (isNaN(n) || n < 0) return '—'
  return detailedAnnual(n)
}

/**
 * Consistent range rule:
 * - both <1L => INR–INR
 * - both 1L.. <1Cr => LPA–LPA
 * - both >=1Cr => Cr–Cr
 * - mixed buckets => INR–INR (avoid ugly mixed units)
 */
export function formatSalaryRange(min, max) {
  const hasMin = min !== null && min !== undefined && min !== ''
  const hasMax = max !== null && max !== undefined && max !== ''

  if (!hasMin && !hasMax) return '—'
  if (!hasMin || !hasMax) return formatSalary(hasMin ? min : max)

  const a = Number(min)
  const b = Number(max)
  if (isNaN(a) || isNaN(b) || a < 0 || b < 0) return '—'

  const low = Math.min(a, b)
  const high = Math.max(a, b)

  const bucket = (x) => (x < 100000 ? 'INR' : x < 10000000 ? 'LPA' : 'CR')
  const bl = bucket(low)
  const bh = bucket(high)

  if (bl !== bh) {
    return `${inr(low)} – ${inr(high)}`
  }

  if (bl === 'INR') return `${inr(low)} – ${inr(high)}`
  if (bl === 'LPA') return `₹${trimNum(low / 100000)} – ₹${trimNum(high / 100000)} LPA`
  return `₹${trimNum(low / 10000000)} – ₹${trimNum(high / 10000000)} Cr`
}

// Optional helper for badges/text
export function formatStatus(s) {
  return titleCase(s || '')
}