
function trimNum(x) { return parseFloat(x.toFixed(1)).toString() }
function inr(n) { return '\u20b9' + Number(n).toLocaleString('en-IN') }

export function formatSalaryShort(amount) {
  if (amount === null || amount === undefined || amount === '') return '\u2014'
  const n = Number(amount)
  if (isNaN(n)) return '\u2014'
  if (n >= 100000) return '\u20b9' + trimNum(n / 100000) + ' LPA'
  if (n >= 1000) return '\u20b9' + trimNum(n / 1000) + 'k'
  return '\u20b9' + n
}
export function formatSalary(amount) {
  if (amount === null || amount === undefined || amount === '') return '\u2014'
  const n = Number(amount)
  if (isNaN(n)) return '\u2014'
  if (n >= 100000) return '\u20b9' + trimNum(n / 100000) + ' LPA (' + inr(n) + ')'
  if (n >= 1000) return '\u20b9' + trimNum(n / 1000) + 'k'
  return '\u20b9' + n
}
export function formatSalaryRange(min, max) {
  if (!min && !max) return '\u2014'
  if (!(min && max)) return formatSalary(min || max)
  const a = Number(min), b = Number(max)
  if (a >= 100000 && b >= 100000) return '\u20b9' + trimNum(a/100000) + ' \u2013 ' + trimNum(b/100000) + ' LPA'
  if (a >= 1000 && a < 100000 && b >= 1000 && b < 100000) return '\u20b9' + trimNum(a/1000) + ' \u2013 ' + trimNum(b/1000) + 'k'
  return formatSalaryShort(a) + ' \u2013 ' + formatSalaryShort(b)
}
