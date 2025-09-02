import { ref } from 'vue'

export const isLoading = ref(false)

export const startLoading = () => {
  isLoading.value = true
}

export const stopLoading = () => {
  isLoading.value = false
}

export const withLoading = async (asyncFunction: Function) => {
  startLoading()
  try {
    return await asyncFunction()
  } finally {
    stopLoading()
  }
}
