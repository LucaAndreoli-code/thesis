import { ref } from 'vue'

export interface Alert {
  type: 'success' | 'error' | 'info' | 'warning'
  message: string
}

export const alert = ref<Alert>({ type: 'info', message: '' })

export function notify(type: Alert['type'], message: string) {
  alert.value.type = type
  alert.value.message = message
  setTimeout(() => {
    alert.value.message = ''
  }, 3000)
  console.log(alert.value)
}
