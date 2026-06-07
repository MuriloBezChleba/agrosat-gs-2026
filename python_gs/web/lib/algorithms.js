// Implementações dos algoritmos de busca e ordenação (espelham o Python)

export function quickSort(arr, keyFn, low = 0, high = arr.length - 1) {
  if (low < high) {
    const p = partition(arr, keyFn, low, high)
    quickSort(arr, keyFn, low, p)
    quickSort(arr, keyFn, p + 1, high)
  }
  return arr
}

function partition(arr, keyFn, low, high) {
  const pivot = keyFn(arr[Math.floor((low + high) / 2)])
  let left = low
  let right = high
  while (true) {
    while (keyFn(arr[left]) < pivot) left++
    while (keyFn(arr[right]) > pivot) right--
    if (left >= right) return right
    ;[arr[left], arr[right]] = [arr[right], arr[left]]
    left++
    right--
  }
}

export function mergeSort(arr, keyFn) {
  if (arr.length <= 1) return [...arr]
  const mid = Math.floor(arr.length / 2)
  const left = mergeSort(arr.slice(0, mid), keyFn)
  const right = mergeSort(arr.slice(mid), keyFn)
  return merge(left, right, keyFn)
}

function merge(left, right, keyFn) {
  const result = []
  let i = 0, j = 0
  while (i < left.length && j < right.length) {
    if (keyFn(left[i]) <= keyFn(right[j])) result.push(left[i++])
    else result.push(right[j++])
  }
  return result.concat(left.slice(i)).concat(right.slice(j))
}

export function binarySearch(sortedArr, target, keyFn) {
  let low = 0, high = sortedArr.length - 1
  while (low <= high) {
    const mid = Math.floor((low + high) / 2)
    const val = keyFn(sortedArr[mid])
    if (val === target) return sortedArr[mid]
    else if (val < target) low = mid + 1
    else high = mid - 1
  }
  return null
}

export function linearSearch(arr, predicate) {
  return arr.filter(predicate)
}
