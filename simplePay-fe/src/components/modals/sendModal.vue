<template>
  <dialog id="sendModal" class="modal">
    <div class="modal-box">
      <form method="dialog" @submit.prevent="withLoading(sendMoney)">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-medium">Invia denaro</h2>
          <button id="closeSendModal" type="button" class="btn btn-sm btn-circle" onclick="sendModal.close()">✕</button>
        </div>
        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text font-medium">Destinatario</span>
          </label>
          <input
            id="emailInput"
            type="email"
            class="input input-bordered w-full"
            placeholder="Email del destinatario"
            required
            v-model="form.to_user_email"
          />
        </div>

        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text font-medium">Importo</span>
          </label>
          <input
            id="amountInput"
            type="number"
            class="input input-bordered w-full"
            placeholder="0,00"
            step="0.01"
            pattern="^\d+(\.\d{1,2})?$"
            v-model="form.amount"
            required
          />
        </div>

        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text font-medium">Messaggio (opzionale)</span>
          </label>
          <input
            type="text"
            class="input input-bordered w-full"
            placeholder="Aggiungi una nota"
            v-model="form.description"
          />
        </div>

        <button :disabled="isLoading" class="btn bg-black text-white w-full hover:bg-gray-800">
          <span class="loading loading-dots" v-if="isLoading"></span>Invia
        </button>
        <button
          :disabled="isLoading"
          type="button"
          class="btn w-full mt-4"
          onclick="sendModal.close()"
        >
          Annulla
        </button>
      </form>
    </div>
  </dialog>
</template>

<script lang="ts" setup>
import type { SendMoneyRequest } from '@/api/payments'
import payments from '@/api/payments'
import { notify } from '@/service/alert'
import { isLoading, withLoading } from '@/service/loading'
import { ref } from 'vue'

const emit = defineEmits(['refresh'])

const form = ref<SendMoneyRequest>({
  amount: null,
  to_user_email: '',
  description: ''
})

const sendMoney = async () => {
  try {
    await payments.sendMoney(form.value)
    notify('success', 'Denaro inviato con successo!')
  } catch (error) {
    console.error('Error sending money:', error)
  } finally {
    const sendModal = document.getElementById('sendModal') as HTMLDialogElement
    sendModal.close()
    clearForm()
  }
}

const clearForm = () => {
  emit('refresh')
  form.value = {
    amount: null,
    to_user_email: '',
    description: ''
  }
}
</script>
